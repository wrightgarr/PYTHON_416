#!usr/bin/env python3
import pandas as pd
import numpy as np
import scipy
from scipy.stats import norm

################
#set parameters#
################
infile = "./Resources/TransitionMatrix.xlsx"
transition_matrix = pd.read_excel(infile, index_col=0)
transition_matrix.columns = range(transition_matrix.shape[1])
seed_number = 0

spot_rates = pd.DataFrame([0.03,0.032,0.034,0.038,0.04,0.045])
spread=[0,0.001,0.002,0.005,0.01,0.017,0.07]
for i in range(len(spread)):
	spot_rates[i]=spot_rates[0]+spread[i]
spread_dict={
	'AAA':0.0,'AA':0.001,'A':0.002,'BBB':0.005,'BB':0.01,'B':0.017,'CCC':0.07
}
cash_flows = [4,4,4,4,4,104]
discounts = (1 + spot_rates).pow(-(spot_rates.index.to_series()+1), axis = 0)

#Bond Starting Values
starting_values_dict={
	'AAA':(cash_flows * discounts[0]).sum(),'AA':(cash_flows * discounts[1]).sum(),'A':(cash_flows * discounts[2]).sum(),'BBB':(cash_flows * discounts[3]).sum(),'BB':(cash_flows * discounts[4]).sum(),'B':(cash_flows * discounts[5]).sum(),'CCC':(cash_flows * discounts[6]).sum()
}
#Bond Ending Values
ending_values_dict={}
for key in starting_values_dict:
	ending_values_dict[key] = starting_values_dict[key] * (1+spread_dict[key] + 0.03)
ending_values_dict['D'] = 40
#create transition values to define epsilons with
np.random.seed(seed_number)
transitions = pd.DataFrame(np.random.rand(1000,4))
#calculate normal inverse of transitions to get epsilons
epsilons = pd.DataFrame(norm.ppf(transitions))
#normal inverse of lookup table
bond_rating_lookup_df = pd.DataFrame(norm.ppf(transition_matrix.cumsum()))
#Create a dictionary that will be mapped to the dataframe of transition outcomes
bond_dict={
	0:'AAA',1:'AA',2:'A',3:'BBB',4:'BB',5:'B',6:'CCC',7:'D'
}
#Correlation Matrices
correlation_matrix_03 = np.array([
    [1, 0.3, 0.3, 0.3], 
    [0.3, 1, 0.3, 0.3],
    [0.3, 0.3, 1, 0.3],
    [0.3, 0.3, 0.3, 1]
    ])
correlation_matrix_zero = np.array([
    [1, 0, 0, 0], 
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
    ])
correlation_matrix_neg = np.array([
    [1, -0.3, -0.3, -0.3], 
    [-0.3, 1, -0.3, -0.3],
    [-0.3, -0.3, 1, -0.3],
    [-0.3, -0.3, -0.3, 1]
    ])

##############################
#Functions that will be used:#
##############################
def cholesky_decomp(correlmat):
	return scipy.linalg.cholesky(correlmat, lower=True)

def z_values(epsdf,chols):
	return epsdf.dot(chols.T)

def bond_final_rating(zvaluesdf, lookupsdf, ratingdict):
	bondfinalrating = pd.DataFrame(index = range(zvaluesdf.shape[0]))
	for i in range(zvaluesdf.shape[1]-2):
		bondfinalrating[i] = pd.DataFrame(np.searchsorted(lookupsdf[0].values, zvaluesdf[i].values)).applymap(ratingdict.get)
	for i in range(2,zvaluesdf.shape[1]):
		bondfinalrating[i] = pd.DataFrame(np.searchsorted(lookupsdf[3].values, zvaluesdf[i].values)).applymap(ratingdict.get)
	return bondfinalrating

def bond_value(bondfinalratingdf, endvaluesdict):
	bondfinalvalue = bondfinalratingdf.applymap(endvaluesdict.get)
	return bondfinalvalue

def portfolio_value(bondfinalvaluedf):
	portfoliovalue = bondfinalvaluedf.sum(axis=1)
	return portfoliovalue

def percentile(portfoliovaluedf,pctilevalue):
	pct = portfoliovaluedf.quantile(pctilevalue)
	return pct
###############
#Use functions#
###############
portfolio_value_03 = portfolio_value(bond_value(bond_final_rating(z_values(epsilons,cholesky_decomp(correlation_matrix_03)),bond_rating_lookup_df,bond_dict),ending_values_dict))
portfolio_value_zero = portfolio_value(bond_value(bond_final_rating(z_values(epsilons,cholesky_decomp(correlation_matrix_zero)),bond_rating_lookup_df,bond_dict),ending_values_dict))
portfolio_value_neg = portfolio_value(bond_value(bond_final_rating(z_values(epsilons,cholesky_decomp(correlation_matrix_neg)),bond_rating_lookup_df,bond_dict),ending_values_dict))

percentile_5_03 = percentile(portfolio_value_03,0.05)
percentile_5_zero = percentile(portfolio_value_zero,0.05)
percentile_5_neg = percentile(portfolio_value_neg,0.05)

def print_res(correl,portval,VAR):
	print("\nWhen mutual correlations = {}:".format(correl))
	print("The mean value of the final portfolio of four bonds is: ${:,.2f}".format(portval.mean()))
	print("The standard deviation of the final portfolio of four bonds is: ${:,.2f}".format(portval.std()))
	print("The skew of the final portfolio of four bonds is: {:,.2f}".format(portval.skew()))
	print("The VaR at {} percent of the final portfolio of four bonds is: ${:,.2f}".format(VAR,portval.mean()-percentile(portval,VAR)))
	return

print_res(0.3,portfolio_value_03,0.05)
print_res(0,portfolio_value_zero,0.05)
print_res((-0.3),portfolio_value_neg,0.05)


