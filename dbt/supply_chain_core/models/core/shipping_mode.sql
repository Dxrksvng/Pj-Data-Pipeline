select
    {{ dbt_utils.generate_surrogate_key(['"Shipping Mode"']) }} as shipping_mode_id,
    "Shipping Mode" as shipping_mode_name
from (
    select distinct "Shipping Mode"
    from {{ source('staging', 'datacosupplychaindataset_tmp') }}
    where "Shipping Mode" is not null
) as distinct_modes