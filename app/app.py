import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2

st.set_page_config(
    page_title="Dynamic Pricing Engine",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Global CSS for Professional Theme ---
st.markdown("""
<style>
    /* Dark theme background */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
        color: #ffffff;
    }
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background: #16213e !important;
        border-right: 2px solid #0f3460;
    }
    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        border: 1px solid #0f3460;
    }
    .metric-value {
        font-size: 2em;
        font-weight: bold;
        color: #00d4ff;
    }
    .metric-label {
        font-size: 1em;
        color: #b0b0b0;
    }
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0099cc 0%, #0077aa 100%);
    }
    /* Selectbox and inputs */
    .stSelectbox, .stTextInput, .stNumberInput {
        background: #16213e;
        border: 1px solid #0f3460;
        border-radius: 5px;
        color: white;
    }
    /* Titles */
    h1, h2, h3 {
        color: #00d4ff;
        font-family: 'Arial', sans-serif;
    }
    /* Dataframe */
    .dataframe {
        background: #16213e;
        color: white;
    }
    /* Footer */
    .footer {
        text-align: center;
        padding: 10px;
        background: #0f0f23;
        color: #b0b0b0;
        border-top: 1px solid #0f3460;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# --- Enhanced Login Page ---
def login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 50px; background: linear-gradient(135deg, #0f3460 0%, #16213e 100%); border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.4);">
            <h1 style="color: #00d4ff; font-size: 3em;">🔐</h1>
            <h2 style="color: #ffffff;">Dynamic Pricing Engine</h2>
            <p style="color: #b0b0b0;">Secure Access Portal</p>
        </div>
        """, unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        login_btn = st.button("Login", use_container_width=True)

        if login_btn:
            if username == "admin" and password == "admin123":
                st.session_state["logged_in"] = True
                st.success("Login successful!")
                st.balloons()
            else:
                st.error("Invalid username or password. Please try again.")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# --- Load Data from DB ---
@st.cache_data
def load_data():
    conn = psycopg2.connect(
        dbname="pricing_engine",
        user="postgres",
        password="hiba0702",
        host="localhost",
        port="5432"
    )
    features = pd.read_sql("SELECT * FROM daily_features", conn)
    predicted = pd.read_sql("SELECT * FROM predicted_prices", conn)
    conn.close()

    features["product_id"] = features["product_id"].astype(str)
    predicted["product_id"] = predicted["product_id"].astype(str)
    features["date"] = pd.to_datetime(features["date"])
    predicted["date"] = pd.to_datetime(predicted["date"])

    sales_data = pd.merge(
        features,
        predicted,
        on=["product_id", "date"],
        how="left"
    )
    return sales_data

sales_data = load_data()
products = sales_data["product_id"].unique() if "product_id" in sales_data.columns else []

# --- Sidebar Navigation ---
st.sidebar.markdown(
    "<h2 style='color:#FFFFFF;'>📊 Dynamic Pricing Engine</h2>",
    unsafe_allow_html=True
)
dashboard = st.sidebar.radio(
    "Select Dashboard",
    [
        "Sales & Demand",
        "Competitor Price Comparison",
        "Price Recommendations",
        "Customer Behavior"
    ],
    index=0,
    label_visibility="visible"
)
# Remove blue color, keep white letters for radio options
st.sidebar.markdown(
    """
    <style>
    .stRadio > div > label {
        color: #FFFFFF !important;
        font-weight: bold;
        font-size: 16px;
        background: transparent;
        padding: 6px 12px;
        border-radius: 6px;
        margin-bottom: 4px;
        box-shadow: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Logout button
if st.sidebar.button("Logout", key="logout_btn"):
    st.session_state["logged_in"] = False
    st.experimental_rerun()

# --- 1️⃣ Sales & Demand Dashboard ---
if dashboard == "Sales & Demand":
    st.title("📈 Sales & Demand Dashboard")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_revenue = sales_data["revenue"].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">₹{total_revenue:,.0f}</div>
            <div class="metric-label">Total Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        avg_units = sales_data["units_sold"].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_units:.1f}</div>
            <div class="metric-label">Avg Units Sold</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        total_views = sales_data["views"].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_views:,.0f}</div>
            <div class="metric-label">Total Views</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        total_purchases = sales_data["purchases"].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_purchases:,.0f}</div>
            <div class="metric-label">Total Purchases</div>
        </div>
        """, unsafe_allow_html=True)

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        date_range = st.date_input("Select Date Range", [sales_data["date"].min(), sales_data["date"].max()])
    with col2:
        selected_products = st.multiselect("Select Products", products, default=products[:3])

    # Handle single date selection
    if len(date_range) == 1:
        start_date_filter = pd.to_datetime(date_range[0])
        end_date_filter = pd.to_datetime(date_range[0])
    else:
        start_date_filter = pd.to_datetime(date_range[0])
        end_date_filter = pd.to_datetime(date_range[1])

    filtered_data = sales_data[
        (sales_data["date"] >= start_date_filter) &
        (sales_data["date"] <= end_date_filter) &
        (sales_data["product_id"].isin(selected_products))
    ]

    # Charts
    st.markdown("#### Sales Trends")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for prod in selected_products:
        prod_data = filtered_data[filtered_data["product_id"] == prod]
        fig.add_trace(go.Scatter(x=prod_data["date"], y=prod_data["units_sold"], name=f"Units - {prod}", mode='lines'), secondary_y=False)
        fig.add_trace(go.Bar(x=prod_data["date"], y=prod_data["revenue"], name=f"Revenue - {prod}", opacity=0.6), secondary_y=True)
    fig.update_layout(title="Units Sold & Revenue Trends", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Product Performance Heatmap")
    perf_df = filtered_data.groupby("product_id").agg({"units_sold": "mean", "revenue": "mean", "views": "mean"}).reset_index()
    perf_melt = perf_df.melt(id_vars="product_id", var_name="Metric", value_name="Value")
    fig_heat = px.bar(perf_melt, x="product_id", y="Value", color="Metric", barmode="group", title="Product Performance Metrics")
    st.plotly_chart(fig_heat, use_container_width=True)

# --- 2️⃣ Competitor Price Comparison Dashboard ---
elif dashboard == "Competitor Price Comparison":
    st.title("💸 Competitor Price Comparison Dashboard")
    st.markdown("#### Compare Our Price vs Flipkart, Amazon, Myntra")

    if all(col in sales_data.columns for col in ["product_id", "flipkart_price", "amazon_price", "myntra_price"]):
        comp_df = sales_data[["product_id", "flipkart_price", "amazon_price", "myntra_price"]].drop_duplicates()
        comp_melt = comp_df.melt(id_vars="product_id", var_name="Platform", value_name="Price")
        fig_comp = px.bar(
            comp_melt,
            x="product_id", y="Price", color="Platform", barmode="group",
            title="Price Comparison Across Platforms"
        )
        st.plotly_chart(fig_comp, use_container_width=True)

        comp_df["Avg Competitor"] = comp_df[["flipkart_price", "amazon_price", "myntra_price"]].mean(axis=1)
        if "price" in sales_data.columns:
            own_price = sales_data.groupby("product_id")["price"].mean()
            comp_df["Our Price"] = comp_df["product_id"].map(own_price)
            comp_df["Price Diff"] = comp_df["Our Price"] - comp_df["Avg Competitor"]
            too_high = comp_df[comp_df["Price Diff"] > 1000]["product_id"].tolist()
            too_low = comp_df[comp_df["Price Diff"] < -1000]["product_id"].tolist()
            if too_high:
                st.warning(f"Our price is too high for: {', '.join(str(i) for i in too_high)}")
            if too_low:
                st.success(f"Our price is lower than competitors for: {', '.join(str(i) for i in too_low)}")
    else:
        st.info("Competitor data not available or columns missing.")

# --- 3️⃣ Price Recommendations Dashboard ---
elif dashboard == "Price Recommendations":
    st.title("💡 Price Recommendations Dashboard")
    st.markdown("#### AI-Powered Pricing Suggestions")

    if "predicted_price" in sales_data.columns:
        rec_df = sales_data.groupby("product_id").agg({
            "predicted_price": "mean",
            "flipkart_price": "mean",
            "amazon_price": "mean",
            "myntra_price": "mean",
            "units_sold": "mean",
            "stock": "mean"
        }).reset_index()

        rec_df["Avg Competitor Price"] = rec_df[["flipkart_price", "amazon_price", "myntra_price"]].mean(axis=1)
        rec_df["Recommendation"] = rec_df.apply(
            lambda row: "Increase Price" if row["predicted_price"] > row["Avg Competitor Price"] * 1.05 and row["units_sold"] > 10 else
                        "Decrease Price" if row["predicted_price"] < row["Avg Competitor Price"] * 0.95 else
                        "Maintain Price", axis=1
        )

        st.dataframe(rec_df[["product_id", "predicted_price", "Avg Competitor Price", "Recommendation"]])

        # Visualization
        fig_rec = px.scatter(
            rec_df, x="Avg Competitor Price", y="predicted_price", color="Recommendation",
            size="units_sold", hover_data=["product_id"], title="Price Recommendations Scatter Plot"
        )
        st.plotly_chart(fig_rec, use_container_width=True)

        # Alerts
        high_stock = rec_df[rec_df["stock"] > 100]["product_id"].tolist()
        if high_stock:
            st.warning(f"High stock products (consider discount): {', '.join(str(i) for i in high_stock)}")

        low_sales = rec_df[rec_df["units_sold"] < 5]["product_id"].tolist()
        if low_sales:
            st.error(f"Low sales products (review pricing): {', '.join(str(i) for i in low_sales)}")
    else:
        st.info("Predicted prices not available.")

# --- 4️⃣ Customer Behavior Dashboard ---
elif dashboard == "Customer Behavior":
    st.title("🛒 Customer Behavior Dashboard")
    st.markdown("#### Product Metrics")

    if "product_id" in sales_data.columns:
        st.dataframe(sales_data.set_index("product_id"))

        st.markdown("#### Conversion Funnel")
        funnel_stages = ["views", "clicks", "add_to_cart", "purchases"]
        funnel_counts = [sales_data[stage].sum() for stage in funnel_stages if stage in sales_data.columns]
        funnel_df = pd.DataFrame({"Stage": funnel_stages[:len(funnel_counts)], "Count": funnel_counts})

        funnel_fig = px.funnel(funnel_df, x="Stage", y="Count", title="Overall Conversion Funnel")
        st.plotly_chart(funnel_fig, use_container_width=True)

        if "views" in sales_data.columns and "clicks" in sales_data.columns:
            if sales_data["views"].sum() > 0:
                bounce_rate = 1 - (sales_data["clicks"].sum() / sales_data["views"].sum())
                st.metric("Bounce Rate", f"{bounce_rate*100:.2f}%")
            else:
                st.metric("Bounce Rate", "N/A")
    else:
        st.info("Behavior data not available.")

# --- Footer ---
st.markdown("""
<div class="footer">
    <p>© 2024 Dynamic Pricing Engine | Powered by AI & Machine Learning | Version 1.0</p>
</div>
""", unsafe_allow_html=True)
