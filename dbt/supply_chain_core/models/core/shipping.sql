with shipping_dim as (
    select * from {{ ref('shipping_mode') }}
),
delivery_dim as (
    select * from {{ ref('delivery_status') }}
),
-- ใช้ DISTINCT เพื่อให้ได้ 1 แถวต่อ 1 Order
distinct_shipping as (
    select distinct
        "Order Id" as order_id,
        "shipping date (DateOrders)" as shipping_date,
        "Days for shipment (scheduled)" as days_for_shipment_scheduled,
        "Days for shipping (real)" as days_for_shipping_real,
        "Late_delivery_risk" as late_delivery_risk,
        "Shipping Mode" as shipping_mode_name,
        "Delivery Status" as delivery_status_name
    from {{ source('staging', 'datacosupplychaindataset_tmp') }}
    where "Order Id" is not null
)
select
    s.order_id,
    s.shipping_date,
    s.days_for_shipment_scheduled,
    s.days_for_shipping_real,
    s.late_delivery_risk,
    sd.shipping_mode_id,
    dd.delivery_status_id
from distinct_shipping as s
left join shipping_dim as sd on s.shipping_mode_name = sd.shipping_mode_name
left join delivery_dim as dd on s.delivery_status_name = dd.delivery_status_name