import pandas as pd
from utils.get_weights import get_weights


risk_free_rate = 0.05
market_return = 0.5

# Obtain historical prices
df = pd.read_csv('data/historical_prices.csv')

# Get weights
weights = get_weights(risk_free_rate, market_return, df)

# Export to a csv file
weights.to_csv('weights_output.csv', index=False)