import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import cross_val_score
import xgboost as xgb
import joblib

# Load dataset
df = pd.read_csv(r"data/preprocessing/final_preprocessed_dataset.csv")
df["date"] = pd.to_datetime(df["date"])

# Encode categorical columns as in training
categorical_cols = ["product_id", "brand", "storage_variant", "category"]
for col in categorical_cols:
    df[col] = df[col].astype("category").cat.codes

# Add lag features as in training
def add_lag_features(df, target_col="price", lags=[1, 7]):
    df = df.sort_values(["product_id", "date"])
    for lag in lags:
        df[f"{target_col}_lag{lag}"] = df.groupby("product_id")[target_col].shift(lag)
        df[f"{target_col}_rolling{lag}"] = df.groupby("product_id")[target_col].shift(1).rolling(lag).mean()
    df = df.dropna().reset_index(drop=True)
    return df

df = add_lag_features(df)

# Competitor lags
competitor_cols = ["flipkart_price", "amazon_price", "myntra_price"]
for col in competitor_cols:
    for lag in [1, 7]:
        df[f"{col}_lag{lag}"] = df.groupby("product_id")[col].shift(lag)
df = df.dropna().reset_index(drop=True)

# Train/test split
train = df[df["date"] < "2024-10-01"]
test = df[df["date"] >= "2024-10-01"]

X_train = train.drop(["price", "date"], axis=1)
y_train = train["price"]
X_test = test.drop(["price", "date"], axis=1)
y_test = test["price"]

# Load model
model = joblib.load(r"notebooks/xgb_price_model.pkl")

# Predict on train and test
dtrain = xgb.DMatrix(X_train)
dtest = xgb.DMatrix(X_test)
train_preds = model.predict(dtrain)
test_preds = model.predict(dtest)

# Compute metrics
train_r2 = r2_score(y_train, train_preds)
test_r2 = r2_score(y_test, test_preds)
mae = mean_absolute_error(y_test, test_preds)
rmse = np.sqrt(mean_squared_error(y_test, test_preds))

print(f"Train R² Score: {train_r2:.4f}")
print(f"Test R² Score: {test_r2:.4f}")
print(f"Difference (Train - Test R²): {train_r2 - test_r2:.4f}")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")

# Overfitting assessment
if train_r2 - test_r2 > 0.05:
    print("Warning: Potential overfitting detected (large gap between train and test R²).")
else:
    print("No significant overfitting; model generalizes well.")
