-- Count records
SELECT COUNT(*) FROM sensor_readings_clean;

-- High-confidence critical events per machine
SELECT
  machine_id,
  COUNT(*) AS critical_events
FROM sensor_readings_clean
WHERE condition_status = 'Critical'
GROUP BY machine_id
HAVING COUNT(*) >= 1;

-- Average vibration per machine
SELECT
  machine_id,
  ROUND(AVG(vibration_mm_s), 2) AS avg_vibration
FROM sensor_readings_clean
GROUP BY machine_id;

-- Latest condition per machine
SELECT
  machine_id,
  MAX(timestamp) AS latest_reading,
  condition_status
FROM sensor_readings_clean
GROUP BY machine_id;
