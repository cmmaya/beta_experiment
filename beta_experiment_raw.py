import yfinance as yf
import pandas as pd
import datetime
import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

# Fetch Historical Data
start = datetime.datetime(2022, 1, 1)
end = datetime.datetime.now()

assets_list = ["SHIB", "RNDR", "MNT", "ARB", "ONDO", "BEAM", "JASMY", "W", "WLD", "SAND", "AEVO", "AXL", "ARKM", 
               "MANTA", "ANT", "LRC", "SFP", "TRAC", "CFG", "MASK", "HIGH", "CHR", "ICX", "LDO"]

eth = yf.download('ETH-USD', start=start, end=end)  # Ethereum data
eth_returns = eth['Adj Close'].pct_change()

# Create DataFrame for returns
returns = pd.DataFrame({
    'ETH': eth_returns,
})
for asset_name in assets_list:
    asset = yf.download(f"{asset_name}-USD", start=start, end=end)  # Example asset

    # Calculate 
    # Returns and Covariance
    asset_returns = asset['Adj Close'].pct_change()
    # Continue for other assets
    returns[f"{asset_name}"] = asset_returns


# Calculate Covariance Matrix
covariance_matrix = returns.cov()

# Calculate Beta Values
market_var = returns['ETH'].var()
betas = {}
for asset in returns.columns[1:]:  # Exclude 'ETH'
    cov_with_market = returns['ETH'].cov(returns[asset])
    betas[asset] = cov_with_market / market_var

# Define Optimization Problem
n = len(returns.columns) - 1  # number of assets excluding ETH
w = cp.Variable(n)
expected_returns = returns.mean()[1:]  # Exclude ETH
covariance_matrix = covariance_matrix.fillna(0)

# Define the minimization objective
objective = cp.Minimize(cp.quad_form(w, covariance_matrix.iloc[1:, 1:]))

# Define the maximization objective
#numerator = w.T @ expected_returns
#denominator = cp.inv_pos(cp.sqrt(cp.quad_form(w, covariance_matrix.iloc[1:, 1:])))
#objective = cp.Maximize(numerator * denominator)


constraints = [cp.sum(w) == 1, w >= 0]  # Adjust constraints as necessary

# Solve Optimization Problem
problem = cp.Problem(objective, constraints)
problem.solve()

# Initialize an empty dictionary
result_dict = {}

# Iterate over the lists and populate the dictionary
for name, value in zip(assets_list, w.value):
    rounded_value = round(value, 3)
    result_dict[name] = rounded_value

print("Optimal Portfolio Weights:", result_dict)

# Analyze Results
# Plotting and further analysis can be done using matplotlib or other libraries as needed
# Calculate the relative prices to ETH
relative_prices = returns.div(returns['ETH'], axis=0)

# Plot the relative prices
plt.figure(figsize=(14, 8))

for asset in relative_prices.columns[1:]:  # Exclude 'ETH' from the plot
    plt.plot(relative_prices.index, relative_prices[asset], label=asset)


plt.title('Price of Assets Relative to ETH')
plt.xlabel('Date')
plt.ylabel('Relative Price')
plt.ylim(0, relative_prices.max().max())
plt.xlim([datetime.datetime(2022, 5, 1), datetime.datetime(2023, 1, 1)])
plt.legend()
plt.show()