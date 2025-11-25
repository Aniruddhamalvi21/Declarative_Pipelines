import dlt

# Sales Ecpectations

sales_rules = {
    "rule_1" : "sales_id IS NOT NULL"
}

# Empty Streaming Table
dlt.create_streaming_table(
    name="sales_stg",
    expect_all_or_drop =sales_rules
)

# creating east_sales_flow

@dlt.append_flow(target="sales_stg")
def east_sales():

    df = spark.readStream.table("dltani.source.sales_east")
    return df

# creating west_sales_flow

@dlt.append_flow(target="sales_stg")
def west_sales():

    df = spark.readStream.table("dltani.source.sales_west")
    return df

