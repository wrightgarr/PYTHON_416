#!usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

seed_number = 1234
norm_dist = "random_draws_normal.csv"

#import data
infile = norm_dist
random_numbers = pd.read_csv(infile, index_col=0)
random_numbers.columns = range(random_numbers.shape[1])
#parameters
mean = 0.065
theta = 0.2
#monthly mean is simply  =annual_mean/12 because returns are continuous (e^mu etc)
monthly_mean = mean/12
monthly_theta = theta/(12**(0.5))

returns = pd.DataFrame(random_numbers*monthly_theta + monthly_mean)
#values:
values = pd.DataFrame(index=range(random_numbers.shape[0]),columns=range(random_numbers.shape[1]))
values[0] = 200*np.exp(returns[0])

for i in range(1,random_numbers.shape[1]):
	values[i] = values[i-1]*np.exp(returns[i])

for i in (5,11,23):
	print()
	print("After {} months:".format(i+1))
	print("The mean asset value is: ${:,.2f}".format(values[i].mean()))
	print("The standard deviation is: ${:,.2f}".format(values[i].std()))
	print("The skew is: {:,.2f}".format(values[i].skew()))

month_12 = pd.DataFrame(values[11])
month_12['pdf'] = 1/month_12.shape[0]
month_12 = month_12.sort_values([11], ascending=[1])
month_12['cdf'] = month_12['pdf'].cumsum()

plt.plot(month_12[11],month_12['cdf'], color = 'royalblue', linewidth = 4)
plt.xlabel('Asset Value ($)')
plt.ylabel('Cumulative Probability')
plt.title("Simulated Probability Distribution in Month 12", loc='center')
plt.style.use('ggplot')
plt.show()