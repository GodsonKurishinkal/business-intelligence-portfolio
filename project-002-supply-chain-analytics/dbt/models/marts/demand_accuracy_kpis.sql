"""
dbt Model: Demand Forecast Accuracy KPIs
=========================================

Calculate forecasting accuracy metrics (MAPE, bias, etc.)
Note: Requires forecast data - mock structure for demonstration
"""

{{ config(
    materialized='table',
    schema='marts'
) }}

with staging_sales as (
    select * from {{ ref('stg_sales') }}
),

-- Mock forecast data (in production, join with actual forecasts from gold layer)
forecast_mock as (
    
    select
        date,
        item_id,
        store_id,
        total_sales as actual_sales,
        
        -- Mock forecast (in production, this comes from ML models)
        total_sales * (1 + (random() * 0.4 - 0.2)) as forecast_sales
        
    from staging_sales
    where total_sales > 0  -- Only forecast periods with demand
    
),

forecast_accuracy as (
    
    select
        item_id,
        store_id,
        date,
        actual_sales,
        forecast_sales,
        
        -- KPI 1: Absolute Error
        abs(actual_sales - forecast_sales) as absolute_error,
        
        -- KPI 2: Percentage Error
        case 
            when actual_sales > 0 
            then abs(actual_sales - forecast_sales) / actual_sales 
            else 0 
        end as percentage_error,
        
        -- KPI 3: Bias (forecast - actual)
        forecast_sales - actual_sales as forecast_bias,
        
        -- KPI 4: Squared Error
        power(actual_sales - forecast_sales, 2) as squared_error
        
    from forecast_mock
    
),

aggregated_accuracy as (
    
    select
        item_id,
        store_id,
        
        -- Volume
        count(*) as forecast_periods,
        sum(actual_sales) as total_actual_sales,
        sum(forecast_sales) as total_forecast_sales,
        
        -- KPI 5: MAE (Mean Absolute Error)
        avg(absolute_error) as mae,
        
        -- KPI 6: MAPE (Mean Absolute Percentage Error)
        avg(percentage_error) as mape,
        
        -- KPI 7: Forecast Bias
        avg(forecast_bias) as avg_bias,
        sum(forecast_bias) as total_bias,
        
        -- KPI 8: Bias % (total bias / total actual)
        case 
            when sum(actual_sales) > 0 
            then sum(forecast_bias) / sum(actual_sales) 
            else 0 
        end as bias_pct,
        
        -- KPI 9: RMSE (Root Mean Squared Error)
        sqrt(avg(squared_error)) as rmse,
        
        -- KPI 10: Tracking Signal (cumulative bias / MAE)
        case 
            when avg(absolute_error) > 0 
            then sum(forecast_bias) / avg(absolute_error) 
            else 0 
        end as tracking_signal,
        
        current_timestamp as calculated_at
        
    from forecast_accuracy
    group by item_id, store_id
    
),

-- Accuracy classification
accuracy_classification as (
    
    select
        *,
        
        -- MAPE categories
        case
            when mape < 0.10 then 'Excellent'  -- <10% error
            when mape < 0.15 then 'Good'        -- 10-15% error
            when mape < 0.25 then 'Fair'        -- 15-25% error
            else 'Poor'                         -- >25% error
        end as accuracy_category,
        
        -- Bias direction
        case
            when abs(bias_pct) < 0.05 then 'Unbiased'  -- Within ±5%
            when bias_pct > 0 then 'Over-forecasting'
            else 'Under-forecasting'
        end as bias_direction
        
    from aggregated_accuracy
    
)

select * from accuracy_classification
