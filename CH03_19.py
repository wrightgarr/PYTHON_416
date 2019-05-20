import numpy as np
import pandas as pd

project_cash_flows = [-256, 34, 44, 55, 67, 92, 70, 50]

cashflow_df = pd.DataFrame(project_cash_flows, columns=['cash_flows'])
cashflow_df['cumulative_cash_flows'] = np.cumsum(cashflow_df['cash_flows'])

full_years = cashflow_df[cashflow_df.cumulative_cash_flows < 0].index.values.max()

part_year = -cashflow_df.cumulative_cash_flows[full_years ]/cashflow_df.cash_flows[full_years + 1]
payback_period = full_years + part_year

print("The Payback Period is: {0:.2f} years.".format(payback_period))