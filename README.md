🛠 Databricks Delta Live Tables (DLT) – End-to-End Data Pipeline

This repository contains a complete Delta Live Tables (DLT) pipeline built on Databricks to process real-time streaming datasets for Sales, Customers, and Products.
The pipeline covers Bronze → Silver → Gold data architecture with CDC (Change Data Capture) and business-level aggregation.

📌 Architecture Overview
Layer	Purpose	Technologies Used
Bronze (Staging)	Ingest raw streaming data with data quality rules	@dlt.table, @dlt.expect_all_or_drop, incremental loads
Silver (Enriched)	Data transformations, SCD Type 1 & Type 2 CDC	@dlt.view, dlt.create_streaming_table, dlt.create_auto_cdc_flow
Gold (Business Layer)	Aggregated business KPIs for analytics	Join Fact and Dimensions, grouping, aggregations
📂 Datasets

The pipeline processes 3 datasets deployed as streaming source tables:

Dataset	Example Source Tables
Sales	sales_east, sales_west
Customers	customers
Products	products

Each dataset supports initial load + incremental load / SCD updates.

🚀 Pipeline Flow
🟫 Bronze Layer
    ├── customers_stg
    ├── products_stg
    ├── sales_stg (east + west append flows)
⬇
⬇
⬨ Automated CDC → SCD1 & SCD2
⬇
⬇
⬦ Silver Layer
    ├── customers_enr
    ├── products_enr
    ├── sales_enr
⬇
⬇
✨ Gold Layer
    ├── fact_sales
    ├── dim_customers
    ├── dim_products
    ├── business_sales 📊 (regional & category-wise sales KPI)

✔ Key Features

🔹 Real-time streaming ingestion
🔹 Expectations enforcement (drop bad records)
🔹 Auto CDC for SCD Type 1 & Type 2
🔹 Merge fact + dimensions for Gold layer output
🔹 Fully declarative DLT pipeline

📑 Explanation of Major Components
1️⃣ Bronze — Ingestion & Validation
@dlt.table(name="customers_stg")
@dlt.expect_all_or_drop({"rule_1": "customer_id IS NOT NULL",
                         "rule_2": "customer_name IS NOT NULL"})


Records failing validation are dropped.

Sales ingestion merges two streaming sources:

@dlt.append_flow(target="sales_stg")
def east_sales(): ...
@dlt.append_flow(target="sales_stg")
def west_sales(): ...

2️⃣ Silver — Enrichment + CDC

Example Silver transformation:

@dlt.view(name="sales_enr_view")
df = df.withColumn("total_amount", col("quantity") * col("amount"))


CDC to build up-to-date dimension tables:

dlt.create_auto_cdc_flow(
    target="dim_products",
    source="products_enr_view",
    keys={"product_id"},
    stored_as_scd_type=2
)

3️⃣ Gold — Business Metrics

Aggregation by region and category:

groupBy("region", "category")
  .agg(sum("total_amount").alias("total_sales"))


Result table: business_sales

▶ How to Run This Pipeline

Open Databricks → Delta Live Tables Pipelines

Create New Pipeline → Select Python Notebook

Paste the full code from this repository

Configure:

Continuous Mode: Enabled

Target Schema = <your_catalog>.<schema>

Click Start

📊 Sample Analytical Output
Region	Category	Total Sales
East	Electronics	1,200.00
West	Furniture	980.00
Central	Stationery	150.00
🧱 Future Enhancements (Optional)

Add Unity Catalog lineage + monitoring

Add Auto Loader ingestion layer

Publish Gold table to Power BI / Tableau

Add ML features – customer segmentation

Below is an architecture diagram ready for your README.

                ┌─────────────────────────┐
                │     Source Systems      │
                │ sales_east / sales_west │
                │  customers / products   │
                └────────────┬────────────┘
                             │ (Streaming)
                             ▼
               ┌────────────────────────────┐
               │        BRONZE Layer         │
               │  ▸ customers_stg            │
               │  ▸ products_stg             │
               │  ▸ sales_stg                │
               │  (Expectations + Validation)│
               └────────────┬───────────────┘
                             ▼
               ┌────────────────────────────┐
               │        SILVER Layer         │
               │  ▸ customers_enr (CDC SCD2) │
               │  ▸ products_enr (CDC SCD2)  │
               │  ▸ sales_enr (CDC SCD1)     │
               │  (Business Transformations) │
               └────────────┬────────────────┘
                             ▼
               ┌────────────────────────────┐
               │         GOLD Layer          │
               │  ▸ dim_customers            │
               │  ▸ dim_products             │
               │  ▸ fact_sales               │
               │  ▸ business_sales (KPIs)    │
               │  (Analytics + BI Ready)     │
               └────────────────────────────┘

🙌 Contribution

Pull requests and fork improvements are welcome!
If you'd like to collaborate on scaling this DLT solution for enterprise workloads, feel free to reach out.

⭐ If this repository helped you, don’t forget to star it!
