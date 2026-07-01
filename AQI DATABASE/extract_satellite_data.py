import ee
import pandas as pd

# ----------------------------------
# Initialize Google Earth Engine
# ----------------------------------
PROJECT_ID = "aqi-hackathon-500714"
ee.Initialize(project=PROJECT_ID)

# ----------------------------------
# Load AQI Data
# ----------------------------------
df = pd.read_csv("clean_aqi.csv")

# ----------------------------------
# Station Coordinates
# Dwarka Sector 8, Delhi
# ----------------------------------
point = ee.Geometry.Point([77.047, 28.592])

results = []

# ----------------------------------
# Function to extract values
# ----------------------------------
def get_value(image):
    data = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point,
        scale=1000,
        maxPixels=1e13
    ).getInfo()

    if data:
        return list(data.values())[0]

    return None


# ----------------------------------
# Loop through AQI records
# ----------------------------------
for index, row in df.iterrows():

    date = row["Date"]
    aqi = row["AQI"]

    start = ee.Date(date)
    end = start.advance(1, "day")

    try:

        # ---------------- HCHO ----------------
        hcho = (
            ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_HCHO")
            .filterDate(start, end)
            .select("tropospheric_HCHO_column_number_density")
            .mean()
        )

        # ---------------- NO2 ----------------
        no2 = (
            ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
            .filterDate(start, end)
            .select("tropospheric_NO2_column_number_density")
            .mean()
        )

        # ---------------- CO ----------------
        co = (
            ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CO")
            .filterDate(start, end)
            .select("CO_column_number_density")
            .mean()
        )

        # ---------------- SO2 ----------------
        so2 = (
            ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_SO2")
            .filterDate(start, end)
            .select("SO2_column_number_density")
            .mean()
        )

        # ---------------- AOD ----------------
        aod = (
            ee.ImageCollection("MODIS/061/MCD19A2_GRANULES")
            .filterDate(start, end)
            .select("Optical_Depth_047")
            .mean()
        )

        # ---------------- ERA5 WEATHER ----------------
        weather = (
            ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
            .filterDate(start, end)
            .first()
        )

        weather_values = weather.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=10000,
            maxPixels=1e13
        ).getInfo()

        # Satellite values
        hcho_val = get_value(hcho)
        no2_val = get_value(no2)
        co_val = get_value(co)
        so2_val = get_value(so2)
        aod_val = get_value(aod)

        # Scale MODIS AOD
        if aod_val is not None:
            aod_val = aod_val / 1000

        # Weather values
        temperature = weather_values.get("temperature_2m")
        dewpoint = weather_values.get("dewpoint_temperature_2m")
        pressure = weather_values.get("surface_pressure")
        wind_u = weather_values.get("u_component_of_wind_10m")
        wind_v = weather_values.get("v_component_of_wind_10m")

        results.append({
            "Date": date,
            "AQI": aqi,
            "HCHO": hcho_val,
            "NO2": no2_val,
            "CO": co_val,
            "SO2": so2_val,
            "AOD": aod_val,
            "Temperature": temperature,
            "DewPoint": dewpoint,
            "Pressure": pressure,
            "Wind_U": wind_u,
            "Wind_V": wind_v
        })

        print(f"Processed {index+1}/{len(df)} : {date}")

    except Exception as e:
        print(f"Skipped {date} : {e}")

# ----------------------------------
# Save Dataset
# ----------------------------------
training = pd.DataFrame(results)

training.to_csv("training_dataset.csv", index=False)

print("\n================================")
print("Training Dataset Created")
print("Saved as training_dataset.csv")
print("================================\n")

print(training.head())