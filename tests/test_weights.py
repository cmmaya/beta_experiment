import pandas as pd
import sys
import os

# Get the parent directory of the current directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, parent_dir)

from utils.get_weights import get_weights


risk_free_rate = 0.05
market_return = 0.5

# Obtain historical prices
df = pd.read_csv('data/historical_prices.csv')

# Get weights
weights = get_weights(risk_free_rate, market_return, df)

print(weights)
# Export to a csv file
weights.to_csv('data/weights_output.csv', index=False)