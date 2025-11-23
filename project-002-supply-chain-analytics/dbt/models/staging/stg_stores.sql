"""
dbt Model: Staging Store Performance
====================================

Stage gold layer store performance metrics.
"""

{{ config(
    materialized='view',
    schema='staging'
) }}

with source_data as (
    
    select
        store_id,
        total_sales,
        avg_daily_sales,
        total_revenue,
        num_items,
        first_date,
        last_date,
        days_operation,
        revenue_per_day,
        created_at
    from {{ source('gold', 'store_performance') }}
    
)

select * from source_data
