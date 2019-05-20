def pv_perp(C, R, g):

	return C/(R-g)

pv = pv_perp(12.5, 8.5, 2.5)

print("The present value of the growing perpetuity is: ${0:.2f}".format(pv))
