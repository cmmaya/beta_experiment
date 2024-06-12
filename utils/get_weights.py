
import pandas as pd
import pandas as pd
import pandas as pd
import numpy as np
from scipy.optimize import minimize

def get_weights(risk_free_rate: int, market_return: int, df: pd.DataFrame):

    # Obtain ETH columns
    eth = df['ETH']

    # Drop ETH column and not useful columns
    df = df.drop(columns=['DAI', 'FLOKI'])
    df = df.drop(columns=df.columns[df.columns.str.contains('ETH|USD')])
    returns = df.pct_change()

    # Compute daily return of Ethereum to use as the market return
    eth_returns = eth.pct_change()

    # Prepare to store beta values
    betas = {}
    means=[]
    returns = returns.replace([np.nan, np.inf, -np.inf], 0)
    eth_returns = eth_returns.replace([np.nan, np.inf, -np.inf], 0)

    # Compute beta for each column (cryptocurrency) against ETH
    for column in returns.columns:
        if column != 'eth':  # Skip calculating ETH's beta with itself
            covariance = returns[column].cov(eth_returns)
            variance = eth_returns.var()
            means.append(max(0,returns[column].mean()))

            beta = covariance / variance
            betas[column] = beta

    # CAPM Expected Returns

    # Simulated covariance matrix based on betas (scaled for demonstration)
    # Normally, you'd calculate this based on historical returns data
    cov_matrix = returns.cov()  # Simplified assumption
    expected_returns=means

    # Number of assets
    num_assets = len(betas)

    # Objective Functions
    def portfolio_variance(weights):
        return weights.T @ cov_matrix @ weights

    def portfolio_return(weights):
        return weights.T @ expected_returns

    target_beta = 1.0

    # Calculate portfolio beta as a function of weights
    def portfolio_beta(weights):
        individual_betas = np.array(list(betas.values()))
        return np.dot(weights, individual_betas)

    # Constraint to achieve the target beta
    constraints = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Weights must sum to 1
        {'type': 'eq', 'fun': lambda x: (portfolio_beta(x) - target_beta)**2}  # Portfolio beta must meet target
    ]
    bounds = tuple((0, 1) for asset in range(num_assets))

    # Initial guess (equal weighting)
    init_guess = np.ones(num_assets) / num_assets

    # Portfolio optimization for minimum variance
    opt_min_var = minimize(portfolio_variance, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    min_var_weights = opt_min_var.x

    # Portfolio optimization for maximum Sharpe Ratio (Risk-Free Rate: 1%)
    constraints = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Weights must sum to 1
        {'type': 'eq', 'fun': lambda x: -(portfolio_beta(x) - target_beta)**2}  # Portfolio beta must meet target
    ]
    def neg_sharpe_ratio(weights):
        return - (portfolio_return(weights) - risk_free_rate) / np.sqrt(portfolio_variance(weights))

    opt_max_sharpe = minimize(neg_sharpe_ratio, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    max_sharpe_weights = opt_max_sharpe.x

    # Round the decimals to 3
    res_max = {}
    res_min = {}
    for i in range(num_assets):
        name=df.columns[i]
        res_max[name]=round(max_sharpe_weights[i],3)
        res_min[name]=round(min_var_weights[i],3)    

    # Assign each weight with their names in a dict
    max_utility_w = {key: value for key, value in res_max.items()}
    min_variance_w = {key: value for key, value in res_min.items()}

    # Extract names, min_weight values, and max_weight values
    names = list(min_variance_w.keys())
    min_weights = list(min_variance_w.values())
    max_weights = list(max_utility_w.values())

    # Create a DataFrame with the data
    data = pd.DataFrame({'Names': names, 'Min Weight': min_weights, 'Max Weight': max_weights})

    # Return the DataFrame
    return data