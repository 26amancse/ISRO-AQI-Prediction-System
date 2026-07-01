import ee
import geemap

ee.Initialize(project="aqi-hackathon-500714")

Map = geemap.Map()

india = ee.FeatureCollection("FAO/GAUL/2015/level0") \
    .filter(ee.Filter.eq("ADM0_NAME", "India"))

image = (
    ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_HCHO")
    .filterDate("2023-01-01", "2023-01-31")
    .select("tropospheric_HCHO_column_number_density")
    .mean()
    .clip(india)
)

Map.centerObject(india, 5)

Map.addLayer(
    image,
    {
        "min": 0,
        "max": 0.0003,
        "palette": ["blue", "green", "yellow", "red"]
    },
    "HCHO"
)

Map.to_html("india_hcho_map.html")
print("Map saved successfully!")