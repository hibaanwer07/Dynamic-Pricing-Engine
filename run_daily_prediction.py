import psycopg2
import pandas as pd
from datetime import date, timedelta
import random
import xgboost as xgb

# ---------- DB CONFIG ----------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "hiba0702",
    "database": "pricing_engine"
}

# ---------- LOAD SAVED XGBOOST MODEL ----------
model = xgb.Booster()
model.load_model(r"C:\Users\ASUS\Documents\Dynamic_pricing_engine\notebooks\xgb_price_model.json")

# ---------- FEATURES ----------
trained_features = [
    "product_id", "brand", "storage_variant", "category", "units_sold",
    "revenue", "stock", "discount", "views", "clicks", "add_to_cart",
    "purchases", "bounce_rate", "flipkart_price", "amazon_price",
    "myntra_price", "day_of_week", "month", "is_weekend",
    "price_lag1", "price_rolling1", "price_lag7", "price_rolling7",
    "flipkart_price_lag1", "flipkart_price_lag7",
    "amazon_price_lag1", "amazon_price_lag7",
    "myntra_price_lag1", "myntra_price_lag7"
]

CAT_COLS = ["brand", "storage_variant", "category", "product_id"]
LAG_COLS = [col for col in trained_features if "lag" in col or "rolling" in col]

# ---------- CONNECT ----------
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# ---------- CREATE TABLES IF NOT EXISTS ----------
cursor.execute("DROP TABLE IF EXISTS daily_features;")
cursor.execute("""
CREATE TABLE daily_features (
    date DATE,
    product_id VARCHAR(10),
    brand VARCHAR(50),
    storage_variant VARCHAR(20),
    category VARCHAR(20),
    units_sold INTEGER,
    revenue INTEGER,
    stock INTEGER,
    discount INTEGER,
    is_festival BOOLEAN,
    views INTEGER,
    clicks INTEGER,
    add_to_cart INTEGER,
    purchases INTEGER,
    bounce_rate FLOAT,
    flipkart_price INTEGER,
    amazon_price INTEGER,
    myntra_price INTEGER,
    day_of_week INTEGER,
    month INTEGER,
    is_weekend BOOLEAN,
    price_lag1 FLOAT,
    price_rolling1 FLOAT,
    price_lag7 FLOAT,
    price_rolling7 FLOAT,
    flipkart_price_lag1 FLOAT,
    flipkart_price_lag7 FLOAT,
    amazon_price_lag1 FLOAT,
    amazon_price_lag7 FLOAT,
    myntra_price_lag1 FLOAT,
    myntra_price_lag7 FLOAT,
    PRIMARY KEY (date, product_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS predicted_prices (
    date DATE,
    product_id VARCHAR(10),
    predicted_price FLOAT,
    PRIMARY KEY (date, product_id)
);
""")

# ---------- DROP OLD PRICE COLUMN IF EXISTS ----------
cursor.execute("ALTER TABLE daily_features DROP COLUMN IF EXISTS price;")
conn.commit()

# ---------- PRODUCT LIST ----------
products = [
    {"product_id":"M100", "brand":"Samsung", "storage_variant":"64GB", "category":"Mobile"},
    {"product_id":"M101", "brand":"Samsung", "storage_variant":"128GB", "category":"Mobile"},
    {"product_id":"M102", "brand":"Redmi", "storage_variant":"128GB", "category":"Mobile"},
    {"product_id":"M103", "brand":"Redmi", "storage_variant":"64GB", "category":"Mobile"},
    {"product_id":"M104", "brand":"Realme", "storage_variant":"128GB", "category":"Mobile"},
    {"product_id":"M105", "brand":"Realme", "storage_variant":"64GB", "category":"Mobile"},
    {"product_id":"M106", "brand":"Apple", "storage_variant":"128GB", "category":"Mobile"},
    {"product_id":"M107", "brand":"Apple", "storage_variant":"256GB", "category":"Mobile"},
    {"product_id":"M108", "brand":"OnePlus", "storage_variant":"128GB", "category":"Mobile"},
    {"product_id":"M109", "brand":"OnePlus", "storage_variant":"256GB", "category":"Mobile"},
    # add as many as you want
]


