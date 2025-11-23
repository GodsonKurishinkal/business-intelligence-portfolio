"""
dbt Model: Inventory KPIs
=========================

Calculate comprehensive inventory performance metrics.
"""

{{ config(
    materialized='table',
    schema='marts'
) }}

with staging_sales as (
    select * from {{ ref('stg_sales') }}
),

inventory_base as (
    
    select
        item_id,
        store_id,
        
        -- Volume metrics
        sum(total_sales) as total_sales_qty,
        sum(total_revenue) as total_revenue,
        avg(total_sales) as avg_daily_sales,
        stddev(total_sales) as stddev_sales,
        
        -- Time metrics
        count(distinct date) as days_with_data,
        min(date) as first_sale_date,
        max(date) as last_sale_date,
        
        -- Stock availability
        sum(days_in_stock) as days_in_stock,
        
        -- Price metrics
        avg(avg_price) as avg_sell_price,
        min(min_price) as min_sell_price,
        max(max_price) as max_sell_price
        
    from staging_sales
    group by item_id, store_id
    
),

inventory_kpis as (
    
    select
        item_id,
        store_id,
        
        -- Base metrics
        total_sales_qty,
        total_revenue,
        avg_daily_sales,
        stddev_sales,
        avg_sell_price,
        
        -- KPI 1: Coefficient of Variation (Demand Variability)
        case 
            when avg_daily_sales > 0 
            then stddev_sales / avg_daily_sales 
            else 0 
        end as demand_cv,
        
        -- KPI 2: Service Level (proxy: days in stock / total days)
        case 
            when days_with_data > 0 
            then days_in_stock::float / days_with_data 
            else 0 
        end as service_level,
        
        -- KPI 3: Stockout Frequency
        case 
            when days_with_data > 0 
            then (days_with_data - days_in_stock)::float / days_with_data 
            else 0 
        end as stockout_frequency,
        
        -- KPI 4: Inventory Turnover (proxy)
        case 
            when avg_daily_sales > 0 
            then total_sales_qty / (avg_daily_sales * 365) 
            else 0 
        end as inventory_turnover_proxy,
        
        -- KPI 5: Days of Supply
        case 
            when avg_daily_sales > 0 
            then 365 / (total_sales_qty / (avg_daily_sales * 365)) 
            else 0 
        end as days_of_supply,
        
        -- KPI 6: Fill Rate (simplified)
        case 
            when days_with_data > 0 
            then days_in_stock::float / days_with_data 
            else 0 
        end as fill_rate,
        
        -- KPI 7: Price Stability
        case 
            when avg_sell_price > 0 
            then (max_sell_price - min_sell_price) / avg_sell_price 
            else 0 
        end as price_volatility,
        
        -- Date range
        first_sale_date,
        last_sale_date,
        days_with_data,
        
        -- Timestamp
        current_timestamp as calculated_at
        
    from inventory_base
    
),

-- XYZ Classification based on CV
xyz_classification as (
    
    select
        *,
        case
            when demand_cv < 0.5 then 'X'  -- Low variability
            when demand_cv < 1.0 then 'Y'  -- Moderate variability
            else 'Z'                        -- High variability
        end as xyz_class,
        
        -- Service level category
        case
            when service_level >= 0.98 then 'Excellent'
            when service_level >= 0.95 then 'Good'
            when service_level >= 0.90 then 'Fair'
            else 'Poor'
        end as service_level_category
        
    from inventory_kpis
    
)

select * from xyz_classification
