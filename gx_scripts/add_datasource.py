# file: add_datasource.py
import great_expectations as gx

# 1. สร้าง Data Context
context = gx.get_context()

# 2. กำหนดค่าการเชื่อมต่อ
PG_CONNECTION_STRING = "postgresql+psycopg2://dpuser:dppass@dp_postgres:5432/dp_course"

# 3. เพิ่มหรืออัปเดต Datasource
datasource = context.sources.add_or_update_postgres(
    name="pg_datasource", connection_string=PG_CONNECTION_STRING
)

# 4. เพิ่ม Table Asset สำหรับ Staging
datasource.add_table_asset(
    name="stg_supply_chain_asset", 
    schema_name="staging", 
    table_name="datacosupplychaindataset_tmp"
)

# # --- เพิ่ม: Asset สำหรับตารางใน Analytics Schema ---
# print("Adding assets for Analytics schema...")

# # Asset สำหรับตาราง Fact
datasource.add_table_asset(
    name="fct_sales_items",
    schema_name="mart_mart", 
    table_name="fct_sales_items"
)

#     (เพิ่ม) ตาราง Fact ที่ 2 ที่ขาดไป
datasource.add_table_asset(
    name="fct_shipping_orders",      # <-- เพิ่มใหม่
    schema_name="mart_mart", 
    table_name="fct_shipping_orders" # <-- เพิ่มใหม่
)

# # Asset สำหรับตาราง Dimension ทั้งหมด
datasource.add_table_asset(name="dim_customer", schema_name="mart_mart", table_name="dim_Customer")
datasource.add_table_asset(name="dim_product", schema_name="mart_mart", table_name="dim_Product")
datasource.add_table_asset(name="dim_location", schema_name="mart_mart", table_name="dim_Location")
datasource.add_table_asset(name="dim_shipping_mode", schema_name="mart_mart", table_name="dim_ShippingMode")
datasource.add_table_asset(name="dim_order_status", schema_name="mart_mart", table_name="dim_OrderStatus")
datasource.add_table_asset(name="dim_delivery_status", schema_name="mart_mart", table_name="dim_DeliveryStatus")
datasource.add_table_asset(name="dim_date", schema_name="mart_mart", table_name="dim_Date")


print("✅ Datasource and all assets are ready.")