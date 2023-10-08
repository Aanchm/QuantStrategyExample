import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

prepared_data = pd.read_csv("stocks_data.csv", index_col = 'Date')
returns = prepared_data.pct_change(1)
log_returns = np.log(prepared_data).diff()

def set_up_plot(x_axis_title, y_axis_title):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,12))
    ax1.set_ylabel(x_axis_title)
    ax2.set_ylabel(y_axis_title)
    ax1.legend(loc='best')
    ax2.legend(loc='best')
    return fig, (ax1, ax2)


fig, (ax1, ax2) = set_up_plot('Cumulative log returns', 'Total relative returns (%)')

for stock in log_returns:
    ax1.plot(log_returns.index, log_returns[stock].cumsum(), label=str(stock))
    ax2.plot(log_returns.index, 100*(np.exp(log_returns[stock].cumsum()) - 1), label=str(stock))

plt.show()

# Get portfolio returns
weights_matrix = pd.DataFrame(1/len(prepared_data.columns), index=prepared_data.index, columns=prepared_data.columns)
weights_dot_returns = weights_matrix.dot(log_returns.transpose())
portfolio_log_returns = pd.Series(np.diag(weights_dot_returns), index=log_returns.index)
total_relative_returns = (np.exp(portfolio_log_returns.cumsum()) - 1)

fig, (ax1, ax2) = set_up_plot('Portfolio cumulative log returns','Portfolio total relative returns (%)')
ax1.plot(portfolio_log_returns.index, portfolio_log_returns.cumsum())
ax2.plot(total_relative_returns.index, 100 * total_relative_returns)
plt.show()

days_per_year = 52 * 5
total_days_in_simulation = len(prepared_data)
number_of_years = total_days_in_simulation / days_per_year

total_portfolio_return = total_relative_returns[-1]
average_yearly_return = (1 + total_portfolio_return)**(1 / number_of_years) - 1

print(f"Total_portfolio_return: {100*total_portfolio_return}% /n Average_yearly return: {100 * average_yearly_return}%")