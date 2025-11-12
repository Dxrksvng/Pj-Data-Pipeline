# pipeline_DataCo
Link slide presentation: https://www.youtube.com/watch?v=dO6Y7ipzRO0
DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS
https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis
1.บริบทธุรกิจ (Business Context) 
อุตสาหกรรม: ธุรกิจค้าปลีก (Retail) หรือ E-commerce ที่มีการดำเนินงานทั่วโลก (Global)
ตลาดหลัก: USCA, LATAM, Europe, Pacific Asia และ Africa
กลุ่มลูกค้า: แบ่งชัดเจน 3 กลุ่ม ได้แก่ Consumer (ผู้บริโภคทั่วไป), Corporate (องค์กร), และ Home Office (ออฟฟิศขนาดเล็ก)
กระบวนการหลัก: หัวใจสำคัญคือการจัดการโลจิสติกส์และซัพพลายเชน (Supply Chain) ตั้งแต่การจัดการคำสั่งซื้อ (Order Management), การชำระเงิน, การตรวจจับการทุจริต (Fraud Detection) ไปจนถึงการจัดส่งสินค้า
ความท้าทาย: การบริหารจัดการการขนส่งให้ตรงเวลา (วิเคราะห์ Late_delivery_risk) และการรักษาผลกำไรต่อออเดอร์
2.เป้าหมายของทีม Data (Data Team Goals)
สร้าง Single Source of Truth (SSOT) : พัฒนา Data Warehouse (Core Schema) ที่เป็น 3NF เพื่อให้ทุกแผนกใช้ข้อมูลจากแหล่งเดียวกัน
สนับสนุนทีม Logistics : สร้าง Dashboard ติดตามประสิทธิภาพการจัดส่ง (เช่น OTD Rate) และวิเคราะห์สาเหตุของความล่าช้า
สนับสนุนทีม Sales & Finance : รายงานยอดขาย (Sales) และกำไร (Profit) โดยสามารถเจาะลึก (Drill-down) ตามภูมิภาค, สินค้า, และกลุ่มลูกค้าได้
สนับสนุนทีม Marketing : วิเคราะห์พฤติกรรมลูกค้า (Customer Behavior) และผลกระทบของส่วนลด (Discount) ต่อยอดขาย
สนับสนุนทีม Risk : สร้างระบบแจ้งเตือนและ Dashboard สำหรับติดตามคำสั่งซื้อที่น่าสงสัย (SUSPECTED_FRAUD)
3.SLA / Schedule (ข้อตกลงระดับบริการ)
กำหนดรอบการประมวลผล (Schedule) และความสดใหม่ของข้อมูล (Freshness) ตามความต้องการใช้งาน:
ต้องพร้อมใช้งานภายใน 8:00 น. ของทุกเช้า
รัน Transform + Validate + Publish ทุก 1 ชั่วโมง
หากแล้วเสร็จ หรือ มีข้อขัดข้อง ให้แจ้งเตือนทีม Data/BI ทางช่องทางที่กำหนด (Email)
4.KPI (ดัชนีชี้วัดความสำเร็จ)
KPIs หลักที่จะถูกนำไปสร้างใน Dashboard ปลายทาง :
ด้านโลจิสติกส์ (Logistics):
On-Time Delivery (OTD) Rate: % ของออเดอร์ที่สถานะ 'Shipping on time'
Late Delivery Rate: % ของออเดอร์ที่ Late_delivery_risk = 1
Shipping Days Variance: ( Days for shipping (real) ) - ( Days for shipment (scheduled) )
ด้านการขายและกำไร (Sales & Profit):
Total Sales: ผลรวมของ Sales
Total Profit: ผลรวมของ benefit_per_order และ order_profit_per_order (คำนวณจาก fct_sales_items)
Profit Margin %
Average Order Value (AOV)
ด้านลูกค้า (Customer):
Sales by Customer Segment: ยอดขายแบ่งตามกลุ่มลูกค้า
ด้านความเสี่ยง (Risk):
Fraud Rate: % ของออเดอร์ที่มีสถานะ SUSPECTED_FRAUD
Value at Risk (VaR): ผลรวมยอดเงินของออเดอร์ที่ SUSPECTED_FRAUD
Core Database Schema (3NF) Diagram
departments
int
department_id
PK
PK
varchar
department_name
categories
int
category_id
PK
PK
varchar
category_name
int
department_id
FK
FK
products
int
product_card_id
PK
PK
varchar
product_name
varchar
product_description
numeric
product_price
int
category_id
FK
FK
customers
int
customer_id
PK
PK
varchar
customer_name
varchar
customer_segment
varchar
customer_city
location
varchar
location_id
PK
PK
varchar
order_zipcode
varchar
order_city
float
latitude
float
longitude
varchar
market
varchar
order_region
shipping_mode
varchar
shipping_mode_id
PK
PK
varchar
shipping_mode_name
delivery_status
varchar
delivery_status_id
PK
PK
varchar
delivery_status_name
orders
int
order_id
PK
PK
timestamp
order_date
varchar
order_status
int
customer_id
FK
FK
varchar
location_id
FK
FK
shipping
int
order_id
PK
PK, FK
timestamp
shipping_date
int
days_scheduled
int
days_real
int
late_delivery_risk
varchar
shipping_mode_id
FK
FK
varchar
delivery_status_id
FK
FK
order_items
int
order_item_id
PK
PK
int
order_id
FK
FK
int
product_card_id
FK
FK
int
order_item_quantity
numeric
sales
numeric
benefit_per_order
numeric
order_profit_per_order
has
has
places
ships to
has
contains
is
uses
has status
​
อธิบาย
Core Database = Database กลางแบบ 3NF โดยใช้ dbt ทำการ Transform มาจากตารางใน staging(ตารางข้อมูลดิบ)
✅ 1. ผ่านกฎข้อที่ 1 (First Normal Form - 1NF)
คือ ทุกคอลัมน์ในตารางจะต้องเก็บค่าเดียว (Atomic) และไม่มีกลุ่มข้อมูลซ้ำ (Repeating Groups)
ตรงกับ Schema อย่างไร:
ในทุกตารางที่เราออกแบบ (tbl_Products, tbl_Customers, etc.) แต่ละช่องจะเก็บข้อมูลเพียงค่าเดียว 
✅ 2. ผ่านกฎข้อที่ 2 (Second Normal Form - 2NF)
กฎข้อนี้ระบุว่า ข้อมูลที่ไม่ใช่คีย์หลักทุกตัว จะต้องขึ้นอยู่กับ "คีย์หลักทั้งหมด" (Fully dependent on the primary key) กฎข้อนี้จะมีความสำคัญมากในตารางที่มีคีย์หลักแบบผสม (Composite Primary Key)
ตรงกับ Schema อย่างไร:
ตารางส่วนใหญ่ของเราใช้ Single-column Primary Key (เช่น order_id ในตาราง orders) ซึ่งเมื่อเป็นเช่นนี้ ตารางจะผ่านกฎ 2NF โดยอัตโนมัติ เพราะไม่มีทางที่ข้อมูลจะไปขึ้นอยู่กับ "ส่วนใดส่วนหนึ่ง" ของคีย์หลักได้
แม้แต่ในตาราง order_items ซึ่ง order_item_id เป็นคีย์หลัก ทุกคอลัมน์ที่เหลือ เช่น order_item_quantity หรือ sales ก็ล้วนอธิบายรายละเอียดของ "รายการสินค้านั้นๆ" โดยตรง จึงขึ้นอยู่กับ order_item_id ทั้งหมด
✅ 3. ผ่านกฎข้อที่ 3 (Third Normal Form - 3NF)
กฎข้อนี้ระบุว่า จะต้องไม่มีการพึ่งพากันระหว่างข้อมูลที่ไม่ใช่คีย์หลัก (No Transitive Dependencies)
ตรงกับ Schema อย่างไร: เราได้ทำการแยกตารางเพื่อกำจัด Transitive Dependencies เหล่านี้โดยเฉพาะ
ตัวอย่างที่ 1: การสร้างตาราง dim_Location
ถ้าไม่ทำ 3NF: ตาราง orders จะมีหน้าตาแบบนี้:
order_id (PK), order_city, order_state, order_country, order_region, market
ปัญหาคืออะไร: market ขึ้นอยู่กับ order_country, order_country ขึ้นอยู่กับ order_state, และ order_state ขึ้นอยู่กับ order_city นี่คือการพึ่งพากันเป็นทอดๆ ของ Non-key attributes ซึ่งเรียกว่า Transitive Dependency
การแก้ไข (ที่ทำใน Schema): เราได้ย้ายข้อมูลทางภูมิศาสตร์ทั้งหมด (order_city, order_state, order_country, order_region, market, latitude, longitude) ไปไว้ในตารางใหม่คือ location และให้ orders เก็บแค่ location_id (FK) ซึ่งเป็นคีย์หลักของ location แทน ทำให้ข้อมูลใน orders ขึ้นอยู่กับ order_id เท่านั้น
ตัวอย่างที่ 2: การสร้างตาราง shipping_mode และ delivery_status
ถ้าไม่ทำ 3NF: ตาราง shipping อาจจะมีคอลัมน์ shipping_mode_name ที่เก็บข้อความว่า 'Standard Class' หรือ 'First Class' โดยตรง
ปัญหาคืออะไร: แม้จะไม่ใช่ Transitive Dependency ที่ชัดเจน แต่การเก็บข้อมูลที่เป็น "ประเภท" หรือ "หมวดหมู่" ในรูปแบบข้อความซ้ำๆ จะทำให้เกิดความซ้ำซ้อนและเสี่ยงต่อการพิมพ์ผิด (เช่น 'Standard Class' กับ 'standard class')
การแก้ไข (ที่ทำใน Schema): เราได้แยกข้อมูลเหล่านี้ออกมาเป็นตารางมิติ (shipping_mode, delivery_status) แล้วใช้ ID (FK) มาอ้างอิงแทน ซึ่งเป็นแนวปฏิบัติที่ดีที่สุดในการทำ Normalization
ตัวอย่างที่ 3: การตัดคอลัมน์ Sales per customer
ปัญหาคืออะไร: ค่า Sales per customer ไม่ได้ขึ้นอยู่กับ order_id หรือ order_item_id โดยตรง แต่เป็นค่าที่ "คำนวณ" มาจากการรวม sales ทั้งหมดของ customer_id คนนั้นๆ มันจึงขึ้นอยู่กับ customer_id ซึ่งเป็น Non-key attribute ในตาราง Orders/OrderItems
การแก้ไข (ที่ทำใน Schema): เราตัดคอลัมน์นี้ออกไปเลย เพราะเป็นค่าที่ควร คำนวณสด (On-the-fly) เมื่อต้องการใช้งาน ไม่ใช่สิ่งที่ต้องจัดเก็บถาวรในตารางข้อมูลดิบ
Data Mart Schema (Star Schemas) Diagram
erDiagram
    %% --- CONFORMED DIMENSIONS (มิติที่ใช้ร่วมกัน) ---
    dim_date {
        varchar date_key PK "PK"
        date full_date
        int year
        int month_number
        varchar month_name
    }
    dim_customer {
        int customer_key PK "PK"
        varchar customer_name
        varchar customer_segment
    }
    dim_product {
        int product_key PK "PK"
        varchar product_name
        varchar category_name
        varchar department_name
    }
    dim_location {
        varchar location_id PK "PK"
        varchar order_city
        varchar market
        float latitude
        float longitude
    }
    dim_orderstatus {
        varchar order_status_key PK "PK"
        varchar order_status_name
    }
    dim_shippingmode {
        varchar shipping_mode_id PK "PK"
        varchar shipping_mode_name
    }
    dim_deliverystatus {
        varchar delivery_status_id PK "PK"
        varchar delivery_status_name
    }

    %% --- MART 1: Sales (Grain: Order Item) ---
    fct_sales_items {
        int order_item_id PK "PK"
        varchar order_date_key FK "FK"
        int product_key FK "FK"
        int customer_key FK "FK"
        varchar location_id FK "FK"
        varchar order_status_key FK "FK"
        numeric sales
        int order_item_quantity
        numeric benefit_per_order
    }

    %% --- MART 2: Shipping (Grain: Order) ---
    fct_shipping_orders {
        int order_id PK "PK"
        varchar order_date_key FK "FK (Order)"
        varchar shipping_date_key FK "FK (Ship)"
        int customer_key FK "FK"
        varchar location_id FK "FK"
        varchar order_status_key FK "FK"
        varchar shipping_mode_id FK "FK"
        varchar delivery_status_id FK "FK"
        int days_scheduled
        int days_real
        int late_delivery_risk
    }

    %% --- Relationships Mart 1: Sales ---
    fct_sales_items }o--|| dim_date : "on"
    fct_sales_items }o--|| dim_product : "of"
    fct_sales_items }o--|| dim_customer : "by"
    fct_sales_items }o--|| dim_location : "at"
    fct_sales_items }o--|| dim_orderstatus : "status"

    %% --- Relationships Mart 2: Shipping ---
    fct_shipping_orders }o--|| dim_date : "ordered on"
    fct_shipping_orders }o..|| dim_date : "shipped on"
    fct_shipping_orders }o--|| dim_customer : "for"
    fct_shipping_orders }o--|| dim_location : "to"
    fct_shipping_orders }o--|| dim_orderstatus : "status"
    fct_shipping_orders }o--|| dim_shippingmode : "via"
    fct_shipping_orders }o--|| dim_deliverystatus : "delivery status"
