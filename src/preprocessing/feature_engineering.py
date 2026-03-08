"""Feature engineering for credit risk analysis."""
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer


class FeatureEngineer:
    """Transforms raw data into model-ready features."""
    
    SEVERITY_WEIGHTS = {'low': 1, 'med': 2, 'high': 3}
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        
    def apply_log_transforms(self) -> 'FeatureEngineer':
        """Log1p transform skewed columns."""
        log_columns = {
            'monthly_revenue': 'monthly_revenue_log',
            'debt_ratio': 'debt_ratio_log',
            'rated_exposure': 'rated_exposure_log'
        }
        for orig_col, log_col in log_columns.items():
            if orig_col in self.df.columns:
                self.df[log_col] = np.log1p(self.df[orig_col])
        return self
    
    def calculate_overdue_severity(self) -> 'FeatureEngineer':
        """Weighted severity score from delinquency indicators."""
        w = self.SEVERITY_WEIGHTS
        self.df['overdue_severity'] = (
            (self.df['overdue_30_59_days'] * w['low']) +
            (self.df['overdue_60_89_days'] * w['med']) +
            (self.df['overdue_90_plus_days'] * w['high'])
        )
        self.df['overdue_severity_log'] = np.log1p(self.df['overdue_severity'])
        return self
    
    def normalize_age(self) -> 'FeatureEngineer':
        """Normalize age to 0-1 range."""
        self.df['age_normalized'] = (self.df['age'] - self.df['age'].min()) / (self.df['age'].max() - self.df['age'].min())
        return self
    
    def impute_missing_with_knn(self, n_neighbors: int = 5) -> 'FeatureEngineer':
        """KNN imputation for missing values."""
        impute_vars = ['monthly_revenue_log', 'rated_exposure_log', 'age_normalized']
        existing_vars = [col for col in impute_vars if col in self.df.columns]
        if existing_vars:
            imputer = KNNImputer(n_neighbors=n_neighbors)
            self.df[existing_vars] = imputer.fit_transform(self.df[existing_vars])
        return self
    
    def calculate_business_scale(self) -> 'FeatureEngineer':
        """Composite business scale score."""
        self.df['business_scale'] = (
            (0.5 * self.df['monthly_revenue_log']) +
            (0.4 * self.df['rated_exposure_log']) +
            (0.1 * self.df['age_normalized'])
        )
        self.df['business_tier'] = pd.qcut(self.df['business_scale'], q=4, labels=['small', 'medium', 'large', 'enterprise'])
        return self
    
    def detect_outliers_iqr(self) -> 'FeatureEngineer':
        """IQR-based outlier flags."""
        outlier_columns = {
            'monthly_revenue': 'revenue_outlier',
            'debt_ratio': 'debt_ratio_outlier',
            'rated_exposure': 'rated_exposure_outlier',
            'overdue_severity': 'overdue_severity_outlier'
        }
        for orig_col, outlier_col in outlier_columns.items():
            if orig_col in self.df.columns:
                Q1, Q3 = self.df[orig_col].quantile(0.25), self.df[orig_col].quantile(0.75)
                IQR = Q3 - Q1
                self.df[outlier_col] = ((self.df[orig_col] < Q1 - 1.5*IQR) | (self.df[orig_col] > Q3 + 1.5*IQR)).astype(int)
        return self
    
    def get_dataframe(self) -> pd.DataFrame:
        return self.df
    
    def get_modeling_dataframe(self) -> pd.DataFrame:
        """Return only modeling columns."""
        modeling_columns = [
            'age_normalized', 'monthly_revenue_log', 'debt_ratio_log', 'rated_exposure_log',
            'overdue_severity', 'revenue_missing', 'debt_ratio_missing', 'rated_exposure_missing',
            'revenue_outlier', 'debt_ratio_outlier', 'rated_exposure_outlier', 'overdue_severity_outlier',
            'business_scale', 'serious_delinquencies_past_2_years'
        ]
        existing = [col for col in modeling_columns if col in self.df.columns]
        return self.df[existing].copy()


def engineer_features(df: pd.DataFrame, n_neighbors: int = 5) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply all feature engineering. Returns (full_df, modeling_df)."""
    engineer = FeatureEngineer(df)
    engineer.apply_log_transforms()
    engineer.calculate_overdue_severity()
    engineer.normalize_age()
    engineer.impute_missing_with_knn(n_neighbors=n_neighbors)
    engineer.calculate_business_scale()
    engineer.detect_outliers_iqr()
    return engineer.get_dataframe(), engineer.get_modeling_dataframe()
