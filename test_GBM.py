import pandas as pd
from extract_drift_and_volatility import extract_drift_and_volatility
from simulate_prices_gbm import simulate_gbm
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('historical_prices.csv')
df = df.drop(columns=['BTC', 'BNB', 'ETH', 'FLOKI', 'SOL', 'DAI'])
df = df.drop(columns=df.columns[df.columns.str.contains('ETH|USD')])
assets_params = extract_drift_and_volatility(df)
prices_gbm = simulate_gbm(assets_params)


# Plot each asset price series
plt.figure(figsize=(12, 8))
for column in prices_gbm.columns:
    plt.plot(df.index, df[column], label=column)

# Position the legend outside the plot area
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xlabel('Time Step')

plt.ylabel('Price')
plt.title('Asset Prices Over Time')
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()


