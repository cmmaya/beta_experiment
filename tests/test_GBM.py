import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Get the parent directory of the current directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, parent_dir)

from utils.simulate_prices_gbm import simulate_gbm

# Read historical prices and discard non useful assets
df = pd.read_csv('data/historical_prices.csv')
df = df.drop(columns=['FLOKI', 'DAI'])
df = df.drop(columns=df.columns[df.columns.str.contains('ETH|USD')])

# Run GBM simulation
T = 1
dt = 1/365
prices_gbm = simulate_gbm(df, T, dt)


# Plot each asset price series
num_assets = np.shape(df)[1]

plt.figure(figsize=(12, 8))

for column in prices_gbm.columns:
    plt.plot(prices_gbm.index, prices_gbm[column], label=column)

# Position the legend outside the plot area
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xlabel('Time Step')
plt.ylabel('Price')
plt.title('Asset Prices Over Time')
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()


