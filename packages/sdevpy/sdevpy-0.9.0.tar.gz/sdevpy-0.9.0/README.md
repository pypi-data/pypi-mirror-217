# SDev.Python

Python repository for various tools and projects in Machine Learning for Quantitative Finance. In the current release,
we focus on stochastic volatility surfaces and their calibration through Machine Learning methods. See other work on our main 
website [SDev-Finance](http://sdev-finance.com/) and [github](https://github.com/sebgur/SDev.Python).

## Stochastic volatility calibration

In this project we use Neural Networks to improve the calibration speed for stochastic volatility models. For now
we consider only the direct map, i.e. the calculation from model parameters to implied volatilities.

We first generate datasets of parameters (inputs) and vanilla option prices (outputs) and then train the network to replicate the prices.
In this manner, the learning model is used as a pricing function to replace costly closed-forms or PDE/MC price calculations.

Our models can be saved to files for later usage, and can be re-trained from a saved state. We cover (Hagan) SABR, No-Arbitrage SABR
(i.e. the actual SABR dynamic), Free-Boundary SABR, ZABR and Heston models.

Jupyter notebooks are available, trained models and datasets are available in our [github](https://github.com/sebgur/SDev.Python) and
[Kaggle account](https://www.kaggle.com/sebastiengurrieri/datasets).

## Other Tools

The package contains various other tools including Black-Scholes/Bachelier formulas, Monte-Carlo simulation of vanilla prices and 
other utilities. It also features a wrapper class above Keras for easier management of trained models with their scalers,
as well as custom callbacks and learning schedules.

Jupyter notebooks of previous work are also available [github](https://github.com/sebgur/SDev.Python) (PINNs, AAD Monte-Carlo),
waiting to be fully integrated here in a next iteration.