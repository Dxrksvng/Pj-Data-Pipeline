-- models/marts/dim_Location.sql
select
    location_id,
    order_zipcode,
    order_city,
    order_state,
    order_country,
    order_region,
    market,
    latitude,
    longitude
from {{ source('core_core', 'location') }}