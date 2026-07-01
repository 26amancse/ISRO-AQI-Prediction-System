import ee
import joblib
import pandas as pd
import datetime

# -------------------------------------
# Initialize Earth Engine
# -------------------------------------

PROJECT_ID = "aqi-hackathon-500714"
ee.Initialize(project=PROJECT_ID)

# Delhi
LAT = 28.6139
LON = 77.2090

POINT = ee.Geometry.Point([LON, LAT])

# Use a few days back because Sentinel-5P has latency
today = datetime.date.today() - datetime.timedelta(days=5)

start = today.strftime("%Y-%m-%d")
end = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")


def get_feature(collection, band):

    try:

        image = (
            ee.ImageCollection(collection)
            .filterBounds(POINT)
            .filterDate(start, end)
            .mean()
        )

        value = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=POINT,
            scale=1000
        ).getInfo()

        return value.get(band)

    except:
        return None


# -------------------------------------
# Get Features
# -------------------------------------

HCHO = get_feature(
    "COPERNICUS/S5P/OFFL/L3_HCHO",
    "tropospheric_HCHO_column_number_density"
)

NO2 = get_feature(
    "COPERNICUS/S5P/OFFL/L3_NO2",
    "tropospheric_NO2_column_number_density"
)

CO = get_feature(
    "COPERNICUS/S5P/OFFL/L3_CO",
    "CO_column_number_density"
)

SO2 = get_feature(
    "COPERNICUS/S5P/OFFL/L3_SO2",
    "SO2_column_number_density"
)

AOD = get_feature(
    "MODIS/061/MCD19A2_GRANULES",
    "Optical_Depth_047"
)

print("Satellite Features")
print("------------------")
print("HCHO :", HCHO)
print("NO2  :", NO2)
print("CO   :", CO)
print("SO2  :", SO2)
print("AOD  :", AOD)

# Replace missing values
features = pd.DataFrame([{
    "HCHO": 0 if HCHO is None else HCHO,
    "NO2": 0 if NO2 is None else NO2,
    "CO": 0 if CO is None else CO,
    "SO2": 0 if SO2 is None else SO2,
    "AOD": 0 if AOD is None else AOD
}])

# -------------------------------------
# Load Model
# -------------------------------------

model = joblib.load("aqi_model.pkl")

prediction = model.predict(features)[0]

print("\n=========================")
print("Predicted AQI :", round(prediction, 2))
print("=========================")