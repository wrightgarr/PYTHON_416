import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
plt.style.use('ggplot')

filename = "hwdata1.xls"
df = pd.read_excel(filename, skiprows=9)
df.columns = ['PolicyholderID', 'LossAmount($)']
sorted_df = df.sort_values(by=['LossAmount($)'])

mean_loss = sorted_df['LossAmount($)'].mean()

sorted_df['l-mu'] = sorted_df['LossAmount($)'] - mean_loss
sorted_df['l-mu2'] = sorted_df['l-mu']**2
sorted_df['l-mu3'] = sorted_df['l-mu']**3
sorted_df['pdf'] = 1/len(sorted_df)
sorted_df['cdf'] = sorted_df['pdf'].cumsum()

variance = (sorted_df['LossAmount($)']*sorted_df['LossAmount($)']*sorted_df['pdf']).sum() - mean_loss**2
sd = (variance**(1/2))
skew = (sorted_df['pdf']*sorted_df['l-mu3']).sum()/(sd**3)

var_10 = 5000*0.9-4634
var_5 = 5000*0.95-4634
var_1 = 5000*0.99-4634

sorted_df.index = np.arange(0, len(df))
try:
	var_val_10 = sorted_df.loc[var_10]['LossAmount($)']
except KeyError:
	var_val_10 = 0
try:
	var_val_5 = sorted_df.loc[var_5]['LossAmount($)']
except KeyError:
	var_val_5 = 0
try:
	var_val_1 = sorted_df.loc[var_1]['LossAmount($)']
except KeyError:
	var_val_1 = 0

#Output results
print("")
print("Mean Loss Amount: ${0:,.2f}".format(mean_loss))
print("Standard Deviation of Losses: ${0:,.2f}".format(sd))
print("Skew of distributiuon: {0:,.2f}".format(skew))

print("The VaR(10 percent): ${0:,.2f}".format(var_val_10))
print("The VaR(5 percent): ${0:,.2f}".format(var_val_5))
print("The VaR(1 percent): ${0:,.2f}".format(var_val_1))

#Plot using matplotlib
fig, ax = plt.subplots()
plt.plot(sorted_df['LossAmount($)'], sorted_df['cdf'], linewidth=4)
plt.xlabel("Loss Amount ($)")
plt.ylabel("Cumulative Probability")

fmt = '${x:,.0f}'
cumval = mtick.StrMethodFormatter(fmt)
ax.xaxis.set_major_formatter(cumval)

plt.title("HWDATA1", loc='center')
plt.show()