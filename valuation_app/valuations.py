import pandas as pd
from datetime import datetime


def load_far(file_path: str) -> pd.DataFrame:
    """Load fixed asset register from CSV or Excel file."""
    if file_path.lower().endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    return df


def compute_asset_age(df: pd.DataFrame, valuation_date: str) -> pd.DataFrame:
    """Add an 'Asset Age (years)' column based on valuation date and acquisition date."""
    valuation_dt = pd.to_datetime(valuation_date)
    df['Asset acquisition date'] = pd.to_datetime(df['Asset acquisition date'])
    df['Asset Age (years)'] = (valuation_dt - df['Asset acquisition date']).dt.days / 365.0
    return df
