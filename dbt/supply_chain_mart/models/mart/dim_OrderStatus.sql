-- models/marts/dim_OrderStatus.sql
select
    {{ dbt_utils.generate_surrogate_key(['order_status']) }} as order_status_key,
    order_status as order_status_name
from (
    select distinct order_status from {{ source('core_core', 'orders') }} 
) as distinct_statuses