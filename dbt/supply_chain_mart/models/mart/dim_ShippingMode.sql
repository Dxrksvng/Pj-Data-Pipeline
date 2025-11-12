-- models/marts/dim_ShippingMode.sql
select * from {{ source('core_core', 'shipping_mode') }}