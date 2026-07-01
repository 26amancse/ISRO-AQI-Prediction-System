import ee

PROJECT_ID = "aqi-hackathon-500714"

ee.Initialize(project=PROJECT_ID)

# India boundary
india = (
    ee.FeatureCollection("FAO/GAUL/2015/level0")
    .filter(ee.Filter.eq("ADM0_NAME", "India"))
)

start_date = "2023-01-01"
end_date = "2023-01-31"

# ---------------- HCHO ----------------
hcho = (
    ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_HCHO")
    .filterDate(start_date, end_date)
    .select("tropospheric_HCHO_column_number_density")
    .mean()
    .clip(india)
)

# ---------------- NO2 ----------------
no2 = (
    ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
    .filterDate(start_date, end_date)
    .select("tropospheric_NO2_column_number_density")
    .mean()
    .clip(india)
)

# ---------------- CO ----------------
co = (
    ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CO")
    .filterDate(start_date, end_date)
    .select("CO_column_number_density")
    .mean()
    .clip(india)
)

# ---------------- SO2 ----------------
so2 = (
    ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_SO2")
    .filterDate(start_date, end_date)
    .select("SO2_column_number_density")
    .mean()
    .clip(india)
)
print("HCHO")
print(
    hcho.reduceRegion(
        ee.Reducer.mean(),
        india.geometry(),
        1000,
        maxPixels=1e13,
    ).getInfo()
)

print("\nNO2")
print(
    no2.reduceRegion(
        ee.Reducer.mean(),
        india.geometry(),
        1000,
        maxPixels=1e13,
    ).getInfo()
)

print("\nCO")
print(
    co.reduceRegion(
        ee.Reducer.mean(),
        india.geometry(),
        1000,
        maxPixels=1e13,
    ).getInfo()
)

print("\nSO2")
print(
    so2.reduceRegion(
        ee.Reducer.mean(),
        india.geometry(),
        1000,
        maxPixels=1e13,
    ).getInfo()
)