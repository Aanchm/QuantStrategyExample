import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yfin
from datetime import date

import os, sys

tickers = ['SPY', 'AAPL', 'MSFT']
past_years_to_analyse = 5
data_col = "Close"
csv_file_name = f"{os.path.dirname(os.path.realpath(__file__))}\stocks_data.csv"

def prepare_data(data, date_bounds, column_name):
    business_days = pd.date_range(start=date_bounds[0], end=date_bounds[1], freq='B')
    close_data = data[column_name].reindex(business_days)

    return close_data


def get_last_n_years_data(n):
    end_date = str(date.today())
    start_year = str(int(end_date[0:4]) - n)
    start_date = end_date.replace(end_date[0:4], start_year)

    return [start_date, end_date]


def get_rolling_average_for_stock(stock_data, window):
    return stock_data.rolling(window=window).mean()


yfin.pdr_override()
date_bounds = get_last_n_years_data(past_years_to_analyse)
data = pdr.get_data_yahoo(tickers, start=date_bounds[0], end=date_bounds[1])
prepared_data = prepare_data(data, date_bounds, data_col)

prepared_data.to_csv(csv_file_name, index_label = 'Date')

stock_to_analyse = 'MSFT'
stock_data = prepared_data.loc[:, stock_to_analyse]
short_rolling_av = get_rolling_average_for_stock(stock_data, 20)
long_rolling_av = get_rolling_average_for_stock(stock_data, 100)

returns = prepared_data.pct_change(1)
log_returns = np.log(prepared_data).diff()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(stock_data.index, stock_data, label=stock_to_analyse)
ax.plot(short_rolling_av.index, short_rolling_av, label='20 days rolling')
ax.plot(long_rolling_av.index, long_rolling_av, label='100 days rolling', color = 'black')
ax.set_xlabel('Date')
ax.set_ylabel(f'{data_col} price ($)')
ax.legend()
plt.show()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,12))

for stock in log_returns:
    ax1.plot(log_returns.index, log_returns[stock].cumsum(), label=str(stock))
    ax2.plot(log_returns.index, 100*(np.exp(log_returns[stock].cumsum()) - 1), label=str(stock))

ax1.set_ylabel('Cumulative log returns')
ax2.set_ylabel('Total relative returns (%)')
ax1.legend(loc='best')
ax2.legend(loc='best')

plt.show()