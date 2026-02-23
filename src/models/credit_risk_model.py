"""Credit risk prediction models."""
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path('/Users/phillipsmith/Desktop/pythonProjects/real-time-credit-risk-simulation')
MODELING_PATH = PROJECT_ROOT / 'src' / 'data' / 'processed' / 'modeling_df.parquet'


def load_modeling_data() -> pd.DataFrame:
    """Load the modeling-ready DataFrame."""
    if not MODELING_PATH.exists():
        raise FileNotFoundError(f"Run pipeline first: python -m src.pipeline")
    return pd.read_parquet(MODELING_PATH, engine='fastparquet')


# TODO: Implement classifier
# class CreditRiskClassifier:
#     def __init__(self):
#         self.model = LogisticRegression()
#     def train(self, X, y):
#         self.model.fit(X, y)
#     def predict(self, X):
#         return self.model.predict(X)