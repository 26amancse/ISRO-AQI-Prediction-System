from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import ee
import os
import joblib
import pandas as pd

# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(

    title="ISRO AQI Prediction API",

    version="2.0"

)

# =====================================================
# CORS
# =====================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

# =====================================================
# GOOGLE EARTH ENGINE
# =====================================================

PROJECT_ID = "air-pollution-501117"

try:

    ee.Initialize(project=PROJECT_ID)

    print("\n===================================")
    print("Google Earth Engine Connected")
    print("===================================\n")

except Exception as e:

    print("\nEarth Engine Initialization Failed")
    print(e)

# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = os.path.abspath(

    os.path.join(BASE_DIR, "..")

)

MODEL_PATH = os.path.join(

    PROJECT_DIR,

    "aqi_model.pkl"

)

print("Model Path :", MODEL_PATH)

# =====================================================
# LOAD MODEL
# =====================================================

try:

    model = joblib.load(MODEL_PATH)

    print("AQI Model Loaded Successfully")

except Exception as e:

    model = None

    print("Unable to Load Model")

    print(e)

# =====================================================
# SAFE VALUE
# =====================================================

def safe(value):

    if value is None:

        return 0

    return value

print("Backend Ready")
# =====================================================
# LOCATION
# =====================================================

LATITUDE = 28.6139

LONGITUDE = 77.2090

POINT = ee.Geometry.Point([LONGITUDE, LATITUDE])

# =====================================================
# GET SATELLITE FEATURE
# =====================================================

def get_feature(collection, band, start_date, end_date):

    try:

        image = (
            ee.ImageCollection(collection)
            .filterBounds(POINT)
            .filterDate(start_date, end_date)
            .mean()
        )

        value = image.reduceRegion(

            reducer=ee.Reducer.mean(),

            geometry=POINT,

            scale=1000,

            maxPixels=1e13

        ).getInfo()

        if value is None:

            return None

        return value.get(band)

    except Exception as e:

        print(f"Error downloading {band}")

        print(e)

        return None


# =====================================================
# ERA5 WEATHER
# =====================================================

def get_weather():

    try:

        weather = (

            ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")

            .filterBounds(POINT)

            .sort("system:time_start", False)

            .first()

        )

        values = weather.reduceRegion(

            reducer=ee.Reducer.mean(),

            geometry=POINT,

            scale=10000,

            maxPixels=1e13

        ).getInfo()

        return {

            "Temperature": safe(values.get("temperature_2m")),

            "DewPoint": safe(values.get("dewpoint_temperature_2m")),

            "Pressure": safe(values.get("surface_pressure")),

            "Wind_U": safe(values.get("u_component_of_wind_10m")),

            "Wind_V": safe(values.get("v_component_of_wind_10m"))

        }

    except Exception as e:

        print("Weather Download Failed")

        print(e)

        return {

            "Temperature": 0,

            "DewPoint": 0,

            "Pressure": 0,

            "Wind_U": 0,

            "Wind_V": 0

        }


# =====================================================
# DOWNLOAD LIVE FEATURES
# =====================================================

def get_live_features():

    start = "2026-06-26"

    end = "2026-06-27"

    print("\nDownloading Sentinel-5P Data...")

    hcho = get_feature(

        "COPERNICUS/S5P/OFFL/L3_HCHO",

        "tropospheric_HCHO_column_number_density",

        start,

        end

    )

    no2 = get_feature(

        "COPERNICUS/S5P/OFFL/L3_NO2",

        "tropospheric_NO2_column_number_density",

        start,

        end

    )

    co = get_feature(

        "COPERNICUS/S5P/OFFL/L3_CO",

        "CO_column_number_density",

        start,

        end

    )

    so2 = get_feature(

        "COPERNICUS/S5P/OFFL/L3_SO2",

        "SO2_column_number_density",

        start,

        end

    )

    aod = get_feature(

        "MODIS/061/MCD19A2_GRANULES",

        "Optical_Depth_047",

        start,

        end

    )

    weather = get_weather()

    return {

        "HCHO": safe(hcho),

        "NO2": safe(no2),

        "CO": safe(co),

        "SO2": safe(so2),

        "AOD": safe(aod),

        **weather

    }
# =====================================================
# PREDICT AQI
# =====================================================

@app.get("/predict")
def predict():

    if model is None:

        return {

            "error": "AQI model not loaded"

        }

    try:

        features = get_live_features()

        X = pd.DataFrame([{

            "HCHO": features["HCHO"],

            "NO2": features["NO2"],

            "CO": features["CO"],

            "SO2": features["SO2"],

            "AOD": features["AOD"],

            "Temperature": features["Temperature"],

            "DewPoint": features["DewPoint"],

            "Pressure": features["Pressure"],

            "Wind_U": features["Wind_U"],

            "Wind_V": features["Wind_V"]

        }])

        prediction = float(model.predict(X)[0])

        wind_speed = (

            features["Wind_U"]**2 +

            features["Wind_V"]**2

        ) ** 0.5

        return {

            "aqi": round(prediction, 2),

            "temperature": round(

                features["Temperature"] - 273.15,

                2

            ),

            "pressure": round(

                features["Pressure"],

                2

            ),

            "wind": round(

                wind_speed,

                2

            ),

            "hcho": features["HCHO"],

            "no2": features["NO2"],

            "co": features["CO"],

            "so2": features["SO2"],

            "aod": features["AOD"]

        }

    except Exception as e:

        print("\nPrediction Failed")

        print(e)

        return {

            "error": str(e)

        }
    # =====================================================
# HOME
# =====================================================

@app.get("/")
def home():

    return {

        "status": "Running",

        "project": "ISRO AQI Prediction API",

        "version": "2.0",

        "model_loaded": model is not None

    }


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health():

    return {

        "status": "Healthy",

        "earth_engine": "Connected",

        "model_loaded": model is not None,

        "location": {

            "latitude": LATITUDE,

            "longitude": LONGITUDE

        }

    }


# =====================================================
# STARTUP MESSAGE
# =====================================================

print("\n=========================================")
print(" ISRO AQI PREDICTION API READY ")
print("=========================================")
print("Server : http://127.0.0.1:8000")
print("Home   : http://127.0.0.1:8000/")
print("Health : http://127.0.0.1:8000/health")
print("Predict: http://127.0.0.1:8000/predict")
print("=========================================\n")