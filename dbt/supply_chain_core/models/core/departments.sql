select
    distinct
    "Department Id" as department_id,
    "Department Name" as department_name
from {{ source('staging', 'datacosupplychaindataset_tmp') }} 
where "Department Id" is not null