import pandas as pd

# Load training dataset
df = pd.read_csv("training_dataset.csv")

print("Before cleaning:")
print(df.isnull().sum())

# Remove rows with missing values
df = df.dropna()

print("\nAfter cleaning:")
print(df.isnull().sum())

print("\nRemaining Records:", len(df))

# Save cleaned dataset
df.to_csv("training_dataset_clean.csv", index=False)

print("\nSaved as training_dataset_clean.csv")