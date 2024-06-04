# Ethereum beta

In these quick notes we aim at answeting the question:

_What is the most superior vehicle of exposure a long ETH beta ($β$) position (risk-adjusted)?_

In this specific case, "ETH beta" refers to the measure of how much a token $\mathsf{X}$ as an investment is expected to respond to swings in the price of ETH. This can be particularly useful for investors trying to understand the risk-reward profile of holding $\mathsf{X}$ relative to ETH, especially in a risk-adjusted context.

## Mathematical Formulation

Beta is calculated using the covariance of the asset's returns with the market's returns divided by the variance of the market's returns. For Ethereum, we can define it as follows:

Let:

- $r_{ETH}$ be the return on Ethereum,
- $r_\mathsf{X}$ be the return on the market index or benchmark.

The beta of Ethereum ($\beta_\text{ETH}$) can be calculated by the formula:

$$ \beta*{\mathsf{X}} = \frac{\text{Cov}(r*\mathsf{X}, r*\text{ETH})}{\text{Var}(r*\mathsf{X})} $$

Where:

- $\text{Cov}(r_{ETH}, r_\mathsf{X})$ is the covariance between the returns on Ethereum and the market returns,
- $\text{Var}(r_\mathsf{X})$ is the variance of the market returns.

## Steps to Calculate Ethereum Beta

1. **Collect Data**: Obtain historical price data for Ethereum and the market index. This could be daily, weekly, or monthly closing prices depending on the desired analysis period.

2. **Compute Returns**: Calculate the periodic returns from the price data. The return at time $t$ fo token $a$, $r_{t,a}$, can be calculated using the formula:
   $$ r*{t,a} = \frac{P*{t,a} - P*{t-1,a}}{P*{t-1,a}} $$
   where $P_{t,a}$ is the price of token $a$ at time $t$ and $P_{t-1,a}$ is the price of token $a$ at time $t-1$.

3. **Calculate Covariance and Variance**: Use the return series to compute the covariance of Ethereum's returns with the market's returns, and the variance of the market's returns.

4. **Calculate Beta**: Apply the beta formula using the values from step 3.

## Interpretation

- **Beta > 1**: Ethereum is more volatile than the market. If the market increases by 1%, Ethereum is expected to increase by more than 1% (and vice versa for decreases).
- **Beta < 1**: Ethereum is less volatile than the market. If the market increases by 1%, Ethereum is expected to increase by less than 1% (and vice versa for decreases).
- **Beta = 1**: Ethereum's volatility matches the market. Movements in Ethereum's price are expected to closely follow the market.

## Model

We want to utilize the concept of beta where Ethereum (ETH) is the reference market, together with a CAPM model to construct an optimally diversified portfolio (referred to as Portfolio X), composed of various assets $(x_1,x_2,\dots,x_N)$. To do this, we will need to establish a framework that considers both the individual asset volatilities and their correlations with Ethereum. This can be approached using portfolio theory to maximize returns for a given level of risk or to minimize risk for a given level of expected return.

## Framework Overview

### Define Portfolio Beta

The beta of Portfolio X relative to Ethereum (ETH) is the weighted sum of the betas of the individual assets in the portfolio:

$$ \beta*\mathsf{X} = \sum*{i=1}^n w*i \beta*{x_i} $$

Here, $\beta\_{x_i} $ is the beta of asset $ x_i $ with respect to Ethereum, and $ w_i $ is the weight of asset $ x_i $ in Portfolio X.

## Objective Function

The goal could be to minimize variance, maximize returns, or find an optimal trade-off between the two (such as maximizing the Sharpe ratio). The objective function should incorporate the portfolio beta and the desired risk-return characteristics.

## Constraints

- The sum of the weights of all assets must equal 1: $\sum_{i=1}^n w_i = 1$
- Additional constraints may include limits on individual asset weights to avoid overexposure: $0 \leq w_i \leq 1$
- Optional constraints on the overall portfolio beta, such as $\beta_X \approx 1$, to maintain a market-neutral position or target a specific beta level.

## Risk and Return Models

- **Return Estimation**: Expected returns of assets $ \mu_i $ can be forecasted based on historical data or using a pricing model like the Capital Asset Pricing Model (CAPM).
- **Risk Estimation**: Covariance matrix of asset returns, $ \Sigma $, which captures the variance of each asset and the covariances between them.

## Optimization

- **Minimize Risk**: Solve for $ w $ in the quadratic optimization problem:
  $$\min_w w^T \Sigma w + (\beta_\mathsf{X}-1)^2$$
  subject to $ \sum\_{i=1}^n w_i = 1 $ and other constraints.
- **Maximize Utility** (e.g., Sharpe Ratio): Maximize
  $$ \frac{w^T \mu - r*f}{\sqrt{w^T \Sigma w}} - (\beta*\mathsf{X}-1)^2$$
  where $ r_f $ is the risk-free rate.
