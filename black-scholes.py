import requests
from scipy.stats import norm
from math import log, sqrt, exp

# Function to fetch real-time stock price from Alpha Vantage API
def get_stock_price(symbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return float(data['Global Quote']['05. price'])
    else:
        print(f"Failed to fetch stock price for {symbol}.")
        return None

# Function to calculate the Black-Scholes call option price
def black_scholes_call(S, K, r, sigma, T):
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)

# Function to calculate the Black-Scholes put option price
def black_scholes_put(S, K, r, sigma, T):
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# Example usage
if __name__ == "__main__":
    symbol = "AAPL"     # Stock symbol
    K = 200             # Strike price
    r = 0.05            # Risk-free interest rate
    sigma = 0.2         # Volatility
    T = 1               # Time to expiration (in years)


    S = get_stock_price(symbol)
   
