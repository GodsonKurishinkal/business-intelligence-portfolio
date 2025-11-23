"""
dbt Model: Financial KPIs
=========================

Financial performance metrics for the supply chain.
Metrics:
- Total Revenue
- Revenue Growth (Month-over-Month)
- Revenue Concentration (Pareto)
"""

{{ config(
    materialized='table',
    schema='marts'
) }}

with monthly_sales as (
    
    select
        date_trunc('month', date) as month,
        store_id,
        sum(total_revenue) as monthly_revenue,
        sum(total_sales) as monthly_units
    from {{ ref('stg_sales') }}
    group by 1, 2
    
),

revenue_growth as (
    
    select
        month,
        store_id,
        monthly_revenue,
        monthly_units,
        
        lag(monthly_revenue) over (partition by store_id order by month) as prev_month_revenue,
        
        case
            when lag(monthly_revenue) over (partition by store_id order by month) > 0 
            then (monthly_revenue - lag(monthly_revenue) over (partition by store_id order by month)) 
                 / lag(monthly_revenue) over (partition by store_id order by month)
            else null
        end as mom_growth_pct
        
    from monthly_sales
    
),

store_contribution as (
    
    select
        store_id,
        sum(monthly_revenue) as total_revenue
    from monthly_sales
    group by 1
    
),

final_metrics as (
    
    select
        g.month,
        g.store_id,
        g.monthly_revenue,
        g.monthly_units,
        round(g.mom_growth_pct * 100, 2) as growth_pct,
        
        round(g.monthly_revenue / s.total_revenue * 100, 2) as pct_of_store_total
        
    from revenue_growth g
    join store_contribution s on g.store_id = s.store_id
    
)

select * from final_metrics
order by month desc, monthly_revenue desc
