"""
K-Means Clustering for Inventory Segmentation
==============================================

This module implements K-means clustering to segment 3.5M+ SKU-store
combinations into 8-12 distinct clusters based on:
- Revenue contribution (ABC)
- Demand variability (CV)
- Seasonality strength
- Trend presence
- Stockout frequency
- Supplier reliability
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
from typing import Dict, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InventorySegmentation:
    """
    K-means clustering for inventory segmentation.
    
    Segments SKU-store combinations into clusters based on multiple
    demand and supply characteristics.
    """
    
    def __init__(
        self,
        n_clusters: int = 8,
        random_state: int = 42
    ):
        """
        Initialize inventory segmentation.
        
        Parameters
        ----------
        n_clusters : int, default=8
            Number of clusters (8-12 recommended)
        random_state : int, default=42
            Random seed for reproducibility
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.kmeans = None
        self.feature_names = None
        
        logger.info(f"Initialized InventorySegmentation with {n_clusters} clusters")
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer features for clustering.
        
        Parameters
        ----------
        df : pd.DataFrame
            Input data with sales history
            
        Returns
        -------
        pd.DataFrame
            Feature matrix for clustering
        """
        logger.info("Preparing clustering features...")
        
        features = pd.DataFrame()
        
        # Feature 1: Annual revenue contribution (ABC classification)
        features['revenue_contribution'] = df.groupby(['item_id', 'store_id'])['revenue'].sum()
        
        # Feature 2: Demand coefficient of variation (XYZ classification)
        demand_stats = df.groupby(['item_id', 'store_id'])['sales'].agg(['mean', 'std'])
        features['demand_cv'] = demand_stats['std'] / demand_stats['mean']
        features['demand_cv'] = features['demand_cv'].fillna(0).replace([np.inf, -np.inf], 0)
        
        # Feature 3: Seasonality strength (FFT analysis)
        features['seasonality_strength'] = self._calculate_seasonality_strength(df)
        
        # Feature 4: Trend slope (linear regression)
        features['trend_slope'] = self._calculate_trend_slope(df)
        
        # Feature 5: Stockout frequency
        features['stockout_frequency'] = self._calculate_stockout_frequency(df)
        
        # Feature 6: Supplier reliability score (mock - would come from data)
        features['supplier_reliability'] = np.random.uniform(0.7, 1.0, size=len(features))
        
        # Clean features
        features = features.fillna(0)
        features = features.replace([np.inf, -np.inf], 0)
        
        logger.info(f"Prepared {len(features):,} SKU-store combinations")
        logger.info(f"Features: {list(features.columns)}")
        
        return features
    
    def _calculate_seasonality_strength(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate seasonality strength using FFT.
        
        Returns value between 0 (no seasonality) and 1 (strong seasonality).
        """
        # Simplified implementation - in production, use FFT
        seasonal_cv = df.groupby(['item_id', 'store_id', df['date'].dt.month])['sales'].mean().groupby(level=[0, 1]).std()
        overall_mean = df.groupby(['item_id', 'store_id'])['sales'].mean()
        seasonality = (seasonal_cv / overall_mean).fillna(0)
        
        return seasonality.clip(0, 1)
    
    def _calculate_trend_slope(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate trend slope using linear regression.
        
        Returns slope coefficient normalized to [-1, 1].
        """
        from scipy.stats import linregress
        
        def calculate_slope(group):
            if len(group) < 10:
                return 0
            x = np.arange(len(group))
            y = group['sales'].values
            slope, _, _, _, _ = linregress(x, y)
            return slope
        
        slopes = df.groupby(['item_id', 'store_id']).apply(calculate_slope)
        
        # Normalize slopes
        slopes = slopes / (slopes.abs().max() + 1e-10)
        
        return slopes.fillna(0)
    
    def _calculate_stockout_frequency(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate stockout frequency.
        
        Returns proportion of days with zero sales (proxy for stockouts).
        """
        stockouts = (df.groupby(['item_id', 'store_id'])['sales'] == 0).groupby(level=[0, 1]).mean()
        
        return stockouts.fillna(0)
    
    def fit(self, features: pd.DataFrame) -> 'InventorySegmentation':
        """
        Fit K-means clustering model.
        
        Parameters
        ----------
        features : pd.DataFrame
            Feature matrix
            
        Returns
        -------
        self
            Fitted model
        """
        logger.info("Fitting K-means clustering...")
        
        self.feature_names = features.columns.tolist()
        
        # Standardize features
        features_scaled = self.scaler.fit_transform(features)
        
        # Fit K-means
        self.kmeans = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=10,
            max_iter=300
        )
        
        self.kmeans.fit(features_scaled)
        
        # Calculate quality metrics
        silhouette = silhouette_score(features_scaled, self.kmeans.labels_)
        davies_bouldin = davies_bouldin_score(features_scaled, self.kmeans.labels_)
        
        logger.info(f"✅ Clustering completed")
        logger.info(f"   Silhouette Score: {silhouette:.3f} (higher is better)")
        logger.info(f"   Davies-Bouldin Score: {davies_bouldin:.3f} (lower is better)")
        
        return self
    
    def predict(self, features: pd.DataFrame) -> np.ndarray:
        """
        Assign clusters to new data.
        
        Parameters
        ----------
        features : pd.DataFrame
            Feature matrix
            
        Returns
        -------
        np.ndarray
            Cluster assignments
        """
        features_scaled = self.scaler.transform(features)
        return self.kmeans.predict(features_scaled)
    
    def assign_business_labels(self, features: pd.DataFrame, clusters: np.ndarray) -> pd.Series:
        """
        Assign business-friendly labels to clusters.
        
        Parameters
        ----------
        features : pd.DataFrame
            Feature matrix
        clusters : np.ndarray
            Cluster assignments
            
        Returns
        -------
        pd.Series
            Business labels
        """
        # Calculate cluster statistics
        cluster_df = features.copy()
        cluster_df['cluster'] = clusters
        
        cluster_stats = cluster_df.groupby('cluster').agg({
            'revenue_contribution': 'mean',
            'demand_cv': 'mean',
            'seasonality_strength': 'mean',
            'trend_slope': 'mean'
        })
        
        # Assign labels based on characteristics
        labels = {}
        
        for cluster in range(self.n_clusters):
            stats = cluster_stats.loc[cluster]
            
            # Determine label components
            if stats['revenue_contribution'] > cluster_stats['revenue_contribution'].quantile(0.67):
                value_label = "Premium"
            elif stats['revenue_contribution'] > cluster_stats['revenue_contribution'].quantile(0.33):
                value_label = "Mid-Tier"
            else:
                value_label = "Budget"
            
            if stats['demand_cv'] < 0.5:
                stability_label = "Stable"
            elif stats['demand_cv'] < 1.0:
                stability_label = "Moderate"
            else:
                stability_label = "Volatile"
            
            labels[cluster] = f"{value_label}-{stability_label}"
        
        # Map clusters to labels
        label_series = pd.Series(clusters).map(labels)
        
        return label_series
    
    def profile_clusters(self, features: pd.DataFrame, clusters: np.ndarray) -> pd.DataFrame:
        """
        Generate cluster profile report.
        
        Parameters
        ----------
        features : pd.DataFrame
            Feature matrix
        clusters : np.ndarray
            Cluster assignments
            
        Returns
        -------
        pd.DataFrame
            Cluster profiles
        """
        cluster_df = features.copy()
        cluster_df['cluster'] = clusters
        
        # Get business labels
        cluster_df['business_label'] = self.assign_business_labels(features, clusters)
        
        # Calculate profiles
        profiles = cluster_df.groupby(['cluster', 'business_label']).agg({
            'revenue_contribution': ['mean', 'std', 'count'],
            'demand_cv': ['mean', 'std'],
            'seasonality_strength': 'mean',
            'trend_slope': 'mean',
            'stockout_frequency': 'mean'
        }).round(3)
        
        profiles.columns = ['_'.join(col).strip() for col in profiles.columns.values]
        
        return profiles


