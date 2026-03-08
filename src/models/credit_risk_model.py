"""Credit risk prediction models."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, roc_curve

PROJECT_ROOT = Path('/Users/phillipsmith/Desktop/pythonProjects/real-time-credit-risk-simulation')
MODELING_PATH = PROJECT_ROOT / 'src' / 'data' / 'processed' / 'modeling_df.parquet'

def load_modeling_data() -> pd.DataFrame:
    """Load the modeling-ready DataFrame."""
    if not MODELING_PATH.exists():
        raise FileNotFoundError(f"Run pipeline first: python -m src.pipeline")
    return pd.read_parquet(MODELING_PATH, engine='fastparquet')

class CreditRiskClassifier:
    """Logistic regression classifier for credit risk prediction."""
    
    def __init__(self, test_size: float = 0.5, random_state: int = 24):
        self.test_size = test_size
        self.random_state = random_state
        self.feature_cols = [
            'age_normalized',
            'monthly_revenue_log',
            'debt_ratio_log',
            'rated_exposure_log',
            'revenue_missing',
            'debt_ratio_missing',
            'rated_exposure_missing',
            'revenue_outlier',
            'debt_ratio_outlier',
            'rated_exposure_outlier'
        ]
        self.model = LogisticRegression(
            random_state=self.random_state,
            class_weight='balanced',
            max_iter=1000
        )
        self.X_train = self.X_test = self.y_train = self.y_test = None
        self.y_pred = self.cnf_matrix = None

    def prepare_data(self, modeling_df: pd.DataFrame = None):
        """Prepare features/target and split into train/test sets."""
        if modeling_df is None:
            modeling_df = load_modeling_data()
        
        modeling_df = modeling_df.copy()
        modeling_df['default_flag'] = (modeling_df['serious_delinquencies_past_2_years'] > 0).astype(int)
        
        X = modeling_df[self.feature_cols]
        Y = modeling_df['default_flag']
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, Y, test_size=self.test_size, random_state=self.random_state
        )
        return self

    def train(self):
        """Train the model on training data."""
        if self.X_train is None:
            raise ValueError("Call prepare_data() first")
        self.model.fit(self.X_train, self.y_train)
        return self

    def predict(self, X: pd.DataFrame = None):
        """Generate predictions on test data or provided data."""
        self.y_pred = self.model.predict(X if X is not None else self.X_test)
        return self.y_pred

    def evaluate(self, plot: bool = False):
        """Return confusion matrix, optionally plot as heatmap."""
        if self.y_pred is None:
            self.predict()
        self.cnf_matrix = confusion_matrix(self.y_test, self.y_pred)
        
        if plot:
            class_names = [0, 1]
            fig, ax = plt.subplots()
            tick_marks = np.arange(len(class_names))
            plt.xticks(tick_marks, class_names)
            plt.yticks(tick_marks, class_names)
            sns.heatmap(pd.DataFrame(self.cnf_matrix), annot=True, cmap="YlGnBu", fmt='g')
            ax.xaxis.set_label_position("top")
            plt.tight_layout()
            plt.title('Confusion Matrix', y=1.1)
            plt.ylabel('Actual label')
            plt.xlabel('Predicted label')
        
        return self.cnf_matrix

    def get_classification_report(self, as_dict: bool = False):
        """Return classification metrics."""
        if self.y_pred is None:
            self.predict()
        return classification_report(
            self.y_test, self.y_pred,
            target_names=['no default', 'default'],
            output_dict=as_dict
        )

    def fit_and_evaluate(self, modeling_df: pd.DataFrame = None):
        """Run full pipeline: prepare, train, predict, evaluate."""
        self.prepare_data(modeling_df)
        self.train()
        self.predict()
        return self.evaluate()

    def plot_roc_curve(self):
        """Plot ROC curve with AUC score."""
        if self.y_pred is None:
            self.predict()
        
        y_pred_proba = self.model.predict_proba(self.X_test)[:, 1]
        fpr, tpr, _ = roc_curve(self.y_test, y_pred_proba)
        auc = roc_auc_score(self.y_test, y_pred_proba)
        
        fig, ax = plt.subplots()
        plt.plot(fpr, tpr, label=f"AUC = {auc:.4f}")
        plt.plot([0, 1], [0, 1], 'k--', label='Random')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend(loc=4)
        return fig, auc

    def get_auc_score(self):
        """Return AUC score."""
        if self.y_pred is None:
            self.predict()
        y_pred_proba = self.model.predict_proba(self.X_test)[:, 1]
        return roc_auc_score(self.y_test, y_pred_proba)