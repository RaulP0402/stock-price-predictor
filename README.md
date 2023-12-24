# stock-price-predictor
Building a stock price predictor using ML and Technical Analysis

# Goal for this project
I want to create a multivariable time series forecasting model to
predict information ratio (aka risk-reward) from technical indicators 
such as MA, S.E (Bollinger Bands), Momentum, Price, Volume, High, Low, 
Close, Open and more. 

Using predicted R/R , identify optimal portfolio allocation of S&P500 stocks 
and compare to benchmark SPY.(S&P ETF)

# Inputs of the model  (Multi-Input Long Short Term Memory (LSTM) neural network)
Matrix of Technical Indicators, calculated at at a 5 or 20 day lag, Wighted Random Sample.

# Output
R(s) - Return of each individual stock
R(m) - Return for the market (SPY)
SD(s) - standard deviation of stock

Using Mean Squared Error (MSE) we can see what the difference is between 
the actuall and predicted information ratio.

maximizing that can create a model to measure R/R



