# 📊 Repository 02: Supply Chain Analytics Intelligence

> **"The Business Translator"** - Transforming data into actionable insights through clustering, KPI calculations, and exploratory analysis

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![dbt](https://img.shields.io/badge/dbt-1.6+-orange?logo=dbt)](https://www.getdbt.com/)
[![Status](https://img.shields.io/badge/Status-In_Development-yellow.svg)]()

---

## 🎯 Purpose

This repository implements **supply chain analytics intelligence** that bridges raw data and ML models. It consumes clean data from the Data Engineering layer and produces:
- **Inventory Segmentation:** K-means clustering on 3.5M+ SKU-store combinations
- **Business KPIs:** 100+ metrics (inventory turns, fill rates, service levels)
- **Demand Pattern Analysis:** Seasonality, trends, variability characterization
- **Business Glossary:** Metric definitions for cross-functional alignment

## 🧠 Core Capabilities

```
┌─────────────────────────────────────────────────────────────────┐
│  SUPPLY CHAIN ANALYTICS INTELLIGENCE                             │
└─────────────────────────────────────────────────────────────────┘

  INPUTS: Gold Layer Data from Repository 01
  ├── daily_sales_agg (3.5M SKU-stores)
  ├── weekly_demand_patterns
  ├── inventory_metrics
  └── warehouse_performance

          ↓

┌──────────────────────────┐
│  K-MEANS CLUSTERING      │  3.5M SKU-Store Segmentation
├──────────────────────────┤
│ Features:                │  • Revenue contribution (ABC)
│ • Annual revenue         │  • Demand variability (CV)
│ • Demand CV              │  • Seasonality strength (FFT)
│ • Seasonality strength   │  • Trend presence (slope)
│ • Trend slope            │  • Stockout frequency
│ • Stockout frequency     │  • Supplier reliability
│ • Supplier reliability   │
├──────────────────────────┤
│ Output: 8-12 Clusters    │
│ • Premium-Stable         │
│ • Budget-Erratic         │
│ • Seasonal-Mid-Tier      │
│ • High-Volume-Volatile   │
│ • Low-Volume-Steady      │
│ • Clearance-Intermittent │
│ • New-Products           │
│ • Promotional-Surge      │
└──────────────────────────┘

          ↓

┌──────────────────────────┐
│  SQL QUERY LIBRARY       │  100+ Business Metrics
├──────────────────────────┤
│ Inventory Metrics:       │  • Inventory turnover
│ • Days of supply         │  • Stock-to-sales ratio
│ • Fill rate              │  • Carrying cost
│ • Service level          │
├──────────────────────────┤
│ Demand Metrics:          │  • Forecast accuracy (MAPE)
│ • Demand volatility      │  • Bias analysis
│ • Seasonality index      │  • Demand classification
├──────────────────────────┤
│ Supply Metrics:          │  • Supplier OTIF
│ • Lead time variability  │  • Warehouse utilization
│ • Order fulfillment rate │  • Transportation cost/unit
└──────────────────────────┘

          ↓

┌──────────────────────────┐
│  DBT MODELS             │  Analytics Engineering
├──────────────────────────┤
│ • Silver → Analytics     │  • Tested transformations
│ • Incremental processing │  • Documentation
│ • Data quality tests     │  • Version control
│ • Lineage tracking       │
└──────────────────────────┘

          ↓

  OUTPUTS: Analytics Layer
  ├── cluster_assignments (SKU-store → cluster)
  ├── kpi_calculations (100+ metrics)
  ├── demand_pattern_classifications
  └── business_glossary

          ↓

    [ML Models] [BI Dashboards] [Stakeholders]
```

---

## 🗂️ Repository Structure

```
02-supply-chain-analytics/
├── sql/                              # SQL query library
│   ├── kpis/
│   │   ├── inventory_metrics.sql
│   │   ├── demand_metrics.sql
│   │   ├── supply_metrics.sql
│   │   └── financial_metrics.sql
│   ├── aggregations/
│   │   ├── daily_summary.sql
│   │   ├── weekly_rollup.sql
│   │   └── monthly_trends.sql
│   └── analysis/
│       ├── abc_analysis.sql
│       ├── seasonality_detection.sql
│       └── trend_analysis.sql
│
├── dbt/                              # Analytics engineering
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   ├── tests/
│   ├── macros/
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── notebooks/                        # Exploratory analysis
│   ├── clustering/
│   │   ├── 01_feature_engineering.ipynb
│   │   ├── 02_kmeans_clustering.ipynb
│   │   ├── 03_cluster_profiling.ipynb
│   │   └── 04_cluster_validation.ipynb
│   ├── demand_patterns/
│   │   ├── 01_seasonality_analysis.ipynb
│   │   ├── 02_trend_detection.ipynb
│   │   └── 03_variability_study.ipynb
│   ├── warehouse_analysis/
│   │   ├── 01_utilization_heatmaps.ipynb
│   │   └── 02_efficiency_benchmarks.ipynb
│   └── supplier_performance/
│       ├── 01_otif_analysis.ipynb
│       └── 02_lead_time_variability.ipynb
│
├── src/
│   ├── clustering/
│   │   ├── __init__.py
│   │   ├── feature_engineer.py
│   │   ├── kmeans_segmenter.py
│   │   ├── cluster_profiler.py
│   │   └── business_labeler.py
│   ├── pattern_detection/
│   │   ├── __init__.py
│   │   ├── seasonality_detector.py
│   │   ├── trend_analyzer.py
│   │   └── variability_classifier.py
│   ├── kpi_calculators/
│   │   ├── __init__.py
│   │   ├── inventory_kpis.py
│   │   ├── demand_kpis.py
│   │   ├── supply_kpis.py
│   │   └── financial_kpis.py
│   └── utils/
│       ├── __init__.py
│       ├── sql_executor.py
│       └── data_loader.py
│
├── docs/
│   ├── business_glossary.md          # Metric definitions
│   ├── cluster_interpretation.md     # Cluster business meaning
│   ├── kpi_catalog.md                # All KPI documentation
│   └── sql_query_reference.md        # SQL query guide
│
├── tests/
│   ├── test_clustering.py
│   ├── test_kpi_calculations.py
│   └── test_pattern_detection.py
│
├── config/
│   ├── clustering_config.yaml
│   └── kpi_definitions.yaml
│
├── .gitignore
├── README.md                         # This file
├── requirements.txt
└── setup.py
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- dbt 1.6+
- Access to gold layer data (Repository 01)
- PostgreSQL or Snowflake

### Installation

```bash
# Navigate to repository
cd 02-supply-chain-analytics

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install dbt
pip install dbt-postgres  # or dbt-snowflake

# Configure dbt
dbt init
dbt debug

# Test dbt models
dbt run
dbt test
```

### Run Clustering

```bash
# Run K-means clustering
python src/clustering/kmeans_segmenter.py

# Profile clusters
python src/clustering/cluster_profiler.py

# Or use Jupyter
jupyter notebook notebooks/clustering/02_kmeans_clustering.ipynb
```

---

## 🧮 K-Means Clustering

### Features Used (6 dimensions)

1. **Annual Revenue Contribution** - Pareto principle (ABC)
2. **Demand Coefficient of Variation** - Volatility (XYZ)
3. **Seasonality Strength** - FFT amplitude analysis
4. **Trend Slope** - Linear regression coefficient
5. **Stockout Frequency** - Availability issues
6. **Supplier Reliability Score** - OTIF performance

### Expected Clusters (8-12)

| Cluster | Description | % of SKUs | Strategy |
|---------|-------------|-----------|----------|
| **Premium-Stable** | High-value, predictable demand | 5% | Continuous review, 99.5% service level |
| **Budget-Erratic** | Low-value, volatile demand | 15% | Periodic review, 90% service level |
| **Seasonal-Mid-Tier** | Moderate value, seasonal peaks | 12% | Seasonal buffers, 95% service level |
| **High-Volume-Volatile** | High sales, high variability | 8% | Extra safety stock, 98% service level |
| **Low-Volume-Steady** | Low but consistent sales | 25% | Loose control, 92% service level |
| **Clearance-Intermittent** | Sporadic demand, end-of-life | 10% | Make-to-order, 85% service level |
| **New-Products** | Insufficient history | 5% | Conservative forecasts, 94% service |
| **Promotional-Surge** | Promotion-driven demand | 20% | Event-based planning, 96% service |

---

## 📊 KPI Library (100+ Metrics)

### Inventory KPIs
- **Inventory Turnover** = COGS / Average Inventory
- **Days of Supply** = Current Inventory / Average Daily Demand
- **Fill Rate** = Orders Fulfilled / Total Orders
- **Service Level** = 1 - (Stockouts / Total Opportunities)
- **Stock-to-Sales Ratio** = Inventory Value / Sales Value
- **Carrying Cost %** = Holding Cost / Inventory Value

### Demand KPIs
- **Forecast Accuracy (MAPE)** = Mean(|Actual - Forecast| / Actual) × 100
- **Forecast Bias** = Mean(Forecast - Actual)
- **Demand Volatility (CV)** = Std Dev / Mean
- **Seasonality Index** = Period Demand / Average Demand

### Supply KPIs
- **Supplier OTIF** = On-Time & In-Full Deliveries %
- **Lead Time Variability** = Std Dev of Lead Times
- **Order Fulfillment Rate** = Complete Orders / Total Orders
- **Warehouse Utilization** = Used Capacity / Total Capacity

### Financial KPIs
- **Revenue per SKU** = Total Revenue / SKU Count
- **Gross Margin %** = (Revenue - COGS) / Revenue
- **Obsolescence Rate** = Obsolete Inventory / Total Inventory

---

## 🔍 Demand Pattern Analysis

### Pattern Types

1. **SMOOTH** - Low CV (<0.5), no seasonality
2. **SEASONAL** - Strong seasonality (FFT amplitude >threshold)
3. **TRENDING** - Significant linear trend (R² >0.3)
4. **LUMPY** - High CV (>1.0), low ADI (<1.32)
5. **INTERMITTENT** - High ADI (>1.32), low CV
6. **ERRATIC** - High CV + High ADI
7. **NEW** - <90 days history

### Analysis Outputs

- **Seasonality Strength** (0-1 scale)
- **Trend Direction** (UPWARD/DOWNWARD/FLAT)
- **Coefficient of Variation**
- **Average Demand Interval (ADI)**
- **Recommended Forecasting Method**

---

## 🛠️ dbt Models

### Staging Layer
- `stg_sales` - Cleaned sales from gold layer
- `stg_inventory` - Clean inventory snapshots
- `stg_shipments` - Logistics data

### Intermediate Layer
- `int_demand_features` - Engineered demand features
- `int_inventory_calcs` - Calculated inventory metrics
- `int_supplier_scores` - Supplier performance

### Marts Layer
- `mart_cluster_assignments` - Final SKU-cluster mapping
- `mart_kpi_dashboard` - All KPIs for BI
- `mart_demand_patterns` - Pattern classifications

---

## 📚 Business Glossary

**Purpose:** Define every metric in business terms for stakeholder alignment

Example entries:
- **Inventory Turnover:** Number of times inventory is sold and replaced per year. Higher = better capital efficiency.
- **Fill Rate:** Percentage of customer orders fulfilled from available stock. Target: 95%+
- **MAPE:** Mean Absolute Percentage Error - forecast accuracy metric. Lower = better. Target: <15%

See [docs/business_glossary.md](docs/business_glossary.md) for complete glossary.

---

## 🔗 Integration Points

### Consumes From (Repository 01)
- `gold/daily_sales_agg/`
- `gold/weekly_demand_patterns/`
- `gold/inventory_metrics/`
- `gold/warehouse_performance/`

### Produces For (Repositories 03 & 04)
- `analytics/cluster_assignments/`
- `analytics/kpi_calculations/`
- `analytics/demand_pattern_classifications/`

---

## 📈 Performance

- **Clustering Time:** 10 minutes for 3.5M SKU-stores
- **KPI Calculation:** 5 minutes for 100+ metrics
- **dbt Models:** 15 minutes full refresh, 2 minutes incremental

---

## 🛠️ Technologies

- **Language:** Python 3.9+, SQL
- **Analytics Engineering:** dbt
- **ML:** Scikit-learn (K-means)
- **Notebooks:** Jupyter
- **Visualization:** Matplotlib, Seaborn, Plotly

---

## 📞 Support

**Maintained by:** Supply Chain Analytics Team  
**Contact:** godson.kurishinkal@gmail.com

---

**Status:** 🚧 Implementation Phase 3  
**Last Updated:** November 23, 2025  
**Version:** 1.0.0
