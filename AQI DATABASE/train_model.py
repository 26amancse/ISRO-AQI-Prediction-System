import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load dataset
df = pd.read_csv("training_dataset_clean.csv")

# Features
X = df[
    [
        "HCHO",
        "NO2",
        "CO",
        "SO2",
        "AOD",
        "Temperature",
        "DewPoint",
        "Pressure",
        "Wind_U",
        "Wind_V",
    ]
]

# Target
y = df["AQI"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# Base model
rf = RandomForestRegressor(random_state=42)

# Parameter search space
param_grid = {
    "n_estimators": [100, 200, 300, 500],
    "max_depth": [10, 20, 30, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "max_features": ["sqrt", "log2"]
}

search = RandomizedSearchCV(
    estimator=rf,
    param_distributions=param_grid,
    n_iter=20,
    cv=5,
    scoring="r2",
    random_state=42,
    n_jobs=-1
)

search.fit(X_train, y_train)

print("\nBest Parameters:")
print(search.best_params_)

model = search.best_estimator_

# Prediction
y_pred = model.predict(X_test)

# Metrics
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)

print("\n========== RESULTS ==========")
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R² :", round(r2, 3))

joblib.dump(model, "aqi_model.pkl")

print("\nModel saved successfully!")