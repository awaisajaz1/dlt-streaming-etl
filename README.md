# Delta Live Tables Streaming Pipeline (DLT)

This project demonstrates a full streaming ETL pipeline using **Databricks Delta Live Tables (DLT)** in the **medallion architecture** pattern.

## 🔁 Pipeline Overview

### 🟤 Bronze Layer
- **`order_stream`**: Ingests raw order data from `dlt_demo.source.orders` (streaming source).
- **`customer_mv`**: Loads customer master data from `dlt_demo.source.customers` (batch source).

### 🔹 Silver Layer
- **`silver_orders`**: Enriched order stream with customer information.
- **`completed_orders`**: View that filters orders where `order_status = 'COMPLETE'`.
- **`pending_orders`**: View that filters orders where `order_status = 'PENDING'`.
- **`append_orders_stream`**: Streaming append table that consolidates completed and pending orders.

### 🟡 Gold Layer
- **`fact_orders`**: Fact table with enriched fields and derived date dimensions.
- **`append_orders_stream`**: Also promoted to a gold table (dual use) for analytics.

## 🛠 Technologies Used

- **Databricks Delta Live Tables**
- **Structured Streaming**
- **PySpark**
- **Medallion Architecture** (Bronze → Silver → Gold)

## 📂 Table Summary

| Layer   | Table/View           | Type       | Description                                  |
|---------|----------------------|------------|----------------------------------------------|
| Bronze  | `order_stream`       | Table      | Raw order stream from source                 |
| Bronze  | `customer_mv`        | Table      | Materialized customer batch view             |
| Silver  | `silver_orders`      | Table      | Enriched order-customer join                 |
| Silver  | `completed_orders`   | View       | Filtered view for completed orders           |
| Silver  | `pending_orders`     | View       | Filtered view for pending orders             |
| Silver  | `append_orders_stream` | Streaming Table | Consolidated append-only orders       |
| Gold    | `fact_orders`        | Table      | Fact table with order + time dimensions      |
| Gold    | `append_orders_stream` | Table    | Reused as a gold layer streaming table       |

## 🚀 How to Run

1. Deploy the code into a Databricks notebook or a Python file.
2. Ensure the following **source tables** exist in `dlt_demo.source`:
   - `orders` (must be a streaming source)
   - `customers` (batch table)
3. Create a **Delta Live Tables pipeline** using the Databricks UI.
4. Point the pipeline to this script and run it.

## ✅ Features

- Enrichment joins between real-time and batch datasets
- Logical views for filtering status
- Append-only streaming table consolidation
- Gold layer fact table with time-dimension extraction

## 📌 Notes

- `append_orders_stream` is both a silver and gold layer component (dual usage).
- Optimizations like `delta.autoOptimize.optimizeWrite` and `autoCompact` are enabled on the streaming append table.

