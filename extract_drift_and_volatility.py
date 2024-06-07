import pandas as pd
import numpy as np

def extract_drift_and_volatility(df: pd.DataFrame):
    """
    Extract drift and volatility from a CSV file of asset prices.

    Parameters:
    - file_path: Path to the CSV file

    Returns:
    - List of tuples [(asset_name, drift_percentage, volatility_percentage), ...]
    """
    
    # Initialize a list to store the results
    results = []
    j = 0
    drift_vector = np.zeros(np.shape(df)[0])
    # Iterate over each column (asset) in the DataFrame
    for asset_name in df.columns:
        # Calculate log returns
        prices = df[asset_name]
        log_returns = np.log(prices / prices.shift(1)).dropna()
        
        # Calculate drift (mean of log returns) and volatility (standard deviation of log returns)
        drift = log_returns.mean()
        drift_vector[j] = drift
        j += 1
        volatility = log_returns.std() #* np.sqrt(522)  # annualize the volatility
        
        # Convert drift and volatility to percentages
        drift_percentage = drift * 100
        volatility_percentage = volatility * 100
        
        # Append the results to the list
        results.append((asset_name, drift_percentage, volatility_percentage))
    
    return results