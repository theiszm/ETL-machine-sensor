-- Count records
SELECT
  'Total sensor records loaded' AS metric,
  COUNT(*) AS value
FROM sensor_readings_clean;

-- High-confidence critical events per machine
SELECT
  machine_id AS machine,
  COUNT(*) AS critical_event_count
FROM sensor_readings_clean
WHERE condition_status = 'Critical'
GROUP BY machine_id
HAVING COUNT(*) >= 1;

-- Average vibration per machine
SELECT
  machine_id AS machine,
  ROUND(AVG(vibration_mm_s), 2) AS avg_vibration_mm_per_s
FROM sensor_readings_clean
GROUP BY machine_id;

-- Latest condition per machine
SELECT
  machine_id AS machine,
  MAX(timestamp) AS last_reading_time,
  condition_status AS current_status
FROM sensor_readings_clean
GROUP BY machine_id;

-- Results interpretation
SELECT
  machine_id AS machine,
  condition_status AS current_status,
  CASE
    WHEN condition_status = 'Critical' THEN 'Immediate inspection recommended'
    WHEN condition_status = 'Warning' THEN 'Monitor closely'
    ELSE 'Operating normally'
  END AS recommended_action
FROM sensor_readings_clean
GROUP BY machine_id;
