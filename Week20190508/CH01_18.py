import numpy as np
import re
a = np.array(dir(re))
numfun = len(a)
print("There are {0:,.0f} functions in the module re.".format(numfun))
