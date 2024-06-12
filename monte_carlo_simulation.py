import pandas as pd

from utils.simulate_prices_gbm import simulate_gbm
from utils.get_weights import get_weights

# Obtain historical prices
df = pd.read_csv('data/historical_prices.csv')

def simulation_montecarlo(df):
    # weights
    risk_free_rate = 0.05
    market_return = 0.5
    T = 1
    dt = 1/365

    data_list_min_w = [] # Min Variance Weights
    data_list_max_w = [] # Max Sharpe Weights

    number_of_simulations = 0

    for _ in range (20):
        number_of_simulations += 1
        prices_gbm = simulate_gbm(df, T, dt)
        weights = get_weights(risk_free_rate, market_return, prices_gbm)
        data_list_min_w.append(list(weights['Min Weight']))
        data_list_max_w.append(list(weights['Max Weight']))

    weights_names = get_weights(risk_free_rate, market_return, df)['Names']

    # Create DataFrames
    return pd.DataFrame(data_list_min_w, columns=weights_names), pd.DataFrame(data_list_max_w, columns=weights_names)

df_min_w, df_max_w  = simulation_montecarlo(df)

# Save the DataFrame to a CSV file
df_min_w.to_csv( 'data/output_simulation_min_weights.csv', index=False)
df_max_w.to_csv( 'data/output_simulation_max_weights.csv', index=False)
