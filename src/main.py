import pandas as pd
import os

from data_acquisition import download_historical_data, get_sp500_tickers
from pair_identification import find_cointegrated_pairs, load_data
from strategy_development import calculate_hedge_ratio_and_spread, generate_signals
from backtesting_engine import Backtester
from performance_analysis import calculate_returns, calculate_sharpe_ratio, calculate_sortino_ratio, calculate_max_drawdown, calculate_volatility

def main():
    # 1. Data Acquisition
    data_file_path = r"C:\Users\shida\OneDrive\Programming\arbitrage_pairs_trading\data\sp500_adj_close.csv"
    
    if not os.path.exists(data_file_path):
        print("Historical data not found. Downloading data...")
        tickers = get_sp500_tickers()
        start_date = "2010-01-01"
        end_date = "2025-06-30"
        print(f"Found {len(tickers)} tickers. Downloading historical data from {start_date} to {end_date}...")
        
        adj_close_data, failed_list = download_historical_data(tickers, start_date, end_date)
        
        if not adj_close_data.empty:
            print(f"\nSuccessfully downloaded data for {len(adj_close_data.columns)} tickers.")
            if failed_list:
                print(f"Failed to download data for {len(failed_list)} tickers: {failed_list}")

            adj_close_data.to_csv(data_file_path)
            print(f"Historical data saved to {data_file_path}")
        else:
            print("\nFailed to download any historical data. Exiting.")
            return
    else:
        print(f"Found existing data file at {data_file_path}. Loading data...")

    stock_data = load_data(data_file_path)
    print("Data loaded successfully.")

    # 2. Pair Identification
    print("\nFinding cointegrated pairs...")
    cointegrated_pairs = find_cointegrated_pairs(stock_data)

    if not cointegrated_pairs:
        print("No cointegrated pairs found. Using a default pair for demonstration (AMZN, NVDA).")
        cointegrated_pairs = [("AMZN", "NVDA")] 
    else:
        print("\nFound cointegrated pairs (Asset1, Asset2, P-value):")
        for pair in cointegrated_pairs:
            print(f"  {pair[0]} - {pair[1]} (p-value: {pair[2]:.4f})")
        # Use the first found pair for backtesting
        cointegrated_pairs = [cointegrated_pairs[0][:2]]

    for asset1_ticker, asset2_ticker in cointegrated_pairs:
        print(f"\n--- Processing pair: {asset1_ticker} and {asset2_ticker} ---")

        series1 = stock_data[asset1_ticker].dropna()
        series2 = stock_data[asset2_ticker].dropna()

        common_index = series1.index.intersection(series2.index)
        series1 = series1.loc[common_index]
        series2 = series2.loc[common_index]

        if len(series1) < 60:
            print(f"Skipping pair {asset1_ticker}-{asset2_ticker}: Not enough data points for strategy.")
            continue

        # 3. Strategy Development
        print("\nCalculating hedge ratio and generating signals...")
        beta, spread = calculate_hedge_ratio_and_spread(series1, series2)
        signals = generate_signals(spread)
        print(f"Hedge ratio (beta) for {asset1_ticker} vs {asset2_ticker}: {beta:.4f}")

        # 4. Backtesting
        print("\nRunning backtest...")
        backtester = Backtester(initial_capital=100000)
        portfolio_value = backtester.run_backtest(stock_data, signals, asset1_ticker, asset2_ticker)
        
        portfolio_value_path = r"C:\Users\shida\OneDrive\Programming\arbitrage_pairs_trading\data\portfolio_value.csv"
        portfolio_value.to_csv(portfolio_value_path)
        print(f"Portfolio value saved to {portfolio_value_path}")

        print(f"\nFinal Portfolio Value: {portfolio_value.iloc[-1]:.2f}")
        print(f"Initial Capital: {backtester.initial_capital:.2f}")
        print(f"Total Return: {((portfolio_value.iloc[-1] - backtester.initial_capital) / backtester.initial_capital * 100):.2f}%")

        # 5. Performance Analysis
        print("\nCalculating performance metrics...")
        returns = calculate_returns(portfolio_value)
        sharpe_ratio = calculate_sharpe_ratio(returns)
        sortino_ratio = calculate_sortino_ratio(returns)
        max_drawdown = calculate_max_drawdown(portfolio_value)
        volatility = calculate_volatility(returns)

        print(f"Sharpe Ratio: {sharpe_ratio:.4f}")
        print(f"Sortino Ratio: {sortino_ratio:.4f}")
        print(f"Max Drawdown: {max_drawdown:.4f}")
        print(f"Volatility (Annualized): {volatility:.4f}")

if __name__ == "__main__":
    main()
