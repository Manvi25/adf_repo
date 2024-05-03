# Databricks notebook source
# MAGIC %run /Workspace/Users/manvi.khandelwal2022@vitstudent.ac.in/customer_file

# COMMAND ----------

from pyspark.sql.functions import col

# COMMAND ----------

product_path = 'dbfs:/mnt/silver/sales_view/product'
store_path = 'dbfs:/mnt/silver/sales_view/store'


# COMMAND ----------

product_df = read_delta_file(product_path)
store_df = read_delta_file(store_path)

# COMMAND ----------


merged_product_store_df = product_df.join(store_df, product_df.store_id == store_df.store_id, "inner")
product_store_df = merged_product_store_df.select(store_df.store_id,"store_name","location","manager_name","product_id","product_name","product_code","description","category_id","price","stock_quantity","supplier_id",product_df.created_at.alias("product_created_at"),product_df.updated_at.alias("product_updated_at"),"image_url","weight","expiry_date","is_active","tax_rate")


# COMMAND ----------

customer_sales_path = "dbfs:/mnt/silver/sales_view/customer_sales"
customer_sales_df = read_delta_file(customer_sales_path)

# COMMAND ----------

merged_prodcust_custsale_df = product_store_df.join(customer_sales_df, product_store_df.product_id == customer_sales_df.product_id, "inner")
final_df = merged_prodcust_custsale_df.select("OrderDate","Category","City","CustomerID","OrderID",product_df.product_id.alias('ProductID'),"Profit","Region","Sales","Segment","ShipDate","ShipMode","latitude","longitude","store_name","location","manager_name","product_name","price","stock_quantity","image_url")


# COMMAND ----------

dbutils.fs.mount(
    source= 'wasbs://gold@storagemanvi.blob.core.windows.net/',
    mount_point = '/mnt/gold',
    extra_configs = {'fs.azure.account.key.storagemanvi.blob.core.windows.net':'xKuYBEvv3wZzSQ4JW7822vtOY7K2cjgOeCBRaNeIgAerDrpYUUtAyc0RZV6rd9Cl06D7n1WbolBA+ASti9NglQ=='}
)

# COMMAND ----------

def write_delta_upsert(df, delta_path):
    df.write.format("delta").mode("overwrite").save(delta_path)

# COMMAND ----------


writeTo = "dbfs:/mnt/gold/sales_view/StoreProductSales"
write_delta_upsert(final_df,writeTo)

