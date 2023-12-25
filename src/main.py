import random
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import statistics

tsla = yf.Ticker('tsla')
his = tsla.history(period='max')

gap=20 # 20 day period
lentsla = len(his['Close'])
mvavg = []
price = []
upper_stdev = []
lower_stdev = []
indx = []

# For each closing price
for i in range(lentsla - 200, lentsla):
    mean = his['Close'][i:i+gap].mean()
    mvavg.append(mean)
    upper_stdev.append(mean + 2*his['Close'][i:i+gap].std())
    lower_stdev.append(mean - 2*his['Close'][i:i+gap].std())
    indx.append(i)

# plot it all
plt.plot(indx, mvavg)
plt.plot(indx, upper_stdev)
plt.plot(indx, lower_stdev)

# plt.show()

# Combine 
# print(pd.DataFrame([mvavg, upper_stdev, lower_stdev]))


# Create table of multiple tickers, list of SP500 Companies
table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

# Get symbols
symbols = list(table[0]['Symbol'])
stockdict={}
for stock in symbols:
    ticker = yf.Ticker(stock)
    if ticker:
        history = ticker.history(period='max')
        if not history.empty:
            stockdict[stock] = history

spy = yf.Ticker("spy").history(period='max')


#---------------------------------------------------------------------------------
# SAMPLING:
# Obtains measurements of 5 random days, to predict avg risk adjusted return in the next 5 days.
#---------------------------------------------------------------------------------
predict = 5
gap=5
y = []
x = []
ticker = []

for stock in stockdict.keys():
    security=stockdict[stock]
    merged = pd.merge(spy, security, left_index=True, right_index=True)
    lenstock = len(merged) - gap - predict
    start = random.choice(range(0, lenstock))

    mvavg = []
    price = []
    upper_stdev = []
    lower_stdev = []
    indx = []
    oscilation = []
    price = []
    predicted_price = []
    spy_price = []
    spy_predicted_price = []

    # For each closing price
    for i in range(start, start+gap):
        mean = merged['Close_x'][i:i+gap].mean()
        mvavg.append(mean)
        upper_stdev.append(mean + 2*merged['Close_x'][i:i+gap].std())
        lower_stdev.append(mean - 2*merged['Close_x'][i:i+gap].std())
        indx.append(i)
        oscilation.append((merged["Close_x"][i] - merged["Close_x"][i+gap])/merged["Close_x"][i+gap])
        price.append(merged["Close_x"][i])
        predicted_price.append(merged["Close_x"][i+predict])
        spy_price.append(merged["Close_y"][i])
        spy_predicted_price.append(merged["Close_y"][i+predict])

    temp_data = pd.DataFrame([mvavg, upper_stdev, lower_stdev, oscilation])
    temp_data=temp_data.T
    temp_merged = merged[start:start+gap]
    temp_data.index = temp_merged.index

    return_of_stock = []
    return_of_spy = []
    for i in range(0, len(predicted_price)):
        return_of_stock.append(predicted_price[i] - price[-1])
        return_of_spy.append(spy_predicted_price[i] - spy_price[-1])

    exp_r_and_r_ratio = (sum(return_of_stock)/len(return_of_stock) - sum(return_of_spy)/len(return_of_spy))/statistics.stdev(return_of_stock)
    y.append(exp_r_and_r_ratio)
    x.append(pd.merge(temp_data, temp_merged,right_index=True,left_index=True))
    ticker.append(stock)

print(x)


