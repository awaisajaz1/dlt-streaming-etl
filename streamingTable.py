import dlt
from pyspark.sql import functions as F

# Bronze Layer: Raw streaming ingestion
@dlt.table(
    name="order_stream",
    comment="Streaming source table for new orders.",
    table_properties={"quality": "bronze"}
)
def order_stream():
    return spark.readStream.table("dlt_demo.source.orders")


@dlt.table(
    name="customer_mv",
    comment="Materialized view of customer data.",
    table_properties={"quality": "bronze"}
)
def customer_mv():
    return spark.read.table("dlt_demo.source.customers")


# Silver Layer: Enrichment and business logic
@dlt.table(
    name="silver_orders",
    comment="Orders enriched with customer information.",
    table_properties={"quality": "silver"}
)
def silver_orders():
    orders = dlt.read_stream("order_stream")
    customers = dlt.read("customer_mv")

    return (
        orders
        .join(customers, orders["order_customer_id"] == customers["customer_id"], "left")
        .select(
            orders["*"],
            customers["customer_name"]
        )
    )


@dlt.view(
    name="completed_orders",
    comment="Logical view filtering completed orders from silver layer."
)
def completed_orders():
    return dlt.read_stream("silver_orders").filter(F.col("order_status") == "COMPLETE")


@dlt.view(
    name="pending_orders",
    comment="Logical view filtering pending orders from silver layer."
)
def pending_orders():
    return dlt.read_stream("silver_orders").filter(F.col("order_status") == "PENDING")

# First, create the target streaming table
dlt.create_streaming_table(
    name="filtered_orders_append",
)

@dlt.append_flow(target="filtered_orders_append")
def pending_orders_append():
    return dlt.read_stream("pending_orders")


@dlt.append_flow(target="filtered_orders_append")
def completed_orders_append():
    return dlt.read_stream("completed_orders")


# Gold Layer: Fact table construction
@dlt.table(
    name="fact_orders",
    comment="Gold fact table containing enriched order data with date dimensions.",
    table_properties={"quality": "gold"}
)
def fact_orders():
    return (
        dlt.read_stream("silver_orders")
        .select(
            "order_id",
            "order_date",
            F.year("order_date").alias("order_year"),
            F.month("order_date").alias("order_month"),
            F.dayofmonth("order_date").alias("order_day"),
            "order_customer_id",
            "customer_name",
            "order_status"
        )
    )


@dlt.table(
    name="append_orders_stream",
    comment="Gold fact table for completed orders only.",
    table_properties={"quality": "gold"}
)
def append_orders_stream():
    return dlt.read("filtered_orders_append")
