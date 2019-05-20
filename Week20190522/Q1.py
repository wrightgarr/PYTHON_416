#!usr/bin/env python3

import numpy as np
import pandas as pd

seed_number = 1234
uniform_dist = "random_draws_uniform.csv"
normal_dist = "random_draws_normal.csv"

#def CreateRandFileUniform(filename,observations,simulations,sd):
def Uniform_Random_Nums(filename,rows,columns,sd):
	np.random.seed(sd)
	x=pd.DataFrame(np.random.rand(rows,columns))
	x.to_csv(filename)
	return x

#def CreateRandFileUniform(filename,observations,simulations,sd):
def Normal_Random_Nums(filename,mu,sigma,rows,columns,sd):
	np.random.seed(sd)
	x=pd.DataFrame(np.random.normal(mu,sigma,[rows,columns]))
	x.to_csv(filename)
	return x