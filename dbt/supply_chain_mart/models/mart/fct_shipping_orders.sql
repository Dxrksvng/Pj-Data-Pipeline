-- models/mart/fct_shipping_orders.sql
with shipping as (
    select * from {{ source('core_core', 'shipping') }} 
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
    s.order_id,
    d_order.date_key as order_date_key,
    d_ship.date_key as shipping_date_key, -- Role-playing dimension
    o.customer_id as customer_key,
    o.location_id as location_key,
    dos.order_status_key,
    s.shipping_mode_id,
    s.delivery_status_id,
    
    -- Measures
    s.days_for_shipment_scheduled,
    s.days_for_shipping_real,
    (s.days_for_shipping_real - s.days_for_shipment_scheduled) as shipping_days_variance,
    s.late_delivery_risk,
    1 as order_count

from shipping as s
left join orders as o on s.order_id = o.order_id
left join dim_date as d_order on cast(o.order_date as date) = d_order.full_date 
left join dim_date as d_ship on cast(s.shipping_date as date) = d_ship.full_date 
left join dim_order_status as dos on o.order_status = dos.order_status_name