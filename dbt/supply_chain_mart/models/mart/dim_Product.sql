-- models/marts/dim_Product.sql
select
    p.product_card_id as product_key,
    p.product_name,
    p.product_description,
    p.product_price,
    p.product_status,
    p.product_image,
    c.category_name,
    d.department_name
from {{ source('core_core', 'products') }} as p 
left join {{ source('core_core', 'categories') }} as c on p.category_id = c.category_id 
left join {{ source('core_core', 'departments') }} as d on c.department_id = d.department_id 