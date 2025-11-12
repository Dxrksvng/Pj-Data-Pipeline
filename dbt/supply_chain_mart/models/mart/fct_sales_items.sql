-- models/mart/fct_sales_items.sql
with order_items as (
    select * from {{ source('core_core', 'order_items') }} 
),
orders as (
    select * from {{ source('core_core', 'orders') }} 
),
dim_date as (
    select * from {{ ref('dim_Date') }} 
),
dim_order_status as (
    select * from {{ ref('dim_OrderStatus') }} 
)
select
    -- Keys
    item.order_item_id,
    item.order_id,
    d.date_key as order_date_key,
    item.product_card_id as product_key,
    ord.customer_id as customer_key,
    ord.location_id as location_key,
    dos.order_status_key,
    
    -- Measures
    item.sales,
    item.order_item_quantity,
    item.order_item_discount,
    item.order_item_total,
    item.benefit_per_order,
    item.order_profit_per_order,
    item.order_item_profit_ratio
    
from order_items as item
left join orders as ord on item.order_id = ord.order_id
left join dim_date as d on cast(ord.order_date as date) = d.full_date
left join dim_order_status as dos on ord.order_status = dos.order_status_name