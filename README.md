# Dynamic Pricing Engine

A machine learning-powered dynamic pricing system for e-commerce, specifically tailored for mobile products. The engine uses historical sales data, competitor pricing, and customer behavior to predict optimal prices that maximize revenue while considering market dynamics. It includes data preprocessing, model training/evaluation, daily prediction scripts, and an interactive Streamlit dashboard for visualization and insights.

## Features

- **AI-Powered Price Predictions**: XGBoost model trained on features like units sold, stock levels, competitor prices (Flipkart, Amazon), customer interactions (views, clicks, add-to-cart), and temporal factors (day of week, lags).
- **Interactive Dashboard**: Streamlit-based UI with sections for:
  - Sales & Demand trends (revenue, units sold, views).
  - Competitor price comparisons.
  - Price recommendations (increase/decrease/maintain based on predictions).
  - Customer behavior analysis (conversion funnel, bounce rate).
- **Daily Predictions**: Automated script to generate synthetic/historical data, predict prices, and store in PostgreSQL database.
- **Model Evaluation**: Comprehensive metrics (R², MAE, RMSE) to assess model performance and detect overfitting.
- **Data Handling**: Supports CSV datasets and PostgreSQL for scalable storage.

## Tech Stack

- **Languages**: Python 3.8+
- **ML Framework**: XGBoost for price prediction modeling.
- **Data Processing**: Pandas, NumPy.
- **Visualization**: Streamlit, Plotly (interactive charts).
- **Database**: PostgreSQL (for features and predictions).
- **Metrics**: Scikit-learn (R², MAE, RMSE).
- **Other**: psycopg2 (DB connectivity), joblib (model serialization).

## Project Structure

```
Dynamic_pricing_engine/
├── app/
│   └── app.py                  # Streamlit dashboard application
├── data/
│   ├── raw/                    # Raw CSV datasets (sales, competitors, customer behavior)
│   │   ├── competitor_prices_2024.csv
│   │   ├── customer_behavior_2024.csv
│   │   └── mobile_sales_2024.csv
│   └── preprocessing/          # Processed datasets
│       └── final_preprocessed_dataset.csv
├── model/                      # (Empty; for future model artifacts)
├── notebooks/                  # Jupyter notebooks for exploration
│   ├── datasets.ipynb          # Data loading and initial analysis
│   ├── preprocessing.ipynb     # Feature engineering and preprocessing
│   ├── final_preprocessed_dataset.csv  # Output from preprocessing
│   ├── xgb_price_model.json    # Trained XGBoost model (JSON format)
│   └── xgb_price_model.pkl     # Trained XGBoost model (Pickle format)
├── run_daily_prediction.py     # Script for daily data generation and price predictions
├── run_daily_prediction.bat    # Windows batch file to run predictions
├── evaluate_model.py           # Model evaluation script
├── temp_run.bat                # Temporary batch file (usage-specific)
└── TODO.md                     # Task tracking
```

## Prerequisites

- Python 3.8+ (with virtual environment recommended).
- PostgreSQL database (local or remote).
- Git (for version control).

## Setup Instructions

1. **Clone the Repository**:
   ```
   git clone https://github.com/hibaanwer07/Dynamic-Pricing-Engine.git
   cd Dynamic-Pricing-Engine
   ```

2. **Create Virtual Environment**:
   ```
   python -m venv .venv
   # Activate (Windows):
   .venv\Scripts\activate
   # Activate (macOS/Linux):
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   Create a `requirements.txt` file with the following content and install:
   ```
   pip install streamlit pandas numpy plotly psycopg2-binary xgboost scikit-learn joblib
   ```
   Or directly:
   ```
   pip install streamlit pandas numpy plotly psycopg2-binary xgboost scikit-learn joblib
   ```

4. **Database Setup**:
   - Install and start PostgreSQL.
   - Create a database named `pricing_engine`.
   - Update DB credentials in `run_daily_prediction.py` and `app/app.py` (host, port, user, password).
   - The prediction script will auto-create tables: `daily_features` and `predicted_prices`.

5. **Prepare Data**:
   - Raw data is in `data/raw/`. Run notebooks in `notebooks/` for preprocessing if needed.
   - The preprocessed dataset is available in `data/preprocessing/final_preprocessed_dataset.csv`.

## Usage

### 1. Run Daily Predictions
This script generates synthetic daily data for the last 30 days, computes features (including lags), predicts prices using the XGBoost model, and upserts into the database.

```
python run_daily_prediction.py
```

- Or use the batch file: `run_daily_prediction.bat`.
- Output: Features and predictions stored in PostgreSQL tables.
- Note: Uses hardcoded product list (Samsung, Redmi, etc.). Extend the `products` list as needed.

### 2. Evaluate the Model
Assess model performance on the preprocessed dataset.

```
python evaluate_model.py
```

- Loads `final_preprocessed_dataset.csv` and `xgb_price_model.pkl`.
- Computes train/test R², MAE, RMSE.
- Checks for overfitting.

### 3. Launch the Dashboard
View interactive visualizations of sales, competitors, recommendations, and customer behavior.

```
streamlit run app/app.py
```

- Access at `http://localhost:8501`.
- Login: Username `admin`, Password `admin123`.
- Requires database connection for data loading.
- Sidebar navigation for different dashboards.

### 4. Explore Notebooks
- `notebooks/datasets.ipynb`: Load and explore raw data.
- `notebooks/preprocessing.ipynb`: Feature engineering (lags, categoricals, etc.) and model training (outputs `xgb_price_model.*`).

## Model Details

- **Target**: Predict `price` for mobile products.
- **Features**: 28 features including categorical (brand, category), numerical (units_sold, stock), temporal (day_of_week, month), and lagged/rolling (price_lag1, competitor lags).
- **Training**: XGBoost Booster, trained on historical data up to 2024-09-30.
- **Evaluation**: Test set from 2024-10-01 onward. Typical metrics: R² ~0.85-0.95, low overfitting.

## Database Schema

- **daily_features**: Daily product features (date, product_id, units_sold, competitor prices, lags, etc.).
- **predicted_prices**: Predicted prices per product/date.

## Notes

- **Synthetic Data**: The prediction script uses random data generation for demonstration. Replace with real data ingestion in production.
- **Security**: Hardcoded DB credentials and simple login—update for production (use environment variables, proper auth).
- **Scalability**: For large datasets, optimize DB queries and consider cloud DB (e.g., AWS RDS).
- **Extensions**: Add more products, real-time data feeds, A/B testing for price changes.
- **License**: MIT (or specify as needed).

## Contributors

Hibaanwer

Gabriel ps




---

© 2024 Dynamic Pricing Engine. Built  using Python and ML.
