-- models/core/dim_location.sql (หรือ location.sql)

with distinct_locations as (
    select distinct
        "Order Zipcode" as order_zipcode,
        "Order City" as order_city,
        "Order State" as order_state,
        "Order Country" as order_country,
        "Order Region" as order_region,
        "Market" as market,
        "Latitude" as latitude,
        "Longitude" as longitude
    from {{ source('staging', 'datacosupplychaindataset_tmp') }}
)
select
    {{ dbt_utils.generate_surrogate_key([
        'coalesce(order_zipcode::text, \'NULL_ZIP\')',
        'coalesce(order_city, \'NULL_CITY\')',
        'coalesce(order_state, \'NULL_STATE\')',
        'coalesce(order_country, \'NULL_COUNTRY\')',
        'coalesce(order_region, \'NULL_REGION\')',
        'coalesce(market, \'NULL_MARKET\')',
        'coalesce(latitude::text, \'NULL_LAT\')',
        'coalesce(longitude::text, \'NULL_LONG\')'
    ]) }} as location_id,
    *
from distinct_locations