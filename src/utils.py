import pandas as pd
import os

def load_data(file_path):
    """Loads historical adjusted close price data from a CSV file."""
    data = pd.read_csv(file_path, index_col=0, parse_dates=True, low_memory=False, skiprows=2, header=0)
    # Ensure all columns are numeric, coercing errors to NaN
    for col in data.columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    # Drop columns that are entirely NaN (e.g., tickers with no data)
    data.dropna(axis=1, how='all', inplace=True)
    return data

def get_data_dir():
    """Returns the absolute path to the data directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
