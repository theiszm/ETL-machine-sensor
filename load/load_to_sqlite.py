import sys
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from extract.extract_sensor_data import extract_sensor_data
from transform.transform_sensor_data import transform_sensor_data

DB_PATH = PROJECT_ROOT / "db" / "sensor_data.db"


def load_to_sqlite(df):
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS sensor_readings_clean (
        timestamp TEXT,
        machine_id TEXT,
        temperature_c REAL,
        vibration_mm_s REAL,
        pressure_kpa REAL,
        temp_avg_5min REAL,
        vibration_avg_5min REAL,
        condition_status TEXT,
        PRIMARY KEY (timestamp, machine_id)
    );
    """
    conn.execute(create_table_sql)

    df.to_sql(
        "sensor_readings_clean",
        conn,
        if_exists="replace",
        index=False
    )

    conn.commit()
    conn.close()

    print(f"[LOAD] Data loaded into {DB_PATH}")


if __name__ == "__main__":
    raw_df = extract_sensor_data()
    clean_df = transform_sensor_data(raw_df)
    load_to_sqlite(clean_df)
