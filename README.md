# ✈️ TravelLens

TravelLens is an end-to-end data engineering project built around 2015 flight data.

## 📌 Project Overview

The project processes raw flight data using Python, SQL, and DuckDB to build a simple data pipeline and generate useful flight insights.

The project covers:

- ✈️ Flight delays
- ❌ Flight cancellations
- 🏷️ Airline performance
- 🗺️ Busiest flight routes

## 🛠️ Technologies Used

- Python
- SQL
- DuckDB
- Apache Airflow
- Streamlit
- Plotly

## 🔄 Data Pipeline

CSV Dataset → Extract → Transform → Load → Analyze → Dashboard

## 📊 Dashboard

The Streamlit dashboard provides:

- Total flights explored
- Average arrival delay
- Cancelled flights
- Airline-wise delay analysis
- Airline-wise cancellation analysis
- Interactive airline filter
- Plotly visualizations

## 📁 Project Structure

```text
Travelens/
├── dags/
│   └── travellens_dag.py
├── data/
├── extract.py
├── app.py
├── requirements.txt
└── README.md
