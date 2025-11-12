-- models/core/tbl_orders.sql (หรือ orders.sql)

with location_dim as (
    select * from {{ ref('location') }} 
),
distinct_orders as (
    -- ยังคงต้อง SELECT DISTINCT เพื่อให้ได้ 1 แถวต่อ 1 Order
    select distinct
        "Order Id" as order_id,
        "Order Customer Id" as customer_id,
        "order date (DateOrders)" as order_date,
        "Order Status" as order_status,
        "Type" as transaction_type,
        
        -- สร้าง Key ชั่วคราว โดยใช้ตรรกะเดียวกับ location เป๊ะๆ
        {{ dbt_utils.generate_surrogate_key([
            'coalesce("Order Zipcode"::text, \'NULL_ZIP\')',
            'coalesce("Order City", \'NULL_CITY\')',
            'coalesce("Order State", \'NULL_STATE\')',
            'coalesce("Order Country", \'NULL_COUNTRY\')',
            'coalesce("Order Region", \'NULL_REGION\')',
            'coalesce("Market", \'NULL_MARKET\')',
            'coalesce("Latitude"::text, \'NULL_LAT\')',
            'coalesce("Longitude"::text, \'NULL_LONG\')'
        ]) }} as temp_location_id

    from {{ source('staging', 'datacosupplychaindataset_tmp') }}
    where "Order Id" is not null
)
select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.order_status,
    o.transaction_type,
    loc.location_id
from distinct_orders as o
left join location_dim as loc
    on o.temp_location_id = loc.location_id -- JOIN ด้วย Key ที่สร้างขึ้นมาใหม่