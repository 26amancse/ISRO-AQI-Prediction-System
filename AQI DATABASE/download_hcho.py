import ee

ee.Initialize()

collection = (
    ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_HCHO")
    .filterDate("2023-01-01", "2023-01-31")
)

print("Number of images:", collection.size().getInfo())