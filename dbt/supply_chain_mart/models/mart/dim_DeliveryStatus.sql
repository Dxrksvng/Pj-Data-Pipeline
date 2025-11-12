-- models/marts/dim_DeliveryStatus.sql
select * from {{ source('core_core', 'delivery_status') }}