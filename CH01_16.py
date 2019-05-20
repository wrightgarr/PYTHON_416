def sigma_days(days, daily_sigma):
	
	return days*daily_sigma

sigma10 = sigma_days(10, 0.2)

print("The 10-day volatility is ${0:.2f}".format(sigma10))