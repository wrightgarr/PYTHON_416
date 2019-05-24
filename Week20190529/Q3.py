#!usr/bin/env python3

import numpy as np
import pandas as pd
import scipy
import scipy.linalg

#Set parameters
seed_number = 1234

stock_file = "random_draws_stock.csv"
bond_file = "random_draws_bond.csv"
mm_file = "random_draws_mm.csv"

monthly_mean_stock = 0.07/12
monthly_sd_stock = 0.20/(12**0.5)
monthly_mean_bond = 0.05/12
monthly_sd_bond = 0.05/(12**0.5)
monthly_mean_mm = 0.03/12
monthly_sd_mm = 0.02/(12**0.5)

correlation_matrix=scipy.array([
	[1, 0.5, 0.1], 
	[0.5, 1, 0.8],
	[0.1, 0.8, 1],
	])

#Compute cholesky matrix
cholesky_decomp = scipy.linalg.cholesky(correlation_matrix, lower=True)

def Normal_Random_Nums(filename,mu,sigma,rows,columns,sd):
	np.random.seed(sd)
	x=pd.DataFrame(np.random.normal(mu,sigma,[rows,columns]))
	x.to_csv(filename)
	return x


Normal_Random_Nums(stock_file,0,1,100000,12,seed_number)
Normal_Random_Nums(bond_file,0,1,100000,12,seed_number)
Normal_Random_Nums(mm_file,0,1,100000,12,seed_number)


#Calculate Epsilons
random_numbers_stock = pd.read_csv(stock_file, index_col=0)
random_numbers_stock.columns = range(random_numbers_stock.shape[1])
epsilon_stock = pd.DataFrame(random_numbers_stock)

random_numbers_bond = pd.read_csv(bond_file, index_col=0)
random_numbers_bond.columns = range(random_numbers_bond.shape[1])
epsilon_bond = pd.DataFrame(random_numbers_bond)

random_numbers_mm = pd.read_csv(mm_file, index_col=0)
random_numbers_mm.columns = range(random_numbers_mm.shape[1])
epsilon_mm = pd.DataFrame(random_numbers_mm)

#Calculate returns
return_stock = monthly_mean_stock + epsilon_stock*cholesky_decomp[0][0]*monthly_sd_stock
return_bond = monthly_mean_bond + epsilon_stock*monthly_sd_bond*cholesky_decomp[1][0] + epsilon_bond*monthly_sd_bond*cholesky_decomp[1][1]
return_mm = monthly_mean_mm + epsilon_stock*monthly_sd_mm*cholesky_decomp[2][0] + epsilon_bond*monthly_sd_mm*cholesky_decomp[2][1] + epsilon_mm*monthly_sd_mm*cholesky_decomp[2][2]

#Calculate PV of each Asset
#stock
pv_stock = pd.DataFrame(index=range(return_stock.shape[0]),columns=range(return_stock.shape[1]))
pv_stock[0] = 50000*np.exp(return_stock[0])
for i in range(1,return_stock.shape[1]):
	pv_stock[i] = pv_stock[i-1]*np.exp(return_stock[i])
#bond
pv_bond = pd.DataFrame(index=range(return_bond.shape[0]),columns=range(return_bond.shape[1]))
pv_bond[0] = 30000*np.exp(return_bond[0])
for i in range(1,return_bond.shape[1]):
	pv_bond[i] = pv_bond[i-1]*np.exp(return_bond[i])
#mm
pv_mm = pd.DataFrame(index=range(return_mm.shape[0]),columns=range(return_mm.shape[1]))
pv_mm[0] = 20000*np.exp(return_mm[0])
for i in range(1,return_mm.shape[1]):
	pv_mm[i] = pv_mm[i-1]*np.exp(return_mm[i])

# Portfolio Value:
pv_portfolio = pv_stock + pv_bond + pv_mm

print("The mean of the final portfolio is: ${:,.2f}".format(pv_portfolio[pv_portfolio.shape[1]-1].mean()))
print("The standard deviation of the final portfolio is: ${:,.2f}".format(pv_portfolio[pv_portfolio.shape[1]-1].std()))
print("The skew of the final portfolio is: {:,.2f}".format(pv_portfolio[pv_portfolio.shape[1]-1].skew()))





