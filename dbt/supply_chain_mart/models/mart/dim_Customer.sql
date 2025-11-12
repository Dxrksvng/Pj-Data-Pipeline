-- models/marts/dim_Customer.sql
select
    customer_id as customer_key,
    customer_fname,
    customer_lname,
    customer_email,
    customer_segment,
    customer_city,
    customer_state,
    customer_country,
    customer_zipcode,
    customer_street
from {{ source('core_core', 'customers') }} 