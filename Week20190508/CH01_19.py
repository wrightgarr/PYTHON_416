def annual_sigma(period, sigma):

	if period in ("M", "Monthly", "monthly", "m", "12"):
		return 12**0.5*sigma
	if period in ("D", "Daily", "daily", "d" "252"):
		return 252**0.5*sigma

daily_to_ann = annual_sigma("daily", 0.04)
monthly_to_ann = annual_sigma("monthly", 0.17)

print("Converting a daily sd of 0.04 to annual yeilds a sd of {0:.2f}".format(daily_to_ann))
print("Converting a monthly sd of 0.17 to annual yeilds a sd of {0:.2f}".format(monthly_to_ann))
