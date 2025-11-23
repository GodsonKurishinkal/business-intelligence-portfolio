"""
dbt Model: Staging Sales
========================

Stage gold layer sales data for analytics transformations.
"""

{{ config(
    materialized='view',
    schema='staging'
) }}

with source_data as (
    
    select
        date,
        store_id,
        item_id,
        total_sales,
        total_revenue,
        avg_price,
        min_price,
        max_price,
        days_in_stock,
        created_at
    from {{ source('gold', 'daily_sales_agg') }}
    
),

add_computed_fields as (
    
    select
        *,
        -- Extract date parts
        extract(year from date) as year,
        extract(quarter from date) as quarter,
        extract(month from date) as month,
        extract(week from date) as week,
        extract(dayofweek from date) as day_of_week,
        
        -- Revenue metrics
        case 
            when total_sales > 0 then total_revenue / total_sales 
            else 0 
        end as revenue_per_unit,
        
        -- Price stability
        case 
            when avg_price > 0 then (max_price - min_price) / avg_price 
            else 0 
        end as price_volatility
        
    from source_data
    
)

select * from add_computed_fields
