def FV_calc(FV, years, rate):

	return FV/((1 + rate)**years)

deposit25 = FV_calc(25000, 5, 0.045)

print("We must deposit ${0:,.2f} today.".format(deposit25))
