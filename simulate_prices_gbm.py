import numpy as np
import pandas as pd

def simulate_gbm(assets, initial_price=100, time_horizon=100, n_steps=100, seed=None):
    """
    Simulate asset prices using Geometric Brownian Motion.

    Parameters:
    - assets: List of tuples [(asset_name, drift, volatility), ...]
    - initial_price: Starting price for all assets
    - time_horizon: Total time for the simulation in years
    - n_steps: Number of time steps in the simulation
    - seed: Random seed for reproducibility

    Returns:
    - DataFrame containing simulated asset prices over time
    """
    if seed is not None:
        np.random.seed(seed)
        
    dt = time_horizon / n_steps
    n_assets = len(assets)
    
    # Initialize the price matrix
    prices = np.zeros((n_steps + 1, n_assets))
    prices[0, :] = initial_price
    
    # Create time index
    time_index = np.linspace(0, time_horizon, n_steps + 1)
    
    # Simulate asset prices
    for i, (name, drift, volatility) in enumerate(assets):
        drift = drift / 100
        volatility = volatility / 100
        for t in range(1, n_steps + 1):
            z = np.random.standard_normal()
            prices[t, i] = prices[t-1, i] * np.exp((drift - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * z)
    
    # Convert to DataFrame
    price_df = pd.DataFrame(prices, columns=[name for name, _, _ in assets], index=time_index)
    
    return price_df