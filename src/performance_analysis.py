import pandas as pd
import numpy as np
import os

from utils import get_data_dir

def calculate_returns(portfolio_value):
    """Calculates daily returns from a portfolio value series."""
    returns = portfolio_value.pct_change().dropna()
    return returns

def calculate_sharpe_ratio(returns, risk_free_rate=0.0):
    """Calculates the annualized Sharpe Ratio."""
    excess_returns = returns - risk_free_rate / 252
    sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
    return sharpe_ratio

def calculate_sortino_ratio(returns, risk_free_rate=0.0):
    """Calculates the annualized Sortino Ratio."""
    excess_returns = returns - risk_free_rate / 252
    downside_returns = excess_returns[excess_returns < 0]
    downside_deviation = np.std(downside_returns)
    
    if downside_deviation == 0:
        return np.nan
        
    sortino_ratio = np.mean(excess_returns) / downside_deviation * np.sqrt(252)
    return sortino_ratio

def calculate_max_drawdown(portfolio_value):
    """Calculates the maximum drawdown."""
    peak = portfolio_value.expanding(min_periods=1).max()
    drawdown = (portfolio_value - peak) / peak
    max_drawdown = drawdown.min()
    return max_drawdown

def calculate_volatility(returns):
    """Calculates the annualized volatility."""
    volatility = np.std(returns) * np.sqrt(252)
    return volatility

if __name__ == "__main__":
    # Load portfolio value data for demonstration
    data_dir = get_data_dir()
    portfolio_value_file = os.path.join(data_dir, "portfolio_value.csv")
    portfolio_value = pd.read_csv(portfolio_value_file, index_col=0, parse_dates=True).squeeze()

    print("Calculating performance metrics...")
    
    returns = calculate_returns(portfolio_value)
    sharpe_ratio = calculate_sharpe_ratio(returns)
    sortino_ratio = calculate_sortino_ratio(returns)
    max_drawdown = calculate_max_drawdown(portfolio_value)
    volatility = calculate_volatility(returns)
    
    print(f"Total Return: {((portfolio_value.iloc[-1] - portfolio_value.iloc[0]) / portfolio_value.iloc[0] * 100):.2f}%")
    print(f"Sharpe Ratio: {sharpe_ratio:.4f}")
    if not np.isnan(sortino_ratio):
        print(f"Sortino Ratio: {sortino_ratio:.4f}")
    else:
        print("Sortino Ratio: N/A (no downside deviation)")
    print(f"Max Drawdown: {max_drawdown:.4f}")
    print(f"Volatility (Annualized): {volatility:.4f}")
