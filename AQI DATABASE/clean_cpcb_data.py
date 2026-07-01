import pandas as pd

# Read Excel
df = pd.read_excel("aqi.xlsx.xlsx")

# Convert from wide to long format
df_long = df.melt(
    id_vars="Day",
    var_name="Month",
    value_name="AQI"
)

# Remove missing AQI values
df_long = df_long.dropna()

# Month mapping
month_map = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

# Convert month names to numbers
df_long["Month"] = df_long["Month"].map(month_map)

# Create Date column
df_long["Date"] = pd.to_datetime({
    "year": 2023,
    "month": df_long["Month"],
    "day": df_long["Day"]
}, errors="coerce")

# Remove invalid dates (e.g., February 30)
df_long = df_long.dropna(subset=["Date"])

# Keep only required columns
df_long = df_long[["Date", "AQI"]]

# Save cleaned data
df_long.to_csv("clean_aqi.csv", index=False)

print(df_long.head(20))

print("\nTotal Records:", len(df_long))
print("\nSaved as clean_aqi.csv")