select
    distinct
    "Category Id" as category_id,
    "Category Name" as category_name,
    "Department Id" as department_id
from {{ source('staging', 'datacosupplychaindataset_tmp') }}
where "Category Id" is not null