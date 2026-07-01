import ee

# ==========================================================
# INITIALIZE GOOGLE EARTH ENGINE
# ==========================================================

PROJECT_ID = "aqi-hackathon-500714"

ee.Initialize(project=PROJECT_ID)

print("===================================")
print("Google Earth Engine Connected")
print("===================================")

# ==========================================================
# LOCATION (DELHI)
# ==========================================================

LAT = 28.6139
LON = 77.2090

point = ee.Geometry.Point([LON, LAT])

# ==========================================================
# GET LATEST AVAILABLE ERA5 IMAGE
# ==========================================================

weather = (
    ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
    .filterBounds(point)
    .sort("system:time_start", False)
    .first()
)

# ==========================================================
# EXTRACT WEATHER DATA
# ==========================================================

values = weather.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=point,
    scale=10000,
    maxPixels=1e13
).getInfo()

print("\n========== ERA5 WEATHER ==========\n")

features = [
    "temperature_2m",
    "dewpoint_temperature_2m",
    "surface_pressure",
    "u_component_of_wind_10m",
    "v_component_of_wind_10m",
    "total_precipitation_sum",
    "skin_temperature"
]

for feature in features:

    print(f"{feature:30} : {values.get(feature)}")

print("\n==================================")

print("\nTotal Variables Returned :", len(values))

print("\n==================================")
print("SUCCESS")
print("==================================")