import pandas as pd
import os

def load_data(file_path):
    """Loads historical adjusted close price data from a CSV file."""
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)
    return data

def get_data_dir():
    """Returns the absolute path to the data directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
