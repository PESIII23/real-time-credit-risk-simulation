
"""Data transformations for credit risk analysis."""
import pandas as pd


def backfill_overdues(df: pd.DataFrame, col_1: str, col_2: str, col_3: str) -> pd.DataFrame:
    """Enforce monotonic delinquency severity (90+ -> 60-89 -> 30-59)."""
    df = df.copy()
    mask_second = df[col_2] < df[col_3]
    df.loc[mask_second, col_2] = df.loc[mask_second, col_3]
    mask_first = df[col_1] < df[col_2]
    df.loc[mask_first, col_1] = df.loc[mask_first, col_2]
    return df


def is_missing_value(df: pd.DataFrame, col_orig: str, col_bool: str) -> pd.DataFrame:
    """Create binary indicator for missing values."""
    df[col_bool] = df[col_orig].isna().astype(int)
    return df


def apply_all_transformations(df: pd.DataFrame) -> pd.DataFrame:
    print(f"      Applying transformations.")
    """Apply all transformations in sequence."""
    df = backfill_overdues(df, 'overdue_30_59_days', 'overdue_60_89_days', 'overdue_90_plus_days')
    df = is_missing_value(df, 'monthly_revenue', 'revenue_missing')
    df = is_missing_value(df, 'debt_ratio', 'debt_ratio_missing')
    df = is_missing_value(df, 'rated_exposure', 'rated_exposure_missing')
    return df