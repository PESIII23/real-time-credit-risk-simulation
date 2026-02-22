
def backfill_overdues(df, col_1: str = None, col_2: str = None, col_3: str = None):
    """Enforce monotonic delinquency severity"""
    mask_second = df[col_2] < df[col_3]
    df.loc[mask_second, col_2] = df.loc[mask_second, col_3] # must backfill higher degree of overdues first

    mask_first = df[col_1] < df[col_2]
    df.loc[mask_first, col_1] = df.loc[mask_first, col_2]
    return df

def is_missing_value(df, col_orig: str = None, col_bool: str = None):
    df[col_bool] = df[col_orig].isna().astype(int)
    return df

def fill_missing_value(df, col: str = None):
    col_mean = df[col].mean()
    df[col] = df[col].fillna(col_mean)
    return df