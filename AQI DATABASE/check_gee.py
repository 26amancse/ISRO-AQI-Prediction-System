import ee

PROJECT_ID = "aqi-hackathon-500714"

ee.Initialize(project=PROJECT_ID)

print("Google Earth Engine Connected Successfully!")

count = ee.ImageCollection(
    "COPERNICUS/S5P/OFFL/L3_HCHO"
).size().getInfo()

print("Number of HCHO Images:", count)