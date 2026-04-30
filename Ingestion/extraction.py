import requests
import pandas as pd
from google.cloud import bigquery
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
# -----------------------------
# CONFIG
# -----------------------------
OPEN_SKY_URL = "https://opensky-network.org/api/states/all"

PROJECT_ID = os.getenv("PROJECT_ID")
DATASET = os.getenv("DATASET")
TABLE = "opensky_data"

TABLE_ID = f"{PROJECT_ID}.{DATASET}.{TABLE}"

# ⚠️ IMPORTANT: service account JSON path
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


# -----------------------------
# FETCH DATA FROM API
# -----------------------------
def fetch_opensky_data():
    response = requests.get(OPEN_SKY_URL)

    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code}")

    data = response.json()
    return data.get("states", [])


# -----------------------------
# TRANSFORM DATA (CLEAN FOR BIGQUERY)
# -----------------------------
def transform_data(states):
    columns = [
        "icao24", "callsign", "origin_country", "time_position",
        "last_contact", "longitude", "latitude", "baro_altitude",
        "on_ground", "velocity", "true_track", "vertical_rate",
        "sensors", "geo_altitude", "squawk", "spi", "position_source"
    ]

    df = pd.DataFrame(states, columns=columns)

    #  drop problematic nested column
    if "sensors" in df.columns:
        df = df.drop(columns=["sensors"])

    #  convert numeric columns safely
    numeric_cols = [
        "time_position", "last_contact", "longitude", "latitude",
        "baro_altitude", "velocity", "true_track",
        "vertical_rate", "geo_altitude"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    #  convert strings safely
    df["icao24"] = df["icao24"].astype("string")
    df["callsign"] = df["callsign"].astype("string")
    df["origin_country"] = df["origin_country"].astype("string")

    # Add ingestion timestamp
    df["ingested_at"] = datetime.utcnow()

    return df


# -----------------------------
# LOAD TO BIGQUERY
# -----------------------------
def load_to_bigquery(df):
    client = bigquery.Client.from_service_account_json(CREDENTIALS_PATH)

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND"  # append data instead of overwrite
    )

    job = client.load_table_from_dataframe(
        df,
        TABLE_ID,
        job_config=job_config
    )

    job.result()

    print(f"✅ Loaded {len(df)} rows into {TABLE_ID}")


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def main():
    print("Fetching OpenSky data...")
    states = fetch_opensky_data()

    print("Transforming data...")
    df = transform_data(states)

    print("Loading into BigQuery...")
    load_to_bigquery(df)

    print("Done!")


# -----------------------------
# RUN SCRIPT
# -----------------------------
if __name__ == "__main__":
    main()
