import pandas as pd

# Read merged CPCB data
df = pd.read_csv("all_stations_aqi.csv")

# Keep only unique Station-Date combinations
df = df[["Date", "Station"]].drop_duplicates()

print(df.head())

print("\nUnique records:", len(df))

# Save
df.to_csv("feature_requests.csv", index=False)

print("\nSaved as feature_requests.csv")