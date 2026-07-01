"""
extract_features_gee.py
----------------------------------------
Part 1
Configuration + Initialization
ISRO Hackathon AQI Prediction Project
"""

import ee
import os
import time
import logging
import pandas as pd
from datetime import datetime

# ==========================================================
# GOOGLE EARTH ENGINE PROJECT
# ==========================================================

PROJECT_ID = "aqi-hackathon-500714"

ee.Initialize(project=PROJECT_ID)

print("✅ Google Earth Engine Initialized")

# ==========================================================
# INPUT / OUTPUT FILES
# ==========================================================

AQI_FILE = "all_stations_aqi.csv"

OUTPUT_FILE = "training_dataset_v2.csv"

CHECKPOINT_FILE = "checkpoint.txt"

LOG_FILE = "extract_features.log"

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("========================================")
logging.info("Feature Extraction Started")
logging.info("========================================")

# ==========================================================
# STATION COORDINATES
# ==========================================================

STATIONS = {

    "alipur": (77.153010, 28.815329),

    "anand_vihar": (77.316078, 28.646886),

    "ito": (77.241060, 28.628624),

    "lodhi_road": (77.227307, 28.591825),

    "mandir_marg": (77.201061, 28.635760),

    "nsit_dwarka": (77.038010, 28.609090),

    "punjabi_bagh": (77.131023, 28.670270),

    "rk_puram": (77.186937, 28.563262),

    "rohini": (77.119920, 28.732528),

    "wazirpur": (77.165453, 28.699782)
}

# ==========================================================
# LOAD AQI DATA
# ==========================================================

df = pd.read_csv(AQI_FILE)

print("\nAQI Records Loaded :", len(df))

logging.info(f"AQI Records : {len(df)}")

# ==========================================================
# CHECKPOINT SUPPORT
# ==========================================================

start_index = 0

if os.path.exists(CHECKPOINT_FILE):

    with open(CHECKPOINT_FILE, "r") as f:

        value = f.read().strip()

        if value.isdigit():

            start_index = int(value)

print("Resuming From Index :", start_index)

logging.info(f"Resume Index : {start_index}")

# ==========================================================
# CREATE OUTPUT FILE IF NOT EXISTS
# ==========================================================

if not os.path.exists(OUTPUT_FILE):

    columns = [

        "Date",
        "Station",
        "AQI",

        "Latitude",
        "Longitude",

        "HCHO",
        "NO2",
        "CO",
        "SO2",
        "AOD",

        "Temperature",
        "DewPoint",
        "Pressure",

        "Wind_U",
        "Wind_V"
    ]

    pd.DataFrame(columns=columns).to_csv(
        OUTPUT_FILE,
        index=False
    )

print("Output File Ready")

logging.info("Output CSV Ready")

# ==========================================================
# EARTH ENGINE DATASETS
# ==========================================================

DATASETS = {

    "HCHO": "COPERNICUS/S5P/OFFL/L3_HCHO",

    "NO2": "COPERNICUS/S5P/OFFL/L3_NO2",

    "CO": "COPERNICUS/S5P/OFFL/L3_CO",

    "SO2": "COPERNICUS/S5P/OFFL/L3_SO2",

    "AOD": "MODIS/061/MCD19A2_GRANULES",

    "ERA5": "ECMWF/ERA5_LAND/DAILY_AGGR"
}

print("Datasets Loaded")

logging.info("Datasets Loaded")

# ==========================================================
# TEST FIRST RECORD
# ==========================================================

print("\nFirst AQI Record")

print(df.iloc[start_index])

logging.info("Initialization Completed")
# ==========================================================
# PART 2
# FEATURE EXTRACTION FUNCTIONS
# ==========================================================

def reduce_image(image, point, scale=1000):
    """
    Reduce an image to a single value at a point.
    Returns None if no data is available.
    """
    try:
        values = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=scale,
            maxPixels=1e13
        ).getInfo()

        if values is None or len(values) == 0:
            return None

        return list(values.values())[0]

    except Exception:
        return None


# ==========================================================
# HCHO
# ==========================================================

def get_hcho(point, start, end):

    image = (
        ee.ImageCollection(DATASETS["HCHO"])
        .filterDate(start, end)
        .select("tropospheric_HCHO_column_number_density")
        .mean()
    )

    return reduce_image(image, point)


# ==========================================================
# NO2
# ==========================================================

def get_no2(point, start, end):

    image = (
        ee.ImageCollection(DATASETS["NO2"])
        .filterDate(start, end)
        .select("tropospheric_NO2_column_number_density")
        .mean()
    )

    return reduce_image(image, point)


# ==========================================================
# CO
# ==========================================================

def get_co(point, start, end):

    image = (
        ee.ImageCollection(DATASETS["CO"])
        .filterDate(start, end)
        .select("CO_column_number_density")
        .mean()
    )

    return reduce_image(image, point)


# ==========================================================
# SO2
# ==========================================================

def get_so2(point, start, end):

    image = (
        ee.ImageCollection(DATASETS["SO2"])
        .filterDate(start, end)
        .select("SO2_column_number_density")
        .mean()
    )

    return reduce_image(image, point)


# ==========================================================
# MODIS AOD
# ==========================================================

def get_aod(point, start, end):

    image = (
        ee.ImageCollection(DATASETS["AOD"])
        .filterDate(start, end)
        .select("Optical_Depth_047")
        .mean()
    )

    value = reduce_image(image, point)

    if value is None:
        return None

    return value / 1000.0


# ==========================================================
# ERA5 WEATHER
# ==========================================================

def get_weather(point, start, end):

    try:

        weather = (
            ee.ImageCollection(DATASETS["ERA5"])
            .filterDate(start, end)
            .first()
        )

        values = weather.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=10000,
            maxPixels=1e13
        ).getInfo()

        if values is None:
            return {
                "Temperature": None,
                "DewPoint": None,
                "Pressure": None,
                "Wind_U": None,
                "Wind_V": None
            }

        return {

            "Temperature":
                values.get("temperature_2m"),

            "DewPoint":
                values.get("dewpoint_temperature_2m"),

            "Pressure":
                values.get("surface_pressure"),

            "Wind_U":
                values.get("u_component_of_wind_10m"),

            "Wind_V":
                values.get("v_component_of_wind_10m")
        }

    except Exception:

        return {

            "Temperature": None,
            "DewPoint": None,
            "Pressure": None,
            "Wind_U": None,
            "Wind_V": None
        }


# ==========================================================
# EXTRACT ALL FEATURES
# ==========================================================

def extract_features(point, start, end):

    weather = get_weather(point, start, end)

    return {

        "HCHO": get_hcho(point, start, end),

        "NO2": get_no2(point, start, end),

        "CO": get_co(point, start, end),

        "SO2": get_so2(point, start, end),

        "AOD": get_aod(point, start, end),

        "Temperature": weather["Temperature"],

        "DewPoint": weather["DewPoint"],

        "Pressure": weather["Pressure"],

        "Wind_U": weather["Wind_U"],

        "Wind_V": weather["Wind_V"]
    }


print("Feature Extraction Functions Loaded")

logging.info("Feature Functions Loaded")
# ==========================================================
# PART 3
# MAIN EXTRACTION LOOP
# ==========================================================

print("\nStarting Feature Extraction...\n")

total_records = len(df)

processed = 0
failed = 0

for index in range(start_index, total_records):

    row = df.iloc[index]

    try:

        # -----------------------------
        # Read AQI Record
        # -----------------------------
        date = row["Date"]
        station = str(row["Station"]).strip().lower()
        aqi = row["AQI"]

        # -----------------------------
        # Check Station Exists
        # -----------------------------
        if station not in STATIONS:

            print(f"Unknown Station : {station}")

            logging.warning(f"Unknown Station : {station}")

            failed += 1

            continue

        # -----------------------------
        # Coordinates
        # -----------------------------
        lon, lat = STATIONS[station]

        point = ee.Geometry.Point([lon, lat])

        # -----------------------------
        # Dates
        # -----------------------------
        start = ee.Date(date)

        end = start.advance(1, "day")

        # -----------------------------
        # Extract Features
        # -----------------------------
        features = extract_features(
            point,
            start,
            end
        )

        # -----------------------------
        # Create Output Row
        # -----------------------------
        output = pd.DataFrame([{

            "Date": date,

            "Station": station,

            "AQI": aqi,

            "Latitude": lat,

            "Longitude": lon,

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

        # -----------------------------
        # Append CSV
        # -----------------------------
        output.to_csv(

            OUTPUT_FILE,

            mode="a",

            header=False,

            index=False

        )

        # -----------------------------
        # Save Checkpoint
        # -----------------------------
        with open(CHECKPOINT_FILE, "w") as f:

            f.write(str(index + 1))

        processed += 1

        # -----------------------------
        # Progress
        # -----------------------------
        print(
            f"[{index+1}/{total_records}] "
            f"{station} | {date} | "
            f"Processed"
        )

        logging.info(
            f"{station} {date} Processed"
        )

        # -----------------------------
        # Prevent EE Rate Limits
        # -----------------------------
        time.sleep(0.2)

    except Exception as e:

        failed += 1

        print(
            f"Failed : {station} {date}"
        )

        print(e)

        logging.error(
            f"{station} {date} : {e}"
        )

        continue

print("\n===================================")
print("Extraction Completed")
print("===================================")

print("Processed :", processed)

print("Failed :", failed)

print("Output :", OUTPUT_FILE)

logging.info("Extraction Finished")
logging.info(f"Processed : {processed}")
logging.info(f"Failed : {failed}")