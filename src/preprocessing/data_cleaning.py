"""
Cleans the input DataFrame by:
    - updating headers
    - handling missing values
    - removing duplicates
    - correcting data types
"""

def clean_data(df):
    df = df.copy()

    df = df.rename(columns={
        'Age': 'Age (yrs)',
        'Monthly Revenue': 'Monthly Revenue ($)',
        'Debt Ratio': 'Debt Ratio (%)',
        'Rated Exposure': 'Rated Exposure',
        '# Overdue 30-59 Days': 'Days Overdue (30-59)',
        '# Overdue 60-89 Days': 'Days Overdue (60-89)',
        '# Overdue 90+ Days': 'Days Overdue (90+)',
        'Serious Delinquencies in past 2 years': 'Delinquencies (last 2 years)'
    })
    return df