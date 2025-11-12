-- ใช้ GROUP BY เพื่อให้ได้ลูกค้า 1 แถวต่อ 1 ID
select
    "Customer Id" as customer_id,
    max("Customer Fname") as customer_fname,
    max("Customer Lname") as customer_lname,
    max("Customer Email") as customer_email,
    max("Customer Password") as customer_password,
    max("Customer Segment") as customer_segment,
    max("Customer Street") as customer_street,
    max("Customer City") as customer_city,
    max("Customer State") as customer_state,
    max("Customer Zipcode") as customer_zipcode,
    max("Customer Country") as customer_country
from {{ source('staging', 'datacosupplychaindataset_tmp') }} 
where "Customer Id" is not null
group by 1