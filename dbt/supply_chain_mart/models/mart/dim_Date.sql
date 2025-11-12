-- models/mart/dim_Date.sql

WITH all_dates AS (

    SELECT order_date AS full_datetime FROM {{ source('core_core', 'orders') }}
    UNION
    SELECT shipping_date AS full_datetime FROM {{ source('core_core', 'shipping') }}
),

unique_dates AS (
    SELECT DISTINCT
        CAST(full_datetime AS DATE) AS full_date
    FROM all_dates
    WHERE full_datetime IS NOT NULL
)

SELECT
    -- ใช้ MD5 ของ PostgreSQL เพื่อสร้าง Key (ตามไอเดียของคุณ)
    md5(CAST(full_date AS text)) AS date_key,
    
    full_date,
    EXTRACT(YEAR FROM full_date) AS year,
    EXTRACT(QUARTER FROM full_date) AS quarter,
    EXTRACT(MONTH FROM full_date) AS month_number,
    TO_CHAR(full_date, 'Month') AS month_name,
    EXTRACT(DAY FROM full_date) AS day_of_month,
    EXTRACT(DOW FROM full_date) AS day_of_week, -- 0=Sun, 6=Sat (Postgres DOW)
    TO_CHAR(full_date, 'Day') AS day_name
    
FROM unique_dates
ORDER BY full_date