import ee

PROJECT_ID = "aqi-hackathon-500714"

ee.Initialize(project=PROJECT_ID)

image = ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR").first()

print(image.bandNames().getInfo())