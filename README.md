
# COVID-19 Data Dashboard with Forecasting and Trend Analysis

This project is a comprehensive COVID-19 data dashboard built with Streamlit. It provides real-time data visualizations, trend analysis, and forecasting for COVID-19 cases across different countries. Users can explore global and country-specific data, compare trends, and download forecast results.

## Features

- **Global Summary**: Overview of total cases, deaths, and vaccinations worldwide.
- **Country-Level Analysis**: View new and total cases, deaths, and vaccinations for any selected country.
- **Trend Analysis**: Options for 7-day moving averages and growth rates for COVID-19 cases and deaths.
- **Forecasting with Prophet**: Predicts future COVID-19 cases based on historical data.
- **Comparative Analysis**: Multi-country comparison of cases over time.
- **Healthcare and Economic Impact**: Insights into healthcare capacity, demographics, and GDP in relation to COVID-19.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/covid-dashboard.git
   cd covid-dashboard
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run covid_dashboard_with_forecasting.py
   ```

## Usage

1. **Select a country** from the dropdown menu for country-specific data.
2. **Choose Trend Analysis options** for 7-day moving average or growth rates.
3. **Set the Forecasting Period** to view future case predictions for the selected country.
4. **Download Forecast Results**: Use the provided download buttons to save forecast data and charts as CSV and PNG files.

## Project Structure

- `covid_dashboard_with_forecasting.py`: Main Streamlit application file.
- `covid_data.xlsx`: Data file containing COVID-19 statistics.
- `requirements.txt`: List of required Python packages.
- `.gitignore`: Specifies files and directories to ignore in the repository.

## Requirements

- Python 3.7+
- Libraries: Streamlit, Pandas, Matplotlib, Prophet, OpenPyXL

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any changes or improvements.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for providing a great platform for building interactive data apps.
- [Our World in Data](https://ourworldindata.org/coronavirus) for COVID-19 data.