​
dim_date
varchar
date_key
PK
PK
date
full_date
int
year
int
month_number
varchar
month_name
dim_customer
int
customer_key
PK
PK
varchar
customer_name
varchar
customer_segment
dim_product
int
product_key
PK
PK
varchar
product_name
varchar
category_name
varchar
department_name
dim_location
varchar
location_id
PK
PK
varchar
order_city
varchar
market
float
latitude
float
longitude
dim_orderstatus
varchar
order_status_key
PK
PK
varchar
order_status_name
fct_sales_items
int
order_item_id
PK
PK
varchar
order_date_key
FK
FK
int
product_key
FK
FK
int
customer_key
FK
FK
varchar
location_id
FK
FK
varchar
order_status_key
FK
FK
numeric
sales
int
order_item_quantity
numeric
benefit_per_order
on
of
by
at
status
​
erDiagram
    %% --- CONFORMED DIMENSIONS (มิติที่ใช้ร่วมกัน) ---
    dim_date {
        varchar date_key PK "PK"
        date full_date
        int year
        int month_number
        varchar month_name
    }
    dim_customer {
        int customer_key PK "PK"
        varchar customer_name
        varchar customer_segment
    }
    dim_location {
        varchar location_id PK "PK"
        varchar order_city
        varchar market
        float latitude
        float longitude
    }
    dim_orderstatus {
        varchar order_status_key PK "PK"
        varchar order_status_name
    }
    dim_shippingmode {
        varchar shipping_mode_id PK "PK"
        varchar shipping_mode_name
    }
    dim_deliverystatus {
        varchar delivery_status_id PK "PK"
        varchar delivery_status_name
    }


    %% --- MART 2: Shipping (Grain: Order) ---
    fct_shipping_orders {
        int order_id PK "PK"
        varchar order_date_key FK "FK (Order)"
        varchar shipping_date_key FK "FK (Ship)"
        int customer_key FK "FK"
        varchar location_id FK "FK"
        varchar order_status_key FK "FK"
        varchar shipping_mode_id FK "FK"
        varchar delivery_status_id FK "FK"
        int days_scheduled
        int days_real
        int late_delivery_risk
    }


    %% --- Relationships Mart 2: Shipping ---
    fct_shipping_orders }o--|| dim_date : "ordered on"
    fct_shipping_orders }o..|| dim_date : "shipped on"
    fct_shipping_orders }o--|| dim_customer : "for"
    fct_shipping_orders }o--|| dim_location : "to"
    fct_shipping_orders }o--|| dim_orderstatus : "status"
    fct_shipping_orders }o--|| dim_shippingmode : "via"
    fct_shipping_orders }o--|| dim_deliverystatus : "delivery status"
