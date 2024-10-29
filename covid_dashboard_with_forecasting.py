import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from io import BytesIO

# Load and cache the dataset
@st.cache_data
def load_data():
    cols_needed = [
        "date", "location", "continent", "total_cases", "new_cases", "total_deaths", "new_deaths", 
        "people_vaccinated", "aged_65_older", "icu_patients", "hospital_beds_per_thousand", 
        "gdp_per_capita", "population"
    ]
    data = pd.read_excel("covid_data.xlsx", usecols=cols_needed)
    data['date'] = pd.to_datetime(data['date'])
    return data

data = load_data()

# Dashboard Title
st.title("Comprehensive COVID-19 Data Dashboard with Trend Analysis and Forecasting")

# Global Summary Section
st.header("🌍 Global Summary")
global_data = data.groupby('date').sum(numeric_only=True).reset_index()
st.metric("Total Cases Worldwide", f"{global_data['total_cases'].max():,.0f}")
st.metric("Total Deaths Worldwide", f"{global_data['total_deaths'].max():,.0f}")
st.metric("Total Vaccinations Worldwide", f"{global_data['people_vaccinated'].max():,.0f}")

# Date Range Selection with a narrower default range for performance
st.subheader("Select Date Range")
start_date, end_date = st.slider(
    "Date range",
    min_value=data['date'].min().date(),
    max_value=data['date'].max().date(),
    value=(data['date'].max().date() - pd.Timedelta(days=365), data['date'].max().date())
)
filtered_data = data[(data['date'] >= pd.to_datetime(start_date)) & (data['date'] <= pd.to_datetime(end_date))]

# Country Selection and Trend Analysis Option
st.header("📈 Country-Level Data and Trend Analysis")
countries = data['location'].unique()
selected_country = st.selectbox("Select a Country", countries)
country_data = filtered_data[filtered_data['location'] == selected_country]

# Trend Analysis Option
trend_option = st.selectbox("Select Trend Analysis", ["None", "7-Day Moving Average", "Growth Rate"])

# Apply Moving Average or Growth Rate Analysis
if trend_option == "7-Day Moving Average":
    country_data['new_cases_7day_avg'] = country_data['new_cases'].rolling(window=7).mean()
    country_data['new_deaths_7day_avg'] = country_data['new_deaths'].rolling(window=7).mean()
    st.line_chart(country_data.set_index('date')[['new_cases_7day_avg', 'new_deaths_7day_avg']])
elif trend_option == "Growth Rate":
    country_data['new_cases_growth_rate'] = country_data['new_cases'].pct_change().fillna(0) * 100
    country_data['new_deaths_growth_rate'] = country_data['new_deaths'].pct_change().fillna(0) * 100
    st.line_chart(country_data.set_index('date')[['new_cases_growth_rate', 'new_deaths_growth_rate']])

# Forecasting Section
st.header("📅 Forecasting COVID-19 Cases")
forecast_period = st.slider("Select Forecasting Period (Days)", 7, 90, 30)

# Prepare data for forecasting
forecast_data = country_data[['date', 'new_cases']].dropna()
forecast_data = forecast_data.rename(columns={"date": "ds", "new_cases": "y"})  # Prophet requires 'ds' and 'y'

# Fit the Prophet model
model = Prophet(daily_seasonality=True)
model.fit(forecast_data)

# Make future predictions
future = model.make_future_dataframe(periods=forecast_period)
forecast = model.predict(future)

# Plot the forecast and add a download button for forecast data
fig, ax = plt.subplots(figsize=(10, 6))
model.plot(forecast, ax=ax)
plt.title(f"COVID-19 Cases Forecast for {selected_country}")
plt.xlabel("Date")
plt.ylabel("Predicted New Cases")
st.pyplot(fig)

# Option to download forecast data as CSV
csv_forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(
    columns={'ds': 'Date', 'yhat': 'Predicted Cases', 'yhat_lower': 'Lower Bound', 'yhat_upper': 'Upper Bound'}
)
st.download_button(
    label="Download Forecast Data as CSV",
    data=csv_forecast.to_csv(index=False).encode('utf-8'),
    file_name=f"{selected_country}_covid_forecast.csv",
    mime="text/csv"
)

# Add forecast components and option to download as PNG
st.subheader("Forecast Components")
components_fig = model.plot_components(forecast)
st.pyplot(components_fig)

# Download forecast chart as PNG
img = BytesIO()
fig.savefig(img, format='png')
img.seek(0)
st.download_button(
    label="Download Forecast Chart as PNG",
    data=img,
    file_name=f"{selected_country}_forecast_chart.png",
    mime="image/png"
)

# Comparative Analysis: Multi-Country Selection
st.header("🌐 Compare Multiple Countries")
selected_countries = st.multiselect("Select Countries for Comparison", countries, default=["United States", "India", "Brazil"])
comparison_data = filtered_data[filtered_data['location'].isin(selected_countries)]

st.subheader("New Cases Comparison")
comparison_chart_data = comparison_data.pivot(index="date", columns="location", values="new_cases").fillna(0)
st.line_chart(comparison_chart_data)

st.subheader("Total Cases Comparison")
comparison_total_cases = comparison_data.pivot(index="date", columns="location", values="total_cases").fillna(0)
st.line_chart(comparison_total_cases)

# Insights on Excess Mortality and Testing Data
st.header("🔍 Additional Insights")

if 'excess_mortality' in data.columns:
    st.subheader("Excess Mortality Over Time")
    excess_data = filtered_data[filtered_data['location'] == selected_country]
    st.line_chart(excess_data.set_index('date')[['excess_mortality']])

if 'new_tests' in data.columns:
    st.subheader("Testing Trends")
    st.line_chart(country_data.set_index('date')[['new_tests']])
    st.metric("Total Tests Conducted", country_data['total_tests'].max())

# Age Demographics Impact
st.header("👶🧓 Age Demographics Impact")
if 'aged_65_older' in data.columns:
    st.subheader("COVID-19 Cases vs. Population Aged 65 and Older")
    age_impact_data = data.groupby('location').last()[['aged_65_older', 'total_cases']]
    st.scatter_chart(age_impact_data)

# Healthcare Capacity (ICU Patients, Hospital Beds)
st.header("🏥 Healthcare Capacity and COVID-19 Impact")
if 'icu_patients' in data.columns and 'hospital_beds_per_thousand' in data.columns:
    st.subheader("ICU Patients vs. COVID-19 Cases")
    icu_capacity_data = data.groupby('location').last()[['icu_patients', 'total_cases']]
    st.scatter_chart(icu_capacity_data)

    st.subheader("Hospital Beds per Thousand vs. COVID-19 Cases")
    beds_capacity_data = data.groupby('location').last()[['hospital_beds_per_thousand', 'total_cases']]
    st.scatter_chart(beds_capacity_data)

# GDP per Capita and COVID-19 Impact
st.header("💰 Economic Impact Analysis")
if 'gdp_per_capita' in data.columns:
    st.subheader("GDP per Capita vs. COVID-19 Cases")
    gdp_data = data.groupby('location').last()[['gdp_per_capita', 'total_cases']]
    st.scatter_chart(gdp_data)
    st.write("This section explores if wealthier countries faced different challenges during the pandemic.")
