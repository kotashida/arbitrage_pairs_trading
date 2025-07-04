import pandas as pd
import numpy as np
import statsmodels.api as sm

def load_data(file_path):
    """Loads historical adjusted close price data from a CSV file."""
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)
    return data

def calculate_hedge_ratio_and_spread(series1, series2):
    """Calculates the hedge ratio (beta) and spread using OLS regression."""
    X = sm.add_constant(series2)
    model = sm.OLS(series1, X)
    results = model.fit()
    beta = results.params[1]
    spread = series1 - beta * series2
    return beta, spread

def generate_signals(spread, entry_zscore=2.0, exit_zscore=0.0):
    """Generates trading signals based on the z-score of the spread."""
    # Use a rolling window to calculate z-scores
    window = 60
    rolling_mean = spread.rolling(window=window).mean()
    rolling_std = spread.rolling(window=window).std()
    
    z_score = (spread - rolling_mean) / rolling_std
    
    signals = pd.DataFrame(index=spread.index)
    signals['long_entry'] = z_score < -entry_zscore
    signals['short_entry'] = z_score > entry_zscore
    signals['long_exit'] = z_score >= exit_zscore
    signals['short_exit'] = z_score <= exit_zscore
    
    return signals

if __name__ == "__main__":
    data_file_path = r"C:\Users\shida\OneDrive\Programming\arbitrage_pairs_trading\data\sp500_adj_close.csv"
    
    # Demonstrate with a hardcoded pair
    cointegrated_pairs = [("AMZN", "NVDA")] 
    
    print(f"Loading data from {data_file_path}...")
    stock_data = load_data(data_file_path)
    print("Data loaded successfully.")
    
    for asset1, asset2 in cointegrated_pairs:
        print(f"\nProcessing pair: {asset1} and {asset2}")
        
        series1 = stock_data[asset1].dropna()
        series2 = stock_data[asset2].dropna()
        
        # Align series to a common index
        common_index = series1.index.intersection(series2.index)
        series1 = series1.loc[common_index]
        series2 = series2.loc[common_index]
        
        if len(series1) < 60: # Ensure enough data for rolling window
            print(f"Skipping pair {asset1}-{asset2}: Not enough data points.")
            continue
            
        beta, spread = calculate_hedge_ratio_and_spread(series1, series2)
        print(f"Hedge ratio (beta) for {asset1} vs {asset2}: {beta:.4f}")
        
        signals = generate_signals(spread)
        print("Generated signals (first 5 rows):")
        print(signals.head())

        print("Generated signals (last 5 rows):")
        print(signals.tail())