import ee
import pandas as pd
import os
import time

# ==========================================================
# EARTH ENGINE INITIALIZATION
# ==========================================================

PROJECT_ID = "aqi-hackathon-500714"

ee.Initialize(project=PROJECT_ID)

print("✅ Google Earth Engine Connected")

# ==========================================================
# FILES
# ==========================================================

AQI_FILE = "all_stations_aqi.csv"
OUTPUT_FILE = "training_dataset_v2.csv"

# ==========================================================
# CHECK INPUT FILE
# ==========================================================

if not os.path.exists(AQI_FILE):
    raise FileNotFoundError(f"{AQI_FILE} not found!")

# ==========================================================
# LOAD AQI DATA
# ==========================================================

aqi_df = pd.read_csv(AQI_FILE)

print("\nAQI Records Loaded :", len(aqi_df))
print(aqi_df.head())

# ==========================================================
# VERIFY REQUIRED COLUMNS
# ==========================================================

required_columns = [
    "Date",
    "Station",
    "AQI"
]

for col in required_columns:

    if col not in aqi_df.columns:

        raise Exception(f"Missing column : {col}")

print("\n✅ Dataset Verified")

# ==========================================================
# CPCB STATION COORDINATES
# ==========================================================

station_coordinates = {

    "alipur": {
        "lat": 28.815329,
        "lon": 77.153010
    },

    "anand_vihar": {
        "lat": 28.646886,
        "lon": 77.316078
    },

    "ito": {
        "lat": 28.628624,
        "lon": 77.241060
    },

    "lodhi_road": {
        "lat": 28.591825,
        "lon": 77.227307
    },

    "mandir_marg": {
        "lat": 28.635760,
        "lon": 77.201061
    },

    "nsit_dwarka": {
        "lat": 28.609090,
        "lon": 77.038010
    },

    "punjabi_bagh": {
        "lat": 28.670270,
        "lon": 77.131023
    },

    "rk_puram": {
        "lat": 28.563262,
        "lon": 77.186937
    },

    "rohini": {
        "lat": 28.732528,
        "lon": 77.119920
    },

    "wazirpur": {
        "lat": 28.699782,
        "lon": 77.165453
    }

}

print("\n✅ Station Coordinates Loaded")

# ==========================================================
# EARTH ENGINE HELPER FUNCTION
# ==========================================================

def get_feature(collection, band, date, lat, lon):

    try:

        point = ee.Geometry.Point([lon, lat])

        start = ee.Date(date)
        end = start.advance(1, "day")

        image = (
            ee.ImageCollection(collection)
            .filterBounds(point)
            .filterDate(start, end)
            .mean()
        )

        value = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=1000,
            maxPixels=1e13
        ).getInfo()

        if value is None:
            return None

        return value.get(band)

    except Exception:
        return None

# ==========================================================
# OUTPUT DATASET
# ==========================================================

columns = [

    "Date",

    "Station",

    "Latitude",

    "Longitude",

    "AQI",

    "HCHO",

    "NO2",

    "CO",

    "SO2",

    "AOD",

    "Temperature",

    "Humidity",

    "Wind_U",

    "Wind_V"

]

training_data = []

print("\n===================================")
print("READY TO DOWNLOAD FEATURES")
print("Stations :", len(station_coordinates))
print("AQI Rows :", len(aqi_df))
print("===================================\n")