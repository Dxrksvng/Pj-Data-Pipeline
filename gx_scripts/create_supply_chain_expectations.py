import great_expectations as gx
from datetime import date

# 1. สร้าง Data Context
context = gx.get_context()

# 2. ดึง Datasource และ Asset ที่มีอยู่แล้ว
datasource = context.datasources["pg_datasource"]
asset = datasource.get_asset("stg_supply_chain_asset")
batch_request = asset.build_batch_request()

# 3. สร้างหรืออัปเดต Expectation Suite
expectation_suite_name = "stg_supply_chain_suite"
context.add_or_update_expectation_suite(expectation_suite_name=expectation_suite_name)
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name=expectation_suite_name,
)

print(f"Creating Expectations for suite: '{expectation_suite_name}'...")

# --- ชุดกฎการตรวจสอบข้อมูล (Expectations) ---

# ตรวจสอบ Primary Key และ Foreign Keys
validator.expect_column_values_to_be_unique(column='Order Item Id')
validator.expect_column_values_to_not_be_null(column='Order Item Id')
validator.expect_column_values_to_not_be_null(column='Order Id')
validator.expect_column_values_to_not_be_null(column='Customer Id')

# ตรวจสอบข้อมูลทั่วไป
validator.expect_column_values_to_be_in_set(
    column='Order Status',
    value_set=['COMPLETE', 'PENDING_PAYMENT', 'PROCESSING', 'PENDING', 'CLOSED', 'ON_HOLD', 'SUSPECTED_FRAUD', 'CANCELED', 'PAYMENT_REVIEW']
)

validator.expect_column_values_to_be_between(column='order date (DateOrders)', max_value=date.today().isoformat(), parse_strings_as_datetimes=True)
# validator.expect_column_values_to_match_regex(
#     column='order date (DateOrders)',
#     # Regex นี้จะตรงกับเช่น "2018-01-31 08:24:00"
#     regex=r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$' 
# )

# ตรวจสอบข้อมูลตัวเลขทางการเงินและจำนวน
validator.expect_column_values_to_be_between(column='Order Item Quantity', min_value=1)
validator.expect_column_values_to_be_between(column='Product Price', min_value=0)
validator.expect_column_values_to_be_between(column='Sales', min_value=0)

# ตรวจสอบค่าพิกัด Latitude และ Longitude
validator.expect_column_values_to_be_between(column='Latitude', min_value=-90, max_value=90)
validator.expect_column_values_to_be_between(column='Longitude', min_value=-180, max_value=180)

# # ตรวจสอบวันที่จัดส่งต้องไม่ก่อนวันสั่งซื้อ
validator.expect_column_pair_values_A_to_be_greater_than_B(
    column_A='shipping date (DateOrders)',
    column_B='order date (DateOrders)',
    or_equal=True,
    # parse_strings_as_datetimes=True
)

# ตรวจสอบค่าที่เป็นไปได้ต่างๆ
validator.expect_column_values_to_be_between(column='Order Item Discount Rate', min_value=0, max_value=1)
validator.expect_column_values_to_be_in_set(column='Type', value_set=['DEBIT', 'PAYMENT', 'TRANSFER', 'CASH'])
validator.expect_column_values_to_be_in_set(column='Shipping Mode', value_set=['First Class', 'Same Day', 'Second Class', 'Standard Class'])
validator.expect_column_values_to_be_in_set(column='Delivery Status', value_set=['Advance shipping', 'Late delivery', 'Shipping canceled', 'Shipping on time'])
validator.expect_column_values_to_be_in_set(column='Market', value_set=['Pacific Asia', 'USCA', 'Africa', 'Europe', 'LATAM'])
validator.expect_column_values_to_be_in_set(column='Customer Segment', value_set=['Consumer', 'Corporate', 'Home Office'])
validator.expect_column_values_to_be_in_set(column='Late_delivery_risk', value_set=[0, 1])
validator.expect_column_values_to_be_in_set(column='Product Status', value_set=[0, 1])

# ตรวจสอบค่าตัวเลขต้องไม่ติดลบ
validator.expect_column_values_to_be_between(column='Days for shipment (scheduled)', min_value=0)
validator.expect_column_values_to_be_between(column='Days for shipping (real)', min_value=0)
validator.expect_column_values_to_be_between(column='Order Item Product Price', min_value=0)
validator.expect_column_values_to_be_between(column='Order Item Total', min_value=0)
validator.expect_column_values_to_be_between(column='Order Item Discount', min_value=0)
validator.expect_column_values_to_be_between(column='Sales per customer', min_value=0)

# # ตรวจสอบความยาวขั้นต่ำของคำอธิบายสินค้า
# validator.expect_column_value_lengths_to_be_between(column='Product Description', min_value=100)

# ตรวจสอบคอลัมน์ต่างๆ ต้องไม่เป็นค่าว่าง (Not Null)
# columns_to_be_not_null = [
#     'Customer City', 'Category Id', 'Department Id', 'Product Card Id', 'Product Category Id',
#     'Order Customer Id', 'Order Item Cardprod Id', 'Order Region', 'Category Name', '_airbyte_ab_id',
#     '_airbyte_emitted_at', 'Order City', 'Customer Fname', 'Department Name', '_airbyte_normalized_at',
#     '_airbyte_datacosupplychaindataset_hashid', 'Order State', 'Order Country', 'Customer State',
#     'Customer Country', 'Customer Street', 'Customer Lname', 'Customer Email', 'Customer Zipcode',
#     'Benefit per order', 'Order Profit Per Order', 'Order Item Profit Ratio', 'Product Image',
#     'Customer Password'
# ]
columns_to_be_not_null = [
    'Customer City', 'Category Id', 'Department Id', 'Product Card Id', 'Product Category Id',
    'Order Customer Id', 'Order Item Cardprod Id', 'Order Region', 'Category Name', 'Order City', 'Customer Fname', 'Department Name', 
    'Order State', 'Order Country', 'Customer State',
    'Customer Country', 'Customer Street', 'Customer Email','Benefit per order', 
    'Order Profit Per Order', 'Order Item Profit Ratio', 'Product Image',
    'Customer Password'
]

for col in columns_to_be_not_null:
    validator.expect_column_values_to_not_be_null(column=col)

# 4. บันทึก Expectation Suite
validator.save_expectation_suite(discard_failed_expectations=False)

print(f"✅ Expectation suite '{expectation_suite_name}' is ready.")