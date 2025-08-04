# DLT Streaming ETL

This repository demonstrates a simple Delta Live Tables (DLT) pipeline on Databricks using a streaming ETL architecture. The pipeline reads order and customer data, enriches the stream, and organizes it into bronze, silver, and gold layers.

## 📁 Layers Overview

### 🔸 Bronze Layer
- **`order_stream`**: Ingests raw order data from a streaming source table.
- **`customer_mv`**: Reads customer master data as a materialized view.

### 🔹 Silver Layer
- **`silver_orders`**: Joins orders with customer data to enrich the stream.
- **`completed_orders`**: View for filtering completed orders.
- **`pending_orders`**: View for filtering pending orders.

### 🟡 Gold Layer
- **`fact_orders`**: Constructs a fact table with enriched order and date fields.
- **`completed_orders_fact`**: Gold table filtered to only completed orders.

## 🛠 Technologies Used
- Databricks Delta Live Tables (DLT)
- PySpark
- Structured Streaming

## 🚀 Getting Started

1. Clone the repo and deploy the notebook/script into a Databricks workspace.
2. Make sure the following source tables exist:
   - `dlt_demo.source.orders` (Streaming table)
   - `dlt_demo.source.customers` (Batch table)
3. Create and configure a DLT pipeline in Databricks UI.
4. Run the pipeline and observe the DAG building and real-time transformation.

## 📌 Notes
- This pipeline demonstrates the typical medallion architecture pattern.
- The code is intentionally simple to help you get started with DLT quickly.