dim_date
varchar
date_key
PK
PK
date
full_date
int
year
int
month_number
varchar
month_name
dim_customer
int
customer_key
PK
PK
varchar
customer_name
varchar
customer_segment
dim_location
varchar
location_id
PK
PK
varchar
order_city
varchar
market
float
latitude
float
longitude
dim_orderstatus
varchar
order_status_key
PK
PK
varchar
order_status_name
dim_shippingmode
varchar
shipping_mode_id
PK
PK
varchar
shipping_mode_name
dim_deliverystatus
varchar
delivery_status_id
PK
PK
varchar
delivery_status_name
fct_shipping_orders
int
order_id
PK
PK
varchar
order_date_key
FK
FK (Order)
varchar
shipping_date_key
FK
FK (Ship)
int
customer_key
FK
FK
varchar
location_id
FK
FK
varchar
order_status_key
FK
FK
varchar
shipping_mode_id
FK
FK
varchar
delivery_status_id
FK
FK
int
days_scheduled
int
days_real
int
late_delivery_risk
ordered on
shipped on
for
to
status
via
delivery status
​
อธิบาย
Data Mart =  database ที่เอาไว้ใช้ query เพื่อตอบ KPI ให้ได้, จะ query ได้ไวกว่า Core Database เพราะเป็นแบบ star schema
Fact Table 1: Sales & Profitability (การขายและกำไร)
ใช้ตอบคำถามว่า "ขายอะไร, ได้กำไรเท่าไหร่, ขายให้ใคร, ที่ไหน"
Fact Table : fct_sales_items
Grain (ความละเอียด) : 1 แถว คือ 1 รายการสินค้า ( order_item_id )
Fact Table 2: Logistics & Fulfillment (การขนส่ง)
Data Mart นี้ใช้ตอบคำถามว่า "การขนส่งเป็นอย่างไร, ช้า/เร็ว, มีความเสี่ยงแค่ไหน"
Fact Table : fct_shipping_orders
Grain (ความละเอียด) : 1 แถว คือ 1 คำสั่งซื้อ ( order_id )
