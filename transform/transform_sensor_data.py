import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REJECTED_PATH = PROJECT_ROOT / "transform" / "rejected_rows.csv"


# Strict engineering thresholds
TEMP_NORMAL_MAX = 70.0
TEMP_WARNING_MAX = 85.0

VIB_NORMAL_MAX = 4.5
VIB_WARNING_MAX = 7.1

PRESSURE_MIN_NORMAL = 120.0
PRESSURE_MAX_NORMAL = 250.0
PRESSURE_MIN_WARNING = 100.0
PRESSURE_MAX_WARNING = 280.0


def classify_condition(row):
    """
    Strict condition classification:
    - Critical if ANY parameter is critical
    - Warning if ANY parameter is warning
    - Otherwise Normal
    """

    # Critical conditions
    if (
        row["temperature_c"] > TEMP_WARNING_MAX
        or row["vibration_mm_s"] > VIB_WARNING_MAX
        or row["pressure_kpa"] < PRESSURE_MIN_WARNING
        or row["pressure_kpa"] > PRESSURE_MAX_WARNING
    ):
        return "Critical"

    # Warning conditions
    if (
        row["temperature_c"] > TEMP_NORMAL_MAX
        or row["vibration_mm_s"] > VIB_NORMAL_MAX
        or row["pressure_kpa"] < PRESSURE_MIN_NORMAL
        or row["pressure_kpa"] > PRESSURE_MAX_NORMAL
    ):
        return "Warning"

    return "Normal"


def transform_sensor_data(df: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamps
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Drop rows with invalid timestamps or machine_id
    invalid_mask = df["timestamp"].isna() | df["machine_id"].isna()
    rejected = df[invalid_mask]

    df = df[~invalid_mask]

    # Physical plausibility filters
    physical_mask = (
        (df["temperature_c"].between(-40, 200)) &
        (df["vibration_mm_s"] >= 0) &
        (df["pressure_kpa"] > 0)
    )

    rejected = pd.concat([rejected, df[~physical_mask]])
    df = df[physical_mask]

    # Remove duplicates (instrumentation-grade rule)
    df = df.drop_duplicates(subset=["timestamp", "machine_id"])

    # Sort for rolling calculations
    df = df.sort_values(["machine_id", "timestamp"])

    # Rolling averages (5-minute window per machine)
    df["temp_avg_5min"] = (
        df.groupby("machine_id")
          .rolling("5min", on="timestamp")["temperature_c"]
          .mean()
          .reset_index(drop=True)
    )

    df["vibration_avg_5min"] = (
        df.groupby("machine_id")
          .rolling("5min", on="timestamp")["vibration_mm_s"]
          .mean()
          .reset_index(drop=True)
    )

    # Condition classification
    df["condition_status"] = df.apply(classify_condition, axis=1)

    # Save rejected rows (for auditability)
    if not rejected.empty:
        rejected.to_csv(REJECTED_PATH, index=False)
        print(f"[TRANSFORM] Rejected rows saved to {REJECTED_PATH}")

    print(f"[TRANSFORM] Clean rows: {len(df)}")

    return df


if __name__ == "__main__":
    # Manual test hook
    from extract.extract_sensor_data import extract_sensor_data

    raw_df = extract_sensor_data()
    clean_df = transform_sensor_data(raw_df)

    print(clean_df[[
        "timestamp",
        "machine_id",
        "temperature_c",
        "vibration_mm_s",
        "pressure_kpa",
        "condition_status"
    ]])
