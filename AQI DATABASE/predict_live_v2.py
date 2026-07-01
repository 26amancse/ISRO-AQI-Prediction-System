import ee
import joblib
import pandas as pd
import datetime
import warnings

warnings.filterwarnings("ignore")

# ==========================================================
# EARTH ENGINE INITIALIZATION
# ==========================================================

PROJECT_ID = "aqi-hackathon-500714"

ee.Initialize(project=PROJECT_ID)

print("==========================================")
print(" GOOGLE EARTH ENGINE CONNECTED ")
print("==========================================")

# ==========================================================
# LOCATION
# ==========================================================

LAT = 28.6139
LON = 77.2090

POINT = ee.Geometry.Point([LON, LAT])

# ==========================================================
# DATE
# (Satellite data usually has a delay)
# ==========================================================

today = datetime.date.today() - datetime.timedelta(days=5)

START_DATE = today.strftime("%Y-%m-%d")
END_DATE = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

print(f"\nUsing Date : {START_DATE}")

# ==========================================================
# GENERIC FEATURE FUNCTION
# ==========================================================

def get_feature(collection, band):

    try:

        image = (
            ee.ImageCollection(collection)
            .filterBounds(POINT)
            .filterDate(START_DATE, END_DATE)
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

        print(f"Error reading {band}")

        return None


# ==========================================================
# SAFE VALUE FUNCTION
# ==========================================================

def safe(value, default=0):

    if value is None:

        return default

    return value


print("\nReady to download live satellite features...\n")
# ==========================================================
# SATELLITE FEATURES
# ==========================================================

print("Downloading Sentinel-5P data...")

# ---------------------------------
# HCHO
# ---------------------------------

HCHO = get_feature(
    "COPERNICUS/S5P/OFFL/L3_HCHO",
    "tropospheric_HCHO_column_number_density"
)

# ---------------------------------
# NO2
# ---------------------------------

NO2 = get_feature(
    "COPERNICUS/S5P/OFFL/L3_NO2",
    "tropospheric_NO2_column_number_density"
)

# ---------------------------------
# CO
# ---------------------------------

CO = get_feature(
    "COPERNICUS/S5P/OFFL/L3_CO",
    "CO_column_number_density"
)

# ---------------------------------
# SO2
# ---------------------------------

SO2 = get_feature(
    "COPERNICUS/S5P/OFFL/L3_SO2",
    "SO2_column_number_density"
)

# ---------------------------------
# AOD (MODIS)
# ---------------------------------

print("Downloading MODIS AOD...")

AOD = get_feature(
    "MODIS/061/MCD19A2_GRANULES",
    "Optical_Depth_047"
)

# ==========================================================
# PRINT RESULTS
# ==========================================================

print("\n==========================================")
print("SATELLITE FEATURES")
print("==========================================")

print(f"HCHO : {HCHO}")
print(f"NO2  : {NO2}")
print(f"CO   : {CO}")
print(f"SO2  : {SO2}")
print(f"AOD  : {AOD}")
# ==========================================================
# ERA5-LAND WEATHER FEATURES
# ==========================================================

print("\nDownloading ERA5-Land Weather Data...")

ERA5 = (
    ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
    .filterBounds(POINT)
    .filterDate(START_DATE, END_DATE)
    .mean()
)

weather = ERA5.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=POINT,
    scale=1000,
    maxPixels=1e13
).getInfo()

Temperature = weather.get("temperature_2m")
DewPoint = weather.get("dewpoint_temperature_2m")
Pressure = weather.get("surface_pressure")
Wind_U = weather.get("u_component_of_wind_10m")
Wind_V = weather.get("v_component_of_wind_10m")

print("\n==========================================")
print("ERA5 WEATHER FEATURES")
print("==========================================")

print(f"Temperature : {Temperature}")
print(f"DewPoint    : {DewPoint}")
print(f"Pressure    : {Pressure}")
print(f"Wind_U      : {Wind_U}")
print(f"Wind_V      : {Wind_V}")
# ==========================================================
# ERA5 WEATHER FEATURES
# ==========================================================

# ==========================================================
# ERA5 WEATHER
# ==========================================================

print("\nDownloading ERA5 Weather...")

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

Temperature = values.get("temperature_2m")
DewPoint = values.get("dewpoint_temperature_2m")
Pressure = values.get("surface_pressure")
Wind_U = values.get("u_component_of_wind_10m")
Wind_V = values.get("v_component_of_wind_10m")

print("\n========== WEATHER ==========")
print("Temperature :", Temperature)
print("DewPoint    :", DewPoint)
print("Pressure    :", Pressure)
print("Wind_U      :", Wind_U)
print("Wind_V      :", Wind_V)
# ==========================================================
# PREPARE FEATURES
# ==========================================================

print("\nPreparing feature vector...")

features = pd.DataFrame([{

    "HCHO": safe(HCHO),

    "NO2": safe(NO2),

    "CO": safe(CO),

    "SO2": safe(SO2),

    "AOD": safe(AOD),

    "Temperature": safe(Temperature),

    "DewPoint": safe(DewPoint),

    "Pressure": safe(Pressure),

    "Wind_U": safe(Wind_U),

    "Wind_V": safe(Wind_V)

}])

print("\n================ FEATURE VECTOR ================\n")
print(features)

# ==========================================================
# LOAD MODEL
# ==========================================================

print("\nLoading trained model...")

MODEL_PATH = "aqi_model.pkl"

model = joblib.load(MODEL_PATH)

print("✅ Model Loaded Successfully")

# ==========================================================
# PREDICT AQI
# ==========================================================

prediction = model.predict(features)[0]

print("\n===============================================")
print("        LIVE AQI PREDICTION")
print("===============================================")

print(f"Prediction Date : {START_DATE}")
print(f"Latitude        : {LAT}")
print(f"Longitude       : {LON}")
print(f"Predicted AQI   : {round(prediction,2)}")

# ==========================================================
# AQI CATEGORY
# ==========================================================

aqi = prediction

if aqi <= 50:
    category = "Good 🟢"

elif aqi <= 100:
    category = "Satisfactory 🟡"

elif aqi <= 200:
    category = "Moderate 🟠"

elif aqi <= 300:
    category = "Poor 🔴"

elif aqi <= 400:
    category = "Very Poor 🟣"

else:
    category = "Severe ⚫"

print(f"Category        : {category}")

print("===============================================\n")

# ==========================================================
# SAVE RESULT
# ==========================================================

result = pd.DataFrame({

    "Date": [START_DATE],

    "Predicted_AQI": [round(prediction,2)],

    "Category": [category]

})

result.to_csv("latest_prediction.csv", index=False)

print("✅ Saved latest_prediction.csv")