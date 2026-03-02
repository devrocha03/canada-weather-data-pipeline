# 🍁 Canada Tech Hubs: Real-Time Weather Data Pipeline

🌎 [Read in English](README_EN.md) | 🇧🇷 [Ler em Português](README.md)

This project is an End-to-End Data Engineering and Analytics pipeline that extracts live weather data from major Canadian tech hubs (Toronto, Vancouver, Montreal, Calgary, and Ottawa) and displays it on an interactive Dashboard. The main goal was to handle dynamic JSON data and bypass security restrictions in modern cloud infrastructures.

## 📊 Final Dashboard (Streamlit)

<div align="center">
  <img src="dashboard_canada.png.png" width="1000">
</div>

## 🛠️ Architecture and Technologies
* **Data Source:** OpenWeatherMap API (REST API)
* **Processing (Cloud):** Databricks (Serverless Compute)
* **Languages:** Python (PySpark) and SQL
* **Storage:** Delta Lake (Medallion Architecture)
* **Data Visualization:** Streamlit (Databricks OAuth Connection)

## 🚀 The Data Pipeline (Medallion Architecture)

1. **Extraction & Bronze Layer (Raw Data - PySpark):**
   * HTTP requests to the OpenWeatherMap API.
   * *Technical Challenge:* In Databricks Serverless environments, writing local temporary files is blocked for security reasons. The workaround was to process the JSON 100% in-memory using PySpark's native `schema_of_json` and `from_json` functions to infer the structure dynamically.
   * Saved in Delta format using `append` mode to build historical data.

2. **Silver Layer (Cleansed - Pure SQL):**
   * Dot notation (`main.temp`) to unpack nested data (Structs).
   * Array indexing (`weather[0]`) to extract data from lists.
   * Data parsing and conversion of extraction time from Unix Epoch format to human-readable Timestamp.

3. **Gold Layer (Business View - Pure SQL):**
   * Implementation of **Window Functions** (`ROW_NUMBER() OVER(PARTITION BY... DESC)`) to filter and isolate only the most recent weather reading for each city. This ensures the Dashboard consumes only the "current snapshot", ignoring the historical stack.

4. **Web Application (Visual Interface):**
   * Dashboard built with Streamlit in Python.
   * Secure, direct connection to Databricks using **OAuth Authentication** (`databricks-sql-connector`), adapting to modern security requirements that block Personal Access Tokens (PAT) for external connections.
