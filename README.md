# Statistical Arbitrage Pairs Trading Backtester

This project implements a complete backtesting pipeline for a statistical arbitrage pairs trading strategy. It leverages cointegration analysis to identify pairs of stocks with a stable, long-run relationship and then backtests a mean-reversion strategy on the identified pairs.

## Methodology

The project is broken down into five key modules, each handling a specific part of the workflow:

1.  **Data Acquisition (`data_acquisition.py`)**: This module is responsible for sourcing the historical price data. It fetches the list of S&P 500 tickers from Wikipedia and then downloads daily adjusted close prices for each ticker from Yahoo Finance. The data is saved to a CSV file for use in the other modules.

2.  **Pair Identification (`pair_identification.py`)**: This module screens for cointegrated pairs of stocks from the downloaded data. It uses the Engle-Granger two-step cointegration test to identify pairs that have a statistically significant long-run equilibrium. These pairs are the candidates for our mean-reversion strategy.

3.  **Strategy Development (`strategy_development.py`)**: For each cointegrated pair, this module defines the trading logic. It calculates the hedge ratio (beta) and the spread between the two assets. Trading signals are then generated based on the z-score of the spread, which indicates when the spread has deviated significantly from its historical mean.

4.  **Backtesting Engine (`backtesting_engine.py`)**: This module simulates the trading strategy using the historical data and the generated signals. It processes the data day-by-day, executes trades, and tracks the value of a hypothetical portfolio, accounting for transaction costs.

5.  **Performance Analysis (`performance_analysis.py`)**: Finally, this module evaluates the performance of the backtested strategy. It calculates key metrics such as the Sharpe ratio, Sortino ratio, maximum drawdown, and annualized volatility to assess the strategy's profitability and risk.

## Backtest Results

The backtesting engine was run on the first cointegrated pair found in the S&P 500 dataset: **MMM (3M Company)** and **HAS (Hasbro, Inc.)**. The results of the backtest are as follows:

*   **Total Return**: 43.42%
*   **Sharpe Ratio**: 0.2783
*   **Sortino Ratio**: 0.3147
*   **Maximum Drawdown**: -25.48%
*   **Annualized Volatility**: 11.73%

These results indicate that the strategy was profitable over the backtesting period, but also experienced a significant drawdown. Further optimization and risk management would be required for a real-world implementation.

## How to Run the Project

To run the project, follow these steps:

1.  **Install Dependencies**: Ensure you have Python installed, then install the required libraries using pip:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Main Script**: Execute the `main.py` script from the `src` directory:

    ```bash
    python src/main.py
    ```

This will run the entire pipeline, from data acquisition to performance analysis, and print the results to the console.