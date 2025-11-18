import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Page Config
st.set_page_config(
    page_title="Supply Chain Command Center",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Supply Chain Command Center")
st.markdown("Executive dashboard for monitoring supply chain health and performance.")

# Mock Data Generation (Replace with real data loading)
@st.cache_data
def load_mock_data():
    dates = pd.date_range(start="2024-01-01", periods=90, freq="D")
    df = pd.DataFrame({
        "Date": dates,
        "Actual_Demand": np.random.randint(100, 200, size=90),
        "Forecast_Demand": np.random.randint(100, 200, size=90) * 1.05, # Slight bias for demo
        "Inventory_Level": np.random.randint(50, 300, size=90)
    })
    return df

data = load_mock_data()

# KPI Section
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Service Level", value="98.5%", delta="1.2%")
with col2:
    st.metric(label="Inventory Turnover", value="4.2", delta="-0.1")
with col3:
    st.metric(label="Forecast Accuracy (MAPE)", value="85%", delta="2.5%")
with col4:
    st.metric(label="Stockout Risk", value="Low", delta="Stable", delta_color="off")

st.divider()

# Charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Demand vs. Forecast")
    fig_demand = px.line(data, x="Date", y=["Actual_Demand", "Forecast_Demand"], 
                         title="Daily Demand Tracking",
                         labels={"value": "Units", "variable": "Metric"},
                         color_discrete_map={"Actual_Demand": "blue", "Forecast_Demand": "orange"})
    st.plotly_chart(fig_demand, use_container_width=True)

with col_right:
    st.subheader("Inventory Levels")
    fig_inv = px.area(data, x="Date", y="Inventory_Level", 
                      title="Inventory Position Over Time",
                      labels={"Inventory_Level": "Units"},
                      color_discrete_sequence=["green"])
    st.plotly_chart(fig_inv, use_container_width=True)

# Detailed Data View
with st.expander("View Detailed Data"):
    st.dataframe(data, use_container_width=True)

st.info("🚀 This dashboard is a template. Connect it to your data sources (CSV, SQL, API) to get started.")
