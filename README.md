# dlt-streaming-etl

Simple Delta Live Tables (DLT) pipeline using streaming tables and views.

## Pipeline Structure

- **order_stream** → Bronze
- **silver_orders** → Silver
  - **pending_orders** (view)
  - **completed_orders** (view)
- **filtered_orders_append** → Streaming Silver (append-only)
- **append_orders_stream** → Final Streaming Tables

## Highlights

- Uses `@dlt.create_streaming_table` for append-only logic
- Views are created with `@dlt.view` (not materialized)
- Auto-optimize and auto-compact enabled
- No CDC, no joins, just clean streaming flow
