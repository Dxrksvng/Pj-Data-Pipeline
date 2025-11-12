select
    "Order Item Id" as order_item_id,
    "Order Id" as order_id,
    "Order Item Cardprod Id" as product_card_id,
    "Order Item Quantity" as order_item_quantity,
    "Order Item Product Price" as order_item_product_price,
    "Order Item Discount Rate" as order_item_discount_rate,
    "Order Item Discount" as order_item_discount,
    "Order Item Profit Ratio" as order_item_profit_ratio,
    "Order Item Total" as order_item_total,
    "Sales" as sales,
    "Benefit per order" as benefit_per_order,
    "Order Profit Per Order" as order_profit_per_order
from {{ source('staging', 'datacosupplychaindataset_tmp') }} 
where "Order Item Id" is not null