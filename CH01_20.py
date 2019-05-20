def sharpe_ratio(Rb, Rf, sigma):

	return (Rb - Rf)/sigma

sr = sharpe_ratio(0.07, 0.03, 0.2)

print("Given Rb = 0.07, Rf = 0.04, and a sigma of 0.2, the sharpe ration is: {0:.2f}".format(sr))