import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="AI Carbon Footprint Calculator",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 AI-Powered Carbon Footprint Calculator")
st.subheader("Sustainability Advisor for Climate Action")

st.markdown("---")

# -------------------------------
# USER INPUTS
# -------------------------------

st.sidebar.header("Enter Your Lifestyle Data")

electricity = st.sidebar.number_input(
    "Monthly Electricity Consumption (kWh)",
    min_value=0.0,
    value=250.0
)

distance = st.sidebar.number_input(
    "Daily Travel Distance (km)",
    min_value=0.0,
    value=10.0
)

transport = st.sidebar.selectbox(
    "Mode of Transport",
    ["Car", "Bus", "Train", "Bike", "Walking"]
)

food = st.sidebar.selectbox(
    "Diet Type",
    ["Vegetarian", "Mixed Diet", "Heavy Meat Consumption"]
)

water = st.sidebar.number_input(
    "Daily Water Usage (Litres)",
    min_value=0.0,
    value=150.0
)

waste = st.sidebar.selectbox(
    "Waste Generation",
    ["Low", "Medium", "High"]
)

# -------------------------------
# EMISSION FACTORS
# -------------------------------

ELECTRICITY_FACTOR = 0.82

TRANSPORT_FACTORS = {
    "Car": 0.21,
    "Bus": 0.08,
    "Train": 0.04,
    "Bike": 0.02,
    "Walking": 0.0
}

FOOD_FACTORS = {
    "Vegetarian": 50,
    "Mixed Diet": 120,
    "Heavy Meat Consumption": 250
}

WASTE_FACTORS = {
    "Low": 10,
    "Medium": 25,
    "High": 50
}

WATER_FACTOR = 0.0003

# -------------------------------
# CALCULATIONS
# -------------------------------

electricity_emission = electricity * ELECTRICITY_FACTOR

transport_emission = (
    distance *
    30 *
    TRANSPORT_FACTORS[transport]
)

food_emission = FOOD_FACTORS[food]

water_emission = (
    water *
    30 *
    WATER_FACTOR
)

waste_emission = WASTE_FACTORS[waste]

monthly_total = (
    electricity_emission +
    transport_emission +
    food_emission +
    water_emission +
    waste_emission
)

annual_total = monthly_total * 12

# -------------------------------
# SUSTAINABILITY SCORE
# -------------------------------

score = max(
    0,
    min(
        100,
        100 - (monthly_total / 8)
    )
)

# -------------------------------
# IMPACT CATEGORY
# -------------------------------

if monthly_total < 200:
    category = "Low"
elif monthly_total < 400:
    category = "Moderate"
elif monthly_total < 700:
    category = "High"
else:
    category = "Very High"

# -------------------------------
# DASHBOARD METRICS
# -------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Monthly CO₂",
    f"{monthly_total:.2f} kg"
)

col2.metric(
    "Annual CO₂",
    f"{annual_total:.2f} kg"
)

col3.metric(
    "Sustainability Score",
    f"{score:.0f}/100"
)

col4.metric(
    "Impact Level",
    category
)

st.markdown("---")

# -------------------------------
# EMISSION BREAKDOWN
# -------------------------------

data = pd.DataFrame({
    "Source": [
        "Electricity",
        "Transport",
        "Food",
        "Water",
        "Waste"
    ],
    "Emission": [
        electricity_emission,
        transport_emission,
        food_emission,
        water_emission,
        waste_emission
    ]
})

colA, colB = st.columns(2)

with colA:

    pie_chart = px.pie(
        data,
        names="Source",
        values="Emission",
        title="Carbon Emission Distribution"
    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )

with colB:

    bar_chart = px.bar(
        data,
        x="Source",
        y="Emission",
        title="Emission Breakdown"
    )

    st.plotly_chart(
        bar_chart,
        use_container_width=True
    )

# -------------------------------
# AI RECOMMENDATIONS
# -------------------------------

st.markdown("---")
st.header("🤖 AI Sustainability Advisor")

recommendations = []

if electricity > 300:
    recommendations.append(
        "Reduce electricity consumption by using LED lighting and energy-efficient appliances."
    )

if transport == "Car":
    recommendations.append(
        "Switch to public transport or carpooling to reduce transportation emissions."
    )

if food == "Heavy Meat Consumption":
    recommendations.append(
        "Reduce red meat consumption and increase plant-based meals."
    )

if water > 200:
    recommendations.append(
        "Use water-saving fixtures and reduce unnecessary water usage."
    )

if waste == "High":
    recommendations.append(
        "Practice waste segregation and recycling."
    )

if not recommendations:
    recommendations.append(
        "Excellent! Your sustainability habits are already environmentally friendly."
    )

for rec in recommendations:
    st.success(rec)

# -------------------------------
# REDUCTION SIMULATOR
# -------------------------------

st.markdown("---")
st.header("📉 Carbon Reduction Simulator")

reduction = st.slider(
    "Reduce emissions by (%)",
    0,
    100,
    20
)

future_emission = monthly_total * (
    1 - reduction / 100
)

saved = monthly_total - future_emission

st.info(
    f"Potential Monthly Reduction: {saved:.2f} kg CO₂"
)

st.success(
    f"Projected Monthly Emission: {future_emission:.2f} kg CO₂"
)

# -------------------------------
# FOOTER
# -------------------------------

st.markdown("---")

st.caption(
    "Developed for 1M1B AI + Sustainability Internship | SDG 13 Climate Action"
)
