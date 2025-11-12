select
    {{ dbt_utils.generate_surrogate_key(['"Delivery Status"']) }} as delivery_status_id,
    "Delivery Status" as delivery_status_name
from (
    select distinct "Delivery Status"
    from {{ source('staging', 'datacosupplychaindataset_tmp') }}
    where "Delivery Status" is not null
) as distinct_statuses