# ✈️ OpenSky Analytics Pipeline

End-to-end data pipeline that ingests real-time flight data from the OpenSky API, transforms it using dbt, and visualizes insights in Looker Studio.

---

## Project Overview

This project demonstrates a modern **Analytics Engineering workflow**:

- Extract real-time aviation data from an external API
- Load raw data into BigQuery
- Transform and model data using dbt (staging → marts)
- Build an interactive dashboard for analytics

---

##  Architecture
OpenSky API
    ↓
Python ingestion script (requests + pandas)
    ↓
BigQuery — raw layer (opensky_raw.opensky_data)
    ↓
dbt staging — stg_flights (clean, cast, rename)
    ↓
dbt marts — mart_flights_hourly / mart_flights_live
    ↓
Looker Studio Dashboard


---

## Tech Stack

- **Python** – API ingestion & data loading  
- **BigQuery** – Cloud data warehouse  
- **dbt** – Data transformation & modeling  
- **Looker Studio** – Data visualization  
- **GitHub** – Version control  

---

##  Data Pipeline

### 1. Ingestion (Python)
- Fetches live flight data from OpenSky API
- Cleans and formats data
- Loads into BigQuery raw table

### 2. Transformation (dbt)
- **Staging layer**
  - Clean columns
  - Cast data types
- **Marts layer**
  - Aggregations (flights per country, avg speed, etc.)

### 3. Visualization
- Interactive dashboard with:
  - Total active flights
  - Average speed & altitude
  - Flights by country
  - Flight activity by hour
  - Geographic flight distribution (heatmap)

---

## Dashboard Preview

https://datastudio.google.com/reporting/8631e01a-2343-40c0-9cf9-565eb9b5fb1d

---

##  Key Insights

- Air traffic is concentrated in North America and Europe  
- Peak flight activity occurs during afternoon hours  
- High-speed aircraft clusters are visible over dense regions  

---

##  How to Run DBT
```
pip install dbt-bigquery
dbt debug
dbt run
dbt test
```
### 1. Clone repo

```bash
git clone https://github.com/your-username/opensky-analytics-pipeline.git
cd opensky-analytics-pipeline