def main():
    """
    Example usage of inventory segmentation.
    """
    print("="*70)
    print("K-MEANS CLUSTERING - INVENTORY SEGMENTATION")
    print("="*70)
    print()
    
    # Load sample data (in production, load from gold layer)
    logger.info("Loading sample data...")
    
    # Generate synthetic data for demonstration
    np.random.seed(42)
    n_samples = 1000
    
    sample_data = pd.DataFrame({
        'item_id': [f'ITEM_{i:04d}' for i in range(n_samples)],
        'store_id': np.random.choice(['CA_1', 'CA_2', 'TX_1', 'WI_1'], n_samples),
        'revenue': np.random.lognormal(10, 2, n_samples),
        'sales': np.random.poisson(50, n_samples),
        'date': pd.date_range('2024-01-01', periods=365, freq='D').tolist() * (n_samples // 365 + 1)
    })
    sample_data = sample_data.iloc[:n_samples]
    sample_data['date'] = pd.to_datetime(sample_data['date'])
    
    # Initialize segmentation
    segmenter = InventorySegmentation(n_clusters=8)
    
    # Prepare features
    features = segmenter.prepare_features(sample_data)
    
    # Fit model
    segmenter.fit(features)
    
    # Assign clusters
    clusters = segmenter.predict(features)
    
    # Generate profiles
    profiles = segmenter.profile_clusters(features, clusters)
    
    print()
    print("📊 CLUSTER PROFILES")
    print("-"*70)
    print(profiles)
    print()
    
    # Cluster distribution
    unique, counts = np.unique(clusters, return_counts=True)
    print("📈 CLUSTER DISTRIBUTION")
    print("-"*70)
    for cluster, count in zip(unique, counts):
        print(f"  Cluster {cluster}: {count:,} SKU-stores ({count/len(clusters)*100:.1f}%)")
    
    print()
    print("✅ Clustering completed successfully!")


if __name__ == "__main__":
    main()
