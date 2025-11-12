# file: create_analytics_expectations.py
import great_expectations as gx
import datetime

# 1. รับ Data Context
context = gx.get_context()

# 2. ดึง Datasource ที่สร้างไว้
datasource = context.datasources["pg_datasource"]

# --- สร้าง Expectations สำหรับ `dim_customer` ---
asset_customer = datasource.get_asset("dim_customer")
batch_request_customer = asset_customer.build_batch_request()
suite_name_customer = "validate_dim_customer"
context.add_or_update_expectation_suite(expectation_suite_name=suite_name_customer)
validator_customer = context.get_validator(
    batch_request=batch_request_customer,
    expectation_suite_name=suite_name_customer,
)

print(f"Creating Expectations for suite: '{suite_name_customer}'...")
validator_customer.expect_column_values_to_not_be_null("customer_key")
validator_customer.expect_column_values_to_be_unique("customer_key")
validator_customer.expect_column_values_to_not_be_null("customer_name")
validator_customer.expect_column_values_to_be_in_set("customer_segment", ['Consumer', 'Corporate', 'Home Office'])
validator_customer.save_expectation_suite(discard_failed_expectations=False)

# --- สร้าง Expectations สำหรับ `dim_product` ---
asset_product = datasource.get_asset("dim_product")
suite_name_product = "validate_dim_product"
context.add_or_update_expectation_suite(suite_name_product)
validator_product = context.get_validator(
    batch_request=asset_product.build_batch_request(),
    expectation_suite_name=suite_name_product,
)

print(f"Creating Expectations for suite: '{suite_name_product}'...")
validator_product.expect_column_values_to_not_be_null("product_key")
validator_product.expect_column_values_to_be_unique("product_key")
validator_product.expect_column_values_to_not_be_null("product_name")
validator_product.expect_column_values_to_not_be_null("category_name")
validator_product.expect_column_values_to_not_be_null("department_name")
validator_product.save_expectation_suite(discard_failed_expectations=False)


# --- สร้าง Expectations สำหรับ `dim_location` ---
asset_location = datasource.get_asset("dim_location")
suite_name_location = "validate_dim_location"
context.add_or_update_expectation_suite(suite_name_location)
validator_location = context.get_validator(
    batch_request=asset_location.build_batch_request(),
    expectation_suite_name=suite_name_location,
)
print(f"Creating Expectations for suite: '{suite_name_location}'...")
validator_location.expect_column_values_to_not_be_null("location_id")
validator_location.expect_column_values_to_be_unique("location_id")
validator_location.expect_column_values_to_not_be_null("order_city")
validator_location.expect_column_values_to_be_in_set(column='market', value_set=['Pacific Asia', 'USCA', 'Africa', 'Europe', 'LATAM'])
validator_location.expect_column_values_to_be_of_type("latitude", "NUMERIC")
validator_location.expect_column_values_to_be_of_type("longitude", "NUMERIC")
validator_location.save_expectation_suite(discard_failed_expectations=False)


