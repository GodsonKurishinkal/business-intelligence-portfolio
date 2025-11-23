"""
dbt Model: Supply Chain KPIs
============================

Key Performance Indicators for Supply Chain Efficiency.
Metrics:
- Service Level (Target: 98%)
- Stockout Rate
- Inventory Turnover
"""

{{ config(
    materialized='table',
    schema='marts'
) }}

with inventory as (
    select * from {{ ref('stg_inventory') }}
),

store_level_kpis as (
    
    select
        store_id,
        count(distinct item_id) as total_items,
        avg(service_level) as avg_service_level,
        avg(stockout_frequency) as avg_stockout_rate,
        avg(inventory_turnover_proxy) as avg_turnover,
        
        -- Categorize Service Level
        sum(case when service_level >= 0.98 then 1 else 0 end) as items_meeting_target,
        sum(case when service_level < 0.90 then 1 else 0 end) as critical_items
        
    from inventory
    group by store_id
    
),

final_metrics as (
    
    select
        store_id,
        total_items,
        round(avg_service_level * 100, 2) as service_level_pct,
        round(avg_stockout_rate * 100, 2) as stockout_rate_pct,
        round(avg_turnover, 2) as turnover_ratio,
        
        round(items_meeting_target::numeric / total_items * 100, 1) as pct_items_meeting_sla,
        
        case
            when avg_service_level >= 0.98 then 'Excellent'
            when avg_service_level >= 0.95 then 'Good'
            when avg_service_level >= 0.90 then 'Fair'
            else 'Poor'
        end as store_performance_rating
        
    from store_level_kpis
    
)

select * from final_metrics
order by service_level_pct desc
