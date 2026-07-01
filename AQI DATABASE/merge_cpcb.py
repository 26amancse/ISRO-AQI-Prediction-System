import pandas as pd
import os

folder = "cpcb"

all_data = []

months = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

for filename in os.listdir(folder):

    if not filename.endswith(".xlsx"):
        continue

    station = filename.replace(".xlsx","")

    path = os.path.join(folder, filename)

    print("Reading:", filename)

    df = pd.read_excel(path)

    for month_num, month in enumerate(months, start=1):

        if month not in df.columns:
            continue

        temp = df[["Day", month]].copy()

        temp.columns = ["Day", "AQI"]

        temp["AQI"] = pd.to_numeric(temp["AQI"], errors="coerce")

        temp = temp.dropna()

        temp["Date"] = pd.to_datetime(
            {
                "year": 2023,
                "month": month_num,
                "day": temp["Day"]
            },
            errors="coerce"
        )

        temp = temp.dropna()

        temp["Station"] = station

        temp = temp[["Date","Station","AQI"]]

        all_data.append(temp)

merged = pd.concat(all_data, ignore_index=True)

merged = merged.sort_values("Date")

merged.to_csv("all_stations_aqi.csv", index=False)

print("\nDone!")
print("Total Records:", len(merged))
print("\nSaved as all_stations_aqi.csv")