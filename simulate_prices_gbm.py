import numpy as np
import pandas as pd

def simulate_gbm(df: pd.DataFrame, T: int, dt: float):
    """
    Simulate multivariate geometric Brownian Motion.

    Parameters:
        de : pd.DataFrame
            Data Frame with historical prices of assets
        T : float
            Total time in days
        dt : float
            Time step in years
    """
    num_steps = int(T / dt)
    num_assets = np.shape(df)[1]
    num_days = np.shape(df)[0]

    log_returns = np.log(df / df.shift(1)) # Returns
    sigma = log_returns.std() * np.sqrt(365/num_days)  # Volatility coefficients
    mu = log_returns.mean() + (sigma*sigma)/2  # Drift coefficients

    # Calculate the covariance matrix of returns and adjust the diagonal to be positive definite
    cov_matrix = log_returns.cov() 
    cov_matrix = np.nan_to_num(cov_matrix, nan=0.001)
    cov_matrix = cov_matrix + 0.01 * np.eye(np.shape(cov_matrix)[0])

    # Preparing the Cholesky decomposition for simulating correlated variables
    L = np.linalg.cholesky(cov_matrix)

    # Simulating the random components
    Z = np.random.normal(size=(num_assets, num_steps))

    prices = np.zeros((num_assets, num_steps))
    prices[:, 0] = df.iloc[-1].values # Initialize with last prices reported

    for i in range(1, num_steps):
        prices[:, i] = prices[:, i-1] * np.exp((mu - 0.5 * sigma**2) * dt + np.dot(L, Z[:, i]) * np.sqrt(dt))
    
    return prices