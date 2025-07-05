import yfinance as yf
import pandas as pd
import time
import os

def get_sp500_tickers():
    """Fetches S&P 500 tickers from Wikipedia."""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url, header=0)
    sp500_table = tables[0]
    tickers = sp500_table['Symbol'].tolist()
    # yfinance uses dashes for some tickers, so replace dots
    tickers = [ticker.replace('.', '-') for ticker in tickers]
    return tickers

def download_historical_data(tickers, start_date, end_date):
    """Downloads historical daily price data for a list of tickers."""
    all_data = []
    failed_tickers = []
    
    print("Starting data download...")
    for i, ticker in enumerate(tickers):
        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
            
            if data.empty:
                raise ValueError("No data downloaded for ticker")

            # 'Close' is the adjusted close price with auto_adjust=True
            data.rename(columns={'Close': ticker}, inplace=True)
            all_data.append(data[[ticker]])
            print(f"({i+1}/{len(tickers)}) Successfully downloaded {ticker}")
            
            time.sleep(0.5) # Pause to avoid overwhelming the API

        except Exception as e:
            failed_tickers.append(ticker)

    if not all_data:
        return pd.DataFrame(), failed_tickers

    full_df = pd.concat(all_data, axis=1)
    return full_df, failed_tickers


if __name__ == "__main__":
    tickers = get_sp500_tickers()
    start_date = "2010-01-01"
    end_date = "2024-06-30"
    print(f"Found {len(tickers)} tickers. Downloading historical data from {start_date} to {end_date}...")
    
    adj_close_data, failed_list = download_historical_data(tickers, start_date, end_date)
    
    if not adj_close_data.empty:
        print(f"\nSuccessfully downloaded data for {len(adj_close_data.columns)} tickers.")
        if failed_list:
            print(f"Failed to download data for {len(failed_list)} tickers: {failed_list}")

        # Save data for later use
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        os.makedirs(data_dir, exist_ok=True)
        output_path = os.path.join(data_dir, "sp500_adj_close.csv")
        adj_close_data.to_csv(output_path)
        print(f"Historical data saved to {output_path}")
    else:
        print("\nFailed to download any historical data.")
