import dlt

# Products Exceptations 
products_rules = {
    "rule_1":"product_id IS NOT NULL",
    "rule_2": "price >= 0"
}

# ingesting products
@dlt.table(
    name="products_stg"
)
@dlt.expect_all_or_drop(products_rules)
def products_stg():

    df = spark.readStream.table("dltani.source.products")
    return df