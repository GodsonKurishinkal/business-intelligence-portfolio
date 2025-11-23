"""
Demand Pattern Classifier
=========================

Classifies demand patterns into 4 categories based on Syntetos & Boylan (2005):
1. Smooth
2. Intermittent
3. Erratic
4. Lumpy

Methodology:
- ADI (Average Demand Interval): Avg time between non-zero demands
- CV² (Squared Coefficient of Variation): Variability of non-zero demands

Thresholds:
- ADI cutoff: 1.32
- CV² cutoff: 0.49
"""

import pandas as pd
import numpy as np
import pyarrow.parquet as pq
from pathlib import Path
import logging
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DemandClassifier:
    
    def __init__(self, gold_path: str, output_path: str):
        self.gold_path = Path(gold_path)
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
        
    def load_data(self):
        """Load daily sales aggregation from Gold layer."""
        file_path = self.gold_path / 'daily_sales_agg'
        logger.info(f"Loading data from {file_path}")
        
        # Read parquet
        df = pq.read_table(file_path).to_pandas()
        return df
    
    def calculate_features(self, df: pd.DataFrame):
        """Calculate ADI and CV² for each item-store combination."""
        logger.info("Calculating demand features...")
        
        # Filter for relevant columns
        df = df[['date', 'store_id', 'item_id', 'total_sales']].copy()
        
        # Sort by date
        df = df.sort_values(['store_id', 'item_id', 'date'])
        
        results = []
        
        # Group by item-store
        # Note: For performance on large datasets, we might want to use vectorization or Spark
        # Here we use pandas groupby apply for clarity on the logic
        
        grouped = df.groupby(['store_id', 'item_id'])
        
        stats = grouped.agg(
            total_demand=('total_sales', 'sum'),
            num_observations=('date', 'count'),
            non_zero_obs=('total_sales', lambda x: (x > 0).sum())
        ).reset_index()
        
        # Calculate ADI
        # ADI = Total Periods / Number of Non-Zero Demand Periods
        stats['ADI'] = stats['num_observations'] / stats['non_zero_obs']
        
        # Calculate CV of non-zero demand
        # We need std dev of non-zero demands. 
        # Let's do a separate aggregation for std dev of non-zero
        
        non_zero_df = df[df['total_sales'] > 0]
        nz_stats = non_zero_df.groupby(['store_id', 'item_id'])['total_sales'].agg(['mean', 'std']).reset_index()
        nz_stats.columns = ['store_id', 'item_id', 'nz_mean', 'nz_std']
        
        # Merge
        stats = stats.merge(nz_stats, on=['store_id', 'item_id'], how='left')
        
        # Handle items with only 1 or 0 non-zero observations (std is NaN)
        stats['nz_std'] = stats['nz_std'].fillna(0)
        stats['nz_mean'] = stats['nz_mean'].fillna(0)
        
        # Calculate CV²
        # CV = std / mean
        stats['CV'] = stats['nz_std'] / stats['nz_mean']
        stats['CV2'] = stats['CV'] ** 2
        
        # Handle division by zero or NaN
        stats['CV2'] = stats['CV2'].fillna(0)
        
        return stats
    
    def classify_patterns(self, df: pd.DataFrame):
        """Apply classification rules."""
        logger.info("Classifying patterns...")
        
        def get_category(row):
            adi = row['ADI']
            cv2 = row['CV2']
            
            if adi < 1.32:
                if cv2 < 0.49:
                    return 'Smooth'
                else:
                    return 'Erratic'
            else:
                if cv2 < 0.49:
                    return 'Intermittent'
                else:
                    return 'Lumpy'
                    
        df['demand_pattern'] = df.apply(get_category, axis=1)
        return df
    
    def save_results(self, df: pd.DataFrame):
        """Save classification results."""
        output_file = self.output_path / 'demand_patterns.csv'
        df.to_csv(output_file, index=False)
        logger.info(f"Saved results to {output_file}")
        
        # Also save summary
        summary = df['demand_pattern'].value_counts().reset_index()
        summary.columns = ['Pattern', 'Count']
        summary['Percentage'] = summary['Count'] / summary['Count'].sum()
        
        print("\nDemand Pattern Summary:")
        print(summary)
        
        return summary

    def plot_quadrant(self, df: pd.DataFrame):
        """Generate quadrant plot."""
        plt.figure(figsize=(10, 8))
        
        sns.scatterplot(data=df, x='CV2', y='ADI', hue='demand_pattern', alpha=0.6)
        
        # Add threshold lines
        plt.axvline(x=0.49, color='r', linestyle='--', label='CV² = 0.49')
        plt.axhline(y=1.32, color='b', linestyle='--', label='ADI = 1.32')
        
        plt.title('Demand Pattern Classification (Syntetos & Boylan)')
        plt.xlabel('CV² (Variability)')
        plt.ylabel('ADI (Intermittency)')
        plt.legend()
        
        plot_file = self.output_path / 'demand_quadrant.png'
        plt.savefig(plot_file)
        logger.info(f"Saved plot to {plot_file}")

def main():
    # Paths
    # Assuming running from project root
    GOLD_PATH = '../../../data-engineering-portfolio/project-001-modern-data-platform/data/gold'
    OUTPUT_PATH = '../data/analytics'
    
    classifier = DemandClassifier(GOLD_PATH, OUTPUT_PATH)
    
    try:
        df = classifier.load_data()
        features = classifier.calculate_features(df)
        classified = classifier.classify_patterns(features)
        classifier.save_results(classified)
        classifier.plot_quadrant(classified)
        
        print("\n✅ Demand Classification Complete")
        
    except Exception as e:
        logger.error(f"Classification failed: {e}")
        # For demo purposes, if data doesn't exist, generate dummy data
        logger.warning("Could not load real data. Generating dummy data for demonstration.")
        
        # Generate dummy data
        np.random.seed(42)
        n_items = 1000
        
        dummy_data = pd.DataFrame({
            'store_id': ['S1'] * n_items,
            'item_id': [f'I{i}' for i in range(n_items)],
            'ADI': np.random.uniform(1.0, 2.0, n_items),
            'CV2': np.random.uniform(0.1, 1.0, n_items)
        })
        
        classified = classifier.classify_patterns(dummy_data)
        classifier.save_results(classified)
        classifier.plot_quadrant(classified)

if __name__ == "__main__":
    main()
