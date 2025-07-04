import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint

def load_data(file_path):
    """Loads historical adjusted close price data from a CSV file."""
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)
    return data

def find_cointegrated_pairs(data, significance_level=0.05):
    """Finds cointegrated pairs of stocks using the Engle-Granger test."""
    n_assets = data.shape[1]
    keys = data.columns
    pairs = []
    
    # Iterate through all unique pairs of assets
    for i in range(n_assets):
        for j in range(i + 1, n_assets):
            asset1 = keys[i]
            asset2 = keys[j]
            
            series1 = data[asset1].dropna()
            series2 = data[asset2].dropna()
            
            # Ensure both series have the same length
            common_index = series1.index.intersection(series2.index)
            if len(common_index) == 0:
                continue
            
            series1 = series1.loc[common_index]
            series2 = series2.loc[common_index]
            
            if len(series1) < 20: # Require a minimum number of data points
                continue

            # Perform the cointegration test
            score, p_value, _ = coint(series1, series2)
            
            if p_value < significance_level:
                pairs.append((asset1, asset2, p_value))
                
    return pairs

if __name__ == "__main__":
    file_path = r"C:\Users\shida\OneDrive\Programming\arbitrage_pairs_trading\data\sp500_adj_close.csv"
    
    print(f"Loading data from {file_path}...")
    stock_data = load_data(file_path)
    
    print("\nFinding cointegrated pairs...")
    cointegrated_pairs = find_cointegrated_pairs(stock_data)
    
    if cointegrated_pairs:
        print("\nFound cointegrated pairs (Asset1, Asset2, P-value):")
        for pair in cointegrated_pairs:
            print(f"  {pair[0]} - {pair[1]} (p-value: {pair[2]:.4f})")
    else:
        print("\nNo cointegrated pairs found at the specified significance level.")
