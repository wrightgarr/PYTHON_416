#!usr/bin/env python3
import pandas as pd
import numpy as np
from scipy.stats import norm

#Set parameters
seed_number = 1234
#Import data
infile = "./Resources/TransitionMatrix.xlsx"
transition_matrix = pd.read_excel(infile, index_col=0)
transition_matrix.columns = range(transition_matrix.shape[1])
#Set Seed
np.random.seed(seed_number)
#Simulate Random Numbers
transitions_AAA=pd.DataFrame(norm.ppf(np.random.rand(20,10000)))
transitions_AA=pd.DataFrame(norm.ppf(np.random.rand(20,10000)))
transitions_A=pd.DataFrame(norm.ppf(np.random.rand(20,10000)))
transitions_BBB=pd.DataFrame(norm.ppf(np.random.rand(20,10000)))
transitions_BB=pd.DataFrame(norm.ppf(np.random.rand(20,10000)))
transitions_B=pd.DataFrame(norm.ppf(np.random.rand(20,10000)))
transitions_CCC=pd.DataFrame(norm.ppf(np.random.rand(20,10000)))

#Create Lookup Table
bond_rating_lookup_table = pd.DataFrame(norm.ppf(transition_matrix.cumsum()))

#Create a dictionary that will be mapped to the dataframe of transition outcomes
bond_dict={
	0:'AAA',1:'AA',2:'A',3:'BBB',4:'BB',5:'B',6:'CCC',7:'D'
}

#Calculate the transition outcome and map the corresponding bond rating
bond_final_rating_AAA = pd.DataFrame(np.searchsorted(bond_rating_lookup_table[0].values, transitions_AAA.values)).applymap(bond_dict.get)
bond_final_rating_AA = pd.DataFrame(np.searchsorted(bond_rating_lookup_table[1].values, transitions_AA.values)).applymap(bond_dict.get)
bond_final_rating_A = pd.DataFrame(np.searchsorted(bond_rating_lookup_table[2].values, transitions_A.values)).applymap(bond_dict.get)
bond_final_rating_BBB = pd.DataFrame(np.searchsorted(bond_rating_lookup_table[3].values, transitions_BBB.values)).applymap(bond_dict.get)
bond_final_rating_BB = pd.DataFrame(np.searchsorted(bond_rating_lookup_table[4].values, transitions_BB.values)).applymap(bond_dict.get)
bond_final_rating_B = pd.DataFrame(np.searchsorted(bond_rating_lookup_table[5].values, transitions_B.values)).applymap(bond_dict.get)
bond_final_rating_CCC = pd.DataFrame(np.searchsorted(bond_rating_lookup_table[6].values, transitions_CCC.values)).applymap(bond_dict.get)
#concatenate transitions of each bond into one dataframe
bond_final_rating=pd.concat([bond_final_rating_AAA,bond_final_rating_AA,bond_final_rating_A,bond_final_rating_BBB,bond_final_rating_BB,bond_final_rating_B,bond_final_rating_CCC])

#Spot Rates
spot_rates = pd.DataFrame([0.03,0.032,0.034,0.038,0.04,0.045])
spread=[0,0.001,0.002,0.005,0.01,0.017,0.07]
spread_dict={
	'AAA':0.0,
	'AA':0.001,
	'A':0.002,
	'BBB':0.005,
	'BB':0.01,
	'B':0.017,
	'CCC':0.07
}
for i in range(len(spread)):
	spot_rates[i]=spot_rates[0]+spread[i]

#Discounts
discounts = (1 + spot_rates).pow(-(spot_rates.index.to_series()+1), axis = 0)

#Cash flows
cash_flows = [4,4,4,4,4,104]

#Bond Starting Values
starting_values_dict={
	'AAA':(cash_flows * discounts[0]).sum(),
	'AA':(cash_flows * discounts[1]).sum(),
	'A':(cash_flows * discounts[2]).sum(),
	'BBB':(cash_flows * discounts[3]).sum(),
	'BB':(cash_flows * discounts[4]).sum(),
	'B':(cash_flows * discounts[5]).sum(),
	'CCC':(cash_flows * discounts[6]).sum()
}

#Bond Ending Values
ending_values_dict={}
for key in starting_values_dict:
	ending_values_dict[key] = starting_values_dict[key] * (1+spread_dict[key] + 0.03)
ending_values_dict['D'] = 40

#Starting Portfolio Value, mean, sd, skew
starting_portfolio_dict={}
for key in starting_values_dict:    
    starting_portfolio_dict[key] =starting_values_dict[key] * 20

bond_final_value = bond_final_rating.applymap(ending_values_dict.get)
portfolio_final_value = bond_final_value.sum()

print("\nThe starting value of the portfolio of 140 bonds is: ${:,.2f}".format(sum(starting_portfolio_dict.values())))
print("The mean value of the final portfolio 140 bonds is: ${:,.2f}".format(portfolio_final_value.mean()))
print("The standard deviation of the final portfolio 140 bonds is: ${:,.2f}".format(portfolio_final_value.std()))
print("The skew of the final portfolio 140 bonds is: {:,.2f}".format(portfolio_final_value.skew()))
