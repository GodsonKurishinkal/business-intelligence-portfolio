"""
dbt Model: Staging Inventory Metrics
====================================

Stage gold layer inventory metrics for analytics.
"""

{{ config(
    materialized='view',
    schema='staging'
) }}

with source_data as (
    
    select
        item_id,
        store_id,
        total_sales,
        avg_daily_sales,
        days_observed,
        first_date,
        last_date,
        zero_sales_days,
        stockout_frequency,
        service_level,
        inventory_turnover_proxy,
        created_at
    from {{ source('gold', 'inventory_metrics') }}
    
)

select * from source_data