# ---------- DATE RANGE ----------
end_date = date.today() - timedelta(days=1)
start_date = end_date - timedelta(days=30)  # Last 30 days
date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

# ---------- PREPARE DATAFRAME ----------
all_rows = []

for current_date in date_list:
    for prod in products:
        units_sold = random.randint(1, 30)
        price = random.randint(10000, 50000)
        is_festival = random.choice([True, False])
        is_weekend = current_date.weekday() >= 5

        row = {
            "date": current_date,
            "product_id": prod["product_id"],
            "brand": prod["brand"],
            "storage_variant": prod["storage_variant"],
            "category": prod["category"],
            "units_sold": units_sold,
            "revenue": price * units_sold,
            "stock": random.randint(40, 120),
            "discount": random.randint(0, 10),
            "is_festival": is_festival,
            "views": random.randint(100, 700),
            "clicks": random.randint(30, 100),
            "add_to_cart": random.randint(0, 70),
            "purchases": random.randint(1, units_sold),
            "bounce_rate": round(random.uniform(30, 80), 2),
            "flipkart_price": random.randint(10000, 50000),
            "amazon_price": random.randint(10000, 50000),
            "myntra_price": random.randint(10000, 50000),
            "day_of_week": current_date.weekday(),
            "month": current_date.month,
            "is_weekend": is_weekend,
        }
        # initialize lag columns to 0
        for col in LAG_COLS:
            row[col] = 0
        all_rows.append(row)

df = pd.DataFrame(all_rows)

# ---------- ENCODE CATEGORICALS ----------
for col in CAT_COLS:
    df[col] = df[col].astype("category").cat.codes.astype(int)

# ---------- FILL LAGS ----------
df.sort_values(["product_id", "date"], inplace=True)
for prod_id in df["product_id"].unique():
    prod_df = df[df["product_id"] == prod_id].copy()
    for lag in [1, 7]:
        prod_df[f"price_lag{lag}"] = prod_df["revenue"].shift(lag).fillna(0)
        for comp in ["flipkart_price", "amazon_price", "myntra_price"]:
            prod_df[f"{comp}_lag{lag}"] = prod_df[comp].shift(lag).fillna(0)
    df.update(prod_df)

# ---------- PREDICT ----------
X = df[trained_features]
dX = xgb.DMatrix(X)
df["predicted_price"] = model.predict(dX)

# ---------- UPSERT DAILY FEATURES & PREDICTIONS ----------
FEATURE_ORDER = [
    "date", "product_id", "brand", "storage_variant", "category",
    "units_sold", "revenue", "stock", "discount", "is_festival",
    "views", "clicks", "add_to_cart", "purchases", "bounce_rate",
    "flipkart_price", "amazon_price", "myntra_price",
    "day_of_week", "month", "is_weekend"
] + LAG_COLS

# Use a single bulk insert for all rows
args_str = ",".join(cursor.mogrify(
    "(" + ",".join(["%s"] * len(FEATURE_ORDER)) + ")", tuple(row[col] for col in FEATURE_ORDER)
).decode() for _, row in df.iterrows())
update_cols = ", ".join([f"{col}=EXCLUDED.{col}" for col in FEATURE_ORDER[2:]])

cursor.execute(f"""
    INSERT INTO daily_features ({','.join(FEATURE_ORDER)})
    VALUES {args_str}
    ON CONFLICT (date, product_id) DO UPDATE SET
        {update_cols}
""")

# Predicted prices
pred_args = ",".join(cursor.mogrify(
    "(%s,%s,%s)", (row["date"], row["product_id"], float(row["predicted_price"]))
).decode() for _, row in df.iterrows())
cursor.execute(f"""
    INSERT INTO predicted_prices (date, product_id, predicted_price)
    VALUES {pred_args}
    ON CONFLICT (date, product_id) DO UPDATE SET
        predicted_price = EXCLUDED.predicted_price
""")

conn.commit()
cursor.close()
conn.close()

print(f"✅ Daily features + predicted prices upserted from {start_date} to {end_date} for {len(products)} products/day.")
