Dynamic Pricing Engine
Overview

The Dynamic Pricing Engine is a machine learning–driven system that automatically adjusts product prices based on demand, competitor prices, customer behavior, and seasonal events. It helps businesses stay competitive, maximize profit, and respond quickly to changing market conditions.

The engine uses sales data, customer activity, and real-world events (like Indian festivals) to suggest optimal prices. It integrates with PostgreSQL for storage, supports automation with Apache Airflow/Task Scheduler, and can be extended into a full API service for e-commerce platforms.

Features

Smart Price Predictions: Machine learning models (Linear Regression, Random Forest, XGBoost) for optimized pricing.

Competitor Tracking: Considers Amazon, Flipkart, and Myntra prices.

Customer Behavior Insights: Views, clicks, add-to-cart, bounce rate.

Festival & Season Aware: Price adjustments during Diwali, Holi, Eid, etc.

Automation: Daily predictions with Apache Airflow / Task Scheduler.

Database Integration: Saves predictions and features into PostgreSQL.

Dashboard Ready: Output designed for visualization in BI tools.

Project Structure
dynamic-pricing-engine/
├── data/                     # Raw and processed datasets
├── notebooks/                # Jupyter notebooks for exploration & modeling
├── src/                      # Source code modules
│   ├── preprocess.py          # Data cleaning and feature engineering
│   ├── train_model.py         # Model training script
│   ├── predict.py             # Generate price predictions
│   └── utils.py               # Helper functions
├── airflow_dags/             # DAGs for Airflow automation
├── reports/                  # Documentation, reports, presentations
├── config.py                 # Configuration settings (DB, paths)
├── main.py                   # Entry point for running predictions
├── requirements.txt           # Python dependencies
└── README.md                  # This file

Installation
Clone the Repository
git clone https://github.com/hibaanwer07/dynamic-pricing-engine.git
cd dynamic-pricing-engine

Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate      # On Mac/Linux
venv\Scripts\activate         # On Windows

Install Dependencies
pip install -r requirements.txt

Configure Database (PostgreSQL)

Create a .env file in the root directory:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=pricing_engine
DB_USER=your_username
DB_PASS=your_password

Running the Application
Preprocess Data
python src/preprocess.py

Train Model
python src/train_model.py

Predict Prices
python src/predict.py

Run with Scheduler (Daily Automation)

Windows: Use Task Scheduler to run main.py.

Linux/Mac: Use Cron jobs or Apache Airflow.

Configuration

Competitor Prices: Defined in dataset (amazon_price, flipkart_price, myntra_price).

Festival Days: Preloaded for 2024 (Diwali, Holi, Eid, etc.).

Database: PostgreSQL connection in config.py.

Automation: Airflow DAGs stored in airflow_dags/.

Contributing

Fork the repository.

Create a feature branch (git checkout -b feature/your-feature).

Commit changes (git commit -m 'Add new feature').

Push to your branch (git push origin feature/your-feature).

Open a Pull Request.

License

This project is licensed under the MIT License.

Acknowledgments

scikit-learn / XGBoost for machine learning models

PostgreSQL for data storage

Task Scheduler for workflow automation

pandas, NumPy, matplotlib for data handling and visualization
