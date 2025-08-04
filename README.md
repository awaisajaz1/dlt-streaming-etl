# Delta Live Tables Streaming ETL

This repository contains a Delta Live Tables (DLT) pipeline for processing streaming order data using the medallion architecture (Bronze → Silver → Gold). It demonstrates real-time ingestion, enrichment, and curation flows using append-only streaming tables.

---

## 📚 Architecture Overview

         +-------------------+
         | source.orders     | ← raw stream
         +-------------------+
                  |
            [Bronze Layer]
                  ↓
         +-------------------+
         | dlt.order_stream  |
         +-------------------+

         +-------------------+
         | dlt.customer_mv   |
         +-------------------+

            [Silver Layer]
                  ↓
         +-------------------+
         | dlt.silver_orders |
         +-------------------+
                  ↓
   +--------------------+--------------------+
   | dlt.pending_orders | dlt.completed_orders|
   +--------------------+--------------------+
                  ↓
     [Streaming Table: Append Flow]
                  ↓
      +-----------------------------+
      | dlt.filtered_orders_append  |
      +-----------------------------+

            [Gold Layer]
                  ↓
         +-----------------------------+
         | dlt.fact_orders            |
         | dlt.append_orders_stream   |
         +-----------------------------+


---

## 🏗️ Pipeline Components

### 🔸 Bronze Layer
- **order_stream**: Ingests streaming orders from a raw source.
- **customer_mv**: Materialized view of customer data (batch).

### ⚪ Silver Layer
- **silver_orders**: Joins orders with customer info.
- **pending_orders / completed_orders**: Views filtering based on `order_status`.
- **filtered_orders_append**: Streaming table for append-only writes.

### 🟡 Gold Layer
- **fact_orders**: Final curated fact table.
- **append_orders_stream**: Combines pending and completed order streams.

---

## ⚙️ Features

- ✅ Real-time ingestion with `dlt.read_stream`.
- ✅ Modular pipeline with `@dlt.view`, `@dlt.table`, and `@dlt.create_streaming_table`.
- ✅ Append-only logic using `dlt.append_flow` pattern.
- ✅ Auto compaction and optimization properties enabled.

---

## 📌 Notes

- Use `dlt.create_streaming_table(name="filtered_orders_append")` before defining append flows.
- `pending_orders` and `completed_orders` are logical views that append into `filtered_orders_append`.
- Designed for scalable streaming transformations on Databricks DLT.

---

## 🔧 To Do
- Add schema expectations and validations.
- Introduce dead-letter queues or quarantine for failed records.
- Add surrogate dimension support (customer, date, product).

