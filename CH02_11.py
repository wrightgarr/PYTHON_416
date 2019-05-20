import numpy as np

def ari_geo_mean(array, meantype):
	a = np.array(array)
	geometric = a.prod()**(1.0/len(a))
	arithmetic = a.sum()/len(a)
	if meantype in ("g", "G", "geometric", "Geometric"):
		return geometric
	if meantype in ("a", "A", "arithmetic", "Arithmetic"):
		return arithmetic


r = [1+0.05, 1+0.11, 1-0.03]

g_mean = ari_geo_mean(r, "G") - 1
a_mean = ari_geo_mean(r, "A") - 1

print("Geometric mean: {0:.3f}".format(g_mean))
print("Arithmetic mean: {0:.3f}".format(a_mean))
