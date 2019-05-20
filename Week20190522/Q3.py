#!usr/bin/env python3

import numpy as np
import pandas as pd

#import data
infile = "random_draws_uniform.csv"
random_numbers = pd.read_csv(infile, index_col=0)
random_numbers.columns = range(random_numbers.shape[1])
#parameters
theta = 0.25
rate_i = [0.05]
#Calculate rates
# create rates df
rates = pd.DataFrame(index=range(random_numbers.shape[0]),columns=range(random_numbers.shape[1]))
rates[0] = rate_i[0]

for i in range(1,random_numbers.shape[1]):
	rates[i] = (rates[i-1]*0.75).where(random_numbers[i-1]<=0.5, (rates[i-1]*0.75*np.exp(0.5)))

#Calculate Cashflows
# create empty cashflows df
cashflows = pd.DataFrame(index=range(random_numbers.shape[0]),columns=range(random_numbers.shape[1]))
cashflows[0] = 15000
#handling the maximum/minimum condition:
rate_cap = pd.DataFrame(index=range(random_numbers.shape[0]),columns=range(random_numbers.shape[1]))
#second condition of the max/min
rate_cap['cap_max'] = 0.06
for i in range(random_numbers.shape[1]):
	rate_cap[i] = (rates[i] - 0.06).where((rates[i] - 0.06)>0,0)
#first condition of the max/min
rate_cap['cap_min'] = 0.05
for i in range(random_numbers.shape[1]):
	rate_cap[i] = (rate_cap['cap_min']).where((rate_cap['cap_min']-rate_cap[i])<0,rate_cap[i])

#populate the cashflows df
for i in range(1,random_numbers.shape[1]):
	cashflows[i] = cashflows[i-1]*(1+rate_cap[i])

#Calculate Present Values
# create present values df
presentvalues = pd.DataFrame(index=range(random_numbers.shape[0]),columns=range(random_numbers.shape[1]))
presentvalues[random_numbers.shape[1]-1]=cashflows[random_numbers.shape[1]-1]
#populate presentvalues df
for i in range(random_numbers.shape[1]-2,-1,-1):
	presentvalues[i] = presentvalues[i+1]/(1+rates[i])+cashflows[i]

#Answer
print("The expected present value of the annuity is ${:,.2f}".format(presentvalues[0].mean()))

