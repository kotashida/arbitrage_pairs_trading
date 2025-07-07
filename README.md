# Arbitrage Pairs Trading Project

This project implements a framework for identifying, backtesting, and analyzing arbitrage pairs trading strategies. It leverages historical financial data to find statistically cointegrated asset pairs and simulates trading strategies based on their price relationships.

## Features

-   **Data Acquisition (`src/data_acquisition.py`):** Tools for downloading and processing historical stock data from financial sources (e.g., Yahoo Finance via `yfinance`).
-   **Pair Identification (`src/pair_identification.py`):** Algorithms to identify suitable pairs for trading, often based on statistical properties like cointegration.
-   **Strategy Development (`src/strategy_development.py`):** Implementation of various pairs trading strategies (e.g., mean-reversion based).
-   **Backtesting Engine (`src/backtesting_engine.py`):** A robust engine to simulate trading strategies on historical data, calculating trades, positions, and portfolio value over time.
-   **Performance Analysis (`src/performance_analysis.py`):** Modules for evaluating the profitability and risk of backtested strategies, including metrics like Sharpe Ratio, drawdown, etc.
-   **Utilities (`src/utils.py`):** Helper functions and common tools used across the project.

## Technologies Used

The project is built using Python and relies on the following key libraries:

-   `yfinance`: For fetching financial data.
-   `pandas`: For data manipulation and analysis.
-   `numpy`: For numerical operations.
-   `statsmodels`: For statistical modeling, especially for cointegration tests.
-   `lxml`: Likely used for parsing XML/HTML, potentially in data acquisition.
-   `scipy`: For scientific computing, including statistical functions.
-   `beautifulsoup4`: For web scraping, potentially in data acquisition.

## Installation

To set up the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/arbitrage_pairs_trading.git
    cd arbitrage_pairs_trading
    ```
    *(Note: Replace `https://github.com/your-username/arbitrage_pairs_trading.git` with the actual repository URL if different.)*

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    -   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The main entry point for the project is `main.py`. You can run it to execute the full workflow of data acquisition, pair identification, backtesting, and analysis.

```bash
python main.py
```

Individual modules within the `src/` directory can also be used independently for specific tasks.

## Data

The `data/` directory is intended to store historical financial data. Currently, it contains:

-   `portfolio_value.csv`: Likely stores the simulated portfolio value over time from backtesting.
-   `sp500_adj_close.csv`: Contains historical adjusted close prices for S&P 500 constituents, used for pair identification and backtesting.

## Project Structure

```
arbitrage_pairs_trading/
├── main.py                 # Main script to run the entire workflow
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── .git/                   # Git version control files
├── data/                   # Stores historical and generated data
│   ├── portfolio_value.csv
│   └── sp500_adj_close.csv
└── src/                    # Source code for different modules
    ├── backtesting_engine.py
    ├── data_acquisition.py
    ├── pair_identification.py
    ├── performance_analysis.py
    ├── strategy_development.py
    └── utils.py
```
