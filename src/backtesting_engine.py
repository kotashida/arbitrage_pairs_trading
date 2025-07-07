import pandas as pd
import numpy as np
import statsmodels.api as sm
import os

from utils import load_data, get_data_dir

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

class Backtester:
    def __init__(self, initial_capital=100000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.portfolio_value = pd.Series(dtype=float)
        self.positions = {'asset1': 0, 'asset2': 0}
        self.in_trade = False

    def run_backtest(self, stock_data, signals, asset1_ticker, asset2_ticker):
        self.portfolio_value = pd.Series(index=stock_data.index, dtype=float)
        
        for i, date in enumerate(stock_data.index):
            if i == 0: # Initialize portfolio value
                self.portfolio_value.loc[date] = self.capital
                continue

            price1 = stock_data.loc[date, asset1_ticker]
            price2 = stock_data.loc[date, asset2_ticker]

            if pd.isna(price1) or pd.isna(price2):
                self.portfolio_value.loc[date] = self.portfolio_value.iloc[i-1]
                continue

            # Update portfolio value
            if self.in_trade:
                current_value = self.capital + \
                                self.positions['asset1'] * price1 + \
                                self.positions['asset2'] * price2
                self.portfolio_value.loc[date] = current_value
            else:
                self.portfolio_value.loc[date] = self.capital

            # Get signals for the current date
            long_entry = signals.loc[date, 'long_entry']
            short_entry = signals.loc[date, 'short_entry']
            long_exit = signals.loc[date, 'long_exit']
            short_exit = signals.loc[date, 'short_exit']

            # Execute trades based on signals
            if not self.in_trade:
                if long_entry: # Buy spread
                    amount_to_invest = self.capital / 2
                    shares1 = amount_to_invest / price1
                    shares2 = amount_to_invest / price2

                    self.positions['asset1'] = shares1
                    self.positions['asset2'] = -shares2 # Short asset2
                    self.in_trade = True

                elif short_entry: # Sell spread
                    amount_to_invest = self.capital / 2
                    shares1 = amount_to_invest / price1
                    shares2 = amount_to_invest / price2

                    self.positions['asset1'] = -shares1 # Short asset1
                    self.positions['asset2'] = shares2
                    self.in_trade = True

            elif self.in_trade:
                # Check for exit conditions
                if (self.positions['asset1'] > 0 and long_exit) or \
                   (self.positions['asset1'] < 0 and short_exit):
                    
                    # Close positions
                    self.capital += self.positions['asset1'] * price1 + \
                                    self.positions['asset2'] * price2
                    
                    self.positions = {'asset1': 0, 'asset2': 0}
                    self.in_trade = False

        return self.portfolio_value

if __name__ == "__main__":
    data_dir = get_data_dir()
    data_file_path = os.path.join(data_dir, "sp500_adj_close.csv")
    
    stock_data = load_data(data_file_path)
    
    # Demonstrate with a sample pair
    asset1_ticker = "AMZN"
    asset2_ticker = "NVDA"

    if asset1_ticker not in stock_data.columns or asset2_ticker not in stock_data.columns:
        print(f"Error: {asset1_ticker} or {asset2_ticker} not found in data.")
    else:
        series1 = stock_data[asset1_ticker].dropna()
        series2 = stock_data[asset2_ticker].dropna()

        # Align series to a common index
        common_index = series1.index.intersection(series2.index)
        series1 = series1.loc[common_index]
        series2 = series2.loc[common_index]

        if len(series1) < 60: # Ensure enough data for rolling window
            print(f"Skipping pair {asset1_ticker}-{asset2_ticker}: Not enough data points for strategy.")
        else:
            beta, spread = calculate_hedge_ratio_and_spread(series1, series2)
            signals = generate_signals(spread)

            backtester = Backtester(initial_capital=100000)
            portfolio_value = backtester.run_backtest(stock_data, signals, asset1_ticker, asset2_ticker)

            print("\nBacktest complete. Portfolio Value (first 5 rows):")
            print(portfolio_value.head())
            print("\nPortfolio Value (last 5 rows):")
            print(portfolio_value.tail())
            print(f"\nFinal Portfolio Value: {portfolio_value.iloc[-1]:.2f}")
            print(f"Initial Capital: {backtester.initial_capital:.2f}")
            print(f"Total Return: {((portfolio_value.iloc[-1] - backtester.initial_capital) / backtester.initial_capital * 100):.2f}%")

            # Save portfolio value for analysis
            portfolio_value_path = os.path.join(data_dir, "portfolio_value.csv")
            portfolio_value.to_csv(portfolio_value_path, header=['Portfolio_Value'])
            print(f"Portfolio value saved to {portfolio_value_path}")