# --- สร้าง Expectations สำหรับ `dim_date` ---
asset_date = datasource.get_asset("dim_date")
suite_name_date = "validate_dim_date"
context.add_or_update_expectation_suite(suite_name_date)
validator_date = context.get_validator(
    batch_request=asset_date.build_batch_request(),
    expectation_suite_name=suite_name_date,
)
print(f"Creating Expectations for suite: '{suite_name_date}'...")
current_year = datetime.datetime.now().year
validator_date.expect_column_values_to_not_be_null("date_key")
validator_date.expect_column_values_to_be_unique("date_key")
validator_date.expect_column_values_to_be_of_type("full_date", "DATE")
validator_date.expect_column_values_to_be_between(
    "year",
    min_value=2000,       # (ตัวอย่าง: ตั้งค่าปีขั้นต่ำที่ยอมรับได้)
    max_value=current_year
)
validator_date.expect_column_values_to_be_between(column='month_number', min_value=1, max_value=12)
validator_date.expect_column_values_to_be_in_set(column='month_name', value_set=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
validator_date.save_expectation_suite(discard_failed_expectations=False)

# --- สร้าง Expectations สำหรับ `dim_order` ---
asset_order_status = datasource.get_asset("dim_order_status")
suite_name_order = "validate_dim_order_status"
context.add_or_update_expectation_suite(suite_name_order)
validator_order = context.get_validator(
    batch_request=asset_order_status.build_batch_request(),
    expectation_suite_name=suite_name_order,
)
print(f"Creating Expectations for suite: '{suite_name_order}'...")
validator_order.expect_column_values_to_not_be_null("order_status_key")
validator_order.expect_column_values_to_be_unique("order_status_key")
validator_order.expect_column_values_to_be_in_set(
    column='order_status_name',
    value_set=['COMPLETE', 'PENDING_PAYMENT', 'PROCESSING', 'PENDING', 'CLOSED', 'ON_HOLD', 'SUSPECTED_FRAUD', 'CANCELED', 'PAYMENT_REVIEW']
)
validator_order.save_expectation_suite(discard_failed_expectations=False)

# --- สร้าง Expectations สำหรับ `dim_shipping` ---
asset_shipping_mode = datasource.get_asset("dim_shipping_mode")
suite_name_shipping = "validate_dim_shipping_mode"
context.add_or_update_expectation_suite(suite_name_shipping)
validator_shipping = context.get_validator(
    batch_request=asset_shipping_mode.build_batch_request(),
    expectation_suite_name=suite_name_shipping,
)
print(f"Creating Expectations for suite: '{suite_name_shipping}'...")
validator_shipping.expect_column_values_to_not_be_null("shipping_mode_id")
validator_shipping.expect_column_values_to_be_unique("shipping_mode_id")
validator_shipping.expect_column_values_to_be_in_set(column='shipping_mode_name', value_set=['First Class', 'Same Day', 'Second Class', 'Standard Class'])
validator_shipping.save_expectation_suite(discard_failed_expectations=False)

# --- สร้าง Expectations สำหรับ `dim_delivery` ---
asset_delivery = datasource.get_asset("dim_delivery_status")
suite_name_delivery = "validate_dim_delivery_status"
context.add_or_update_expectation_suite(suite_name_delivery)
validator_delivery = context.get_validator(
    batch_request=asset_delivery.build_batch_request(),
    expectation_suite_name=suite_name_delivery,
)
print(f"Creating Expectations for suite: '{suite_name_delivery}'...")
validator_delivery.expect_column_values_to_not_be_null("delivery_status_id")
validator_delivery.expect_column_values_to_be_unique("delivery_status_id")
validator_delivery.expect_column_values_to_be_in_set(column='delivery_status_name', value_set=['Advance shipping', 'Late delivery', 'Shipping canceled', 'Shipping on time'])
validator_delivery.save_expectation_suite(discard_failed_expectations=False)

# --- สร้าง Expectations สำหรับ `fct_order_items` ---
asset_fact = datasource.get_asset("fct_sales_items")
suite_name_fact = "validate_fct_sales_items"
context.add_or_update_expectation_suite(suite_name_fact)
validator_fact = context.get_validator(
    batch_request=asset_fact.build_batch_request(),
    expectation_suite_name=suite_name_fact,
)

print(f"Creating Expectations for suite: '{suite_name_fact}'...")
validator_fact.expect_column_values_to_not_be_null("order_item_id")
validator_fact.expect_column_values_to_be_unique("order_item_id")
validator_fact.expect_column_values_to_be_between(column='sales', min_value=0)
for fk_col in ["order_status_key", "order_date_key", "customer_key", "product_key", "location_id"]:
    validator_fact.expect_column_values_to_not_be_null(fk_col)

validator_fact.expect_column_values_to_be_between(column='order_item_quantity', min_value=1)
validator_fact.expect_column_values_to_not_be_null("benefit_per_order")
validator_fact.save_expectation_suite(discard_failed_expectations=False)

# --- สร้าง Expectations สำหรับ `fct_shipping_order` ---
asset_fact_shipping = datasource.get_asset("fct_shipping_orders")
suite_name_fact_shipping = "validate_fct_shipping_orders"
context.add_or_update_expectation_suite(suite_name_fact_shipping)
validator_fact_shipping = context.get_validator(
    batch_request=asset_fact_shipping.build_batch_request(),
    expectation_suite_name=suite_name_fact_shipping,
)

print(f"Creating Expectations for suite: '{suite_name_fact_shipping}'...")
validator_fact_shipping.expect_column_values_to_not_be_null("order_id")
validator_fact_shipping.expect_column_values_to_be_unique("order_id")
validator_fact_shipping.expect_column_values_to_be_in_set(column='late_delivery_risk', value_set=[0, 1])
for fk_col in ["order_date_key", "customer_key", "shipping_date_key", "location_id", "order_status_key", "shipping_mode_id", "delivery_status_id"]:
    validator_fact_shipping.expect_column_values_to_not_be_null(fk_col)

validator_fact_shipping.expect_column_values_to_be_between(column='days_for_shipment_scheduled', min_value=0)
validator_fact_shipping.expect_column_values_to_be_between(column='days_for_shipment_real', min_value=0)
validator_fact_shipping.save_expectation_suite(discard_failed_expectations=False)

print(f"\n✅ All Analytics Expectation suites are ready.")