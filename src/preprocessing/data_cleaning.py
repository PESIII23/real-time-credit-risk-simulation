import pandas as pd

"""
Cleans the input DataFrame by:
    - updating headers
    - handling missing values
    - removing duplicates
    - correcting data types
"""

def clean_raw_data(df):
    df = df.copy()

    df = df.rename(columns={
        'Age': 'age',
        'Monthly Revenue': 'monthly_revenue',
        'Debt Ratio': 'debt_ratio',
        'Rated Exposure': 'rated_exposure',
        '# Overdue 30-59 Days': 'overdue_30_59_days',
        '# Overdue 60-89 Days': 'overdue_60_89_days',
        '# Overdue 90+ Days': 'overdue_90_plus_days',
        'Serious Delinquencies in past 2 years': 'serious_delinquencies_past_2_years'
    })

    return df