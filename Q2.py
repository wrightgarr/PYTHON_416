import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

initial = 20000
rate = 1.05
yrs = np.arange(0,51)

FV = np.around(initial*rate**yrs, decimals=2)
cum_val = pd.DataFrame(FV, columns=['CumulativeValue'])
future_value = cum_val.values.max()
print("The Accumulated value in 50 yrs is: ${0:,.2f}".format(future_value))

#Plot using matplotlib
plt.plot(cum_val, color = 'royalblue')
plt.scatter(cum_val.index,cum_val)

plt.xlabel("Year")
plt.ylabel("Accumulated value")
plt.title("50 year cumulative value", loc='center')

plt.show()