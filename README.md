# Machine Sensor ETL Pipeline

## Overview
This project implements an ETL (Extract, Transform, Load) pipeline for processing machine sensor data.
Raw sensor readings are extracted from CSV files, cleaned and validated using Python, and loaded into a MySQL database for analytics and monitoring.

## Data Description
The dataset contains time-series sensor readings collected from industrial machines, including:
- Timestamp
- Machine ID
- Temperature (°C)
- Vibration (mm/s)
- Pressure (kPa)

## ETL Architecture
1. Extract raw sensor data from CSV files
2. Transform data by cleaning, validating, and classifying operating conditions
3. Load processed data into a MySQL database for analysis

SQLite is used for local storage during development, with the pipeline designed to support migration to MySQL.

## Status
Project setup in progress.
