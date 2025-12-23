import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data_raw" / "sensor_readings.csv"

def extract_sensor_data():
    
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Sensor data file not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    expected_columns = {
        "timestamp",
        "machine_id",
        "temperature_c",
        "vibration_mm_s",
        "pressure_kpa"
    }

    if not expected_columns.issubset(df.columns):
        missing = expected_columns - set(df.columns)
        raise ValueError(f"Missing expected columns: {missing}")

    print(f"[EXTRACT] Rows extracted: {len(df)}")

    return df


if __name__ == "__main__":
    df = extract_sensor_data()
    print(df.head())
