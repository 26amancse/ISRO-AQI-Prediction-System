import ee

PROJECT_ID = "aqi-hackathon-500714"
ee.Initialize(project=PROJECT_ID)

point = ee.Geometry.Point([77.047, 28.592])

start = ee.Date("2023-01-01")
end = start.advance(1, "day")

aod = (
    ee.ImageCollection("MODIS/061/MCD19A2_GRANULES")
    .filterDate(start, end)
    .select("Optical_Depth_047")
    .mean()
)

value = aod.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=point,
    scale=1000,
    maxPixels=1e13
)

print(value.getInfo())