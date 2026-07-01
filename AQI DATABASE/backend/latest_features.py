import ee
import pandas as pd
import datetime
import os

# ==========================================
# INITIALIZE EARTH ENGINE
# ==========================================

PROJECT_ID = "aqi-hackathon-500714"

ee.Initialize(project=PROJECT_ID)

# ==========================================
# LOCATION (DELHI)
# ==========================================

LAT = 28.6139
LON = 77.2090

POINT = ee.Geometry.Point([LON, LAT])

# ==========================================
# TODAY
# ==========================================

today = datetime.date.today() - datetime.timedelta(days=5)

start = today.strftime("%Y-%m-%d")
end = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

# ==========================================
# HELPER FUNCTION
# ==========================================

def get_value(collection, band):

    try:

        image = (
            ee.ImageCollection(collection)
            .filterDate(start, end)
            .filterBounds(POINT)
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

# ==========================================
# SATELLITE FEATURES
# ==========================================

HCHO = get_value(
    "COPERNICUS/S5P/OFFL/L3_HCHO",
    "tropospheric_HCHO_column_number_density"
)

NO2 = get_value(
    "COPERNICUS/S5P/OFFL/L3_NO2",
    "tropospheric_NO2_column_number_density"
)

CO = get_value(
    "COPERNICUS/S5P/OFFL/L3_CO",
    "CO_column_number_density"
)

SO2 = get_value(
    "COPERNICUS/S5P/OFFL/L3_SO2",
    "SO2_column_number_density"
)

AOD = get_value(
    "MODIS/061/MCD19A2_GRANULES",
    "Optical_Depth_047"
)

TEMP = get_value(
    "ECMWF/ERA5/DAILY",
    "temperature_2m"
)

HUMIDITY = get_value(
    "ECMWF/ERA5/DAILY",
    "dewpoint_temperature_2m"
)

WIND_U = get_value(
    "ECMWF/ERA5/DAILY",
    "u_component_of_wind_10m"
)

WIND_V = get_value(
    "ECMWF/ERA5/DAILY",
    "v_component_of_wind_10m"
)

# ==========================================
# DATAFRAME
# ==========================================

df = pd.DataFrame({

    "Date":[start],

    "HCHO":[HCHO],

    "NO2":[NO2],

    "CO":[CO],

    "SO2":[SO2],

    "AOD":[AOD],

    "Temperature":[TEMP],

    "Humidity":[HUMIDITY],

    "Wind_U":[WIND_U],

    "Wind_V":[WIND_V]

})

# ==========================================
# SAVE
# ==========================================

os.makedirs("../data", exist_ok=True)

df.to_csv("../data/latest_features.csv", index=False)

print(df)

print("\nSaved as latest_features.csv")