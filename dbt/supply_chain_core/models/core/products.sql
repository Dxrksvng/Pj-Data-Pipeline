select
    "Product Card Id" as product_card_id,
    max("Product Name") as product_name,
    max("Product Description") as product_description,
    max("Product Price") as product_price,
    max("Product Status") as product_status,
    max("Product Image") as product_image,
    max("Category Id") as category_id
from {{ source('staging', 'datacosupplychaindataset_tmp') }} 
where "Product Card Id" is not null
group by 1