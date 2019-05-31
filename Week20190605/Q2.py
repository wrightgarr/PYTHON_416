#!usr/bin/env python3
import pandas as pd
import numpy as np

credit_rating = ['AAA','AA','A','BBB','BB','B','CCC','D']

#Import data
infile = "./Resources/TransitionMatrix.xlsx"
transition_matrix = pd.read_excel(infile, index_col=0)
transition_matrix.columns = range(transition_matrix.shape[1])
#Bond rating lookup table
bond_rating_lookup_table = transition_matrix.cumsum()
#set seed
seed_number = 12345

##########################
#Two steps, one year each#
##########################

np.random.seed(seed_number)
transition_prob=pd.DataFrame(np.random.rand(1000,2))

bond_dict={
	0:'AAA',1:'AA',2:'A',3:'BBB',4:'BB',5:'B',6:'CCC',7:'D'
}
#One year step: step one
bond_final_rating_BBB = pd.DataFrame(np.searchsorted(bond_rating_lookup_table[3].values, transition_prob[0].values)).applymap(bond_dict.get)
#One year step: step two
bond_final_rating_BBB[1] = pd.DataFrame(np.searchsorted(bond_rating_lookup_table[0].values, transition_prob[1].values)).applymap(bond_dict.get).where(bond_final_rating_BBB[0]=='AAA',\
	pd.DataFrame(np.searchsorted(bond_rating_lookup_table[1].values, transition_prob[1].values)).applymap(bond_dict.get).where(bond_final_rating_BBB[0]=='AA',\
		pd.DataFrame(np.searchsorted(bond_rating_lookup_table[2].values, transition_prob[1].values)).applymap(bond_dict.get).where(bond_final_rating_BBB[0]=='A',\
			pd.DataFrame(np.searchsorted(bond_rating_lookup_table[3].values, transition_prob[1].values)).applymap(bond_dict.get).where(bond_final_rating_BBB[0]=='BBB',\
				pd.DataFrame(np.searchsorted(bond_rating_lookup_table[4].values, transition_prob[1].values)).applymap(bond_dict.get).where(bond_final_rating_BBB[0]=='BB',\
					pd.DataFrame(np.searchsorted(bond_rating_lookup_table[5].values, transition_prob[1].values)).applymap(bond_dict.get).where(bond_final_rating_BBB[0]=='B',\
						pd.DataFrame(np.searchsorted(bond_rating_lookup_table[6].values, transition_prob[1].values)).applymap(bond_dict.get).where(bond_final_rating_BBB[0]=='CCC',\
							'D')))))))

bond_count = bond_final_rating_BBB[1].value_counts()

bond_count_dict = {}
for i in credit_rating:
	try:
		bond_count_dict[i] = bond_count[i]
	except KeyError:
		bond_count_dict[i] = 0

print("\n##########################\n#Two steps, one year each#\n##########################")

print("\nNumber of bonds in each category at year end:")
for key in bond_count_dict:
	print("{}:".format(key), bond_count_dict["{}".format(key)])

print("\nProbability that the BBB bond ends up in each category:")
dict_sum = sum(bond_count_dict.values())
bond_prob_dict = {}
for key in bond_count_dict:
	bond_prob_dict[key] = float(bond_count_dict[key]/dict_sum)
	print("{}:".format(key), bond_prob_dict["{}".format(key)])


#####################
#One step, two years#
#####################

infile_2yr = "./Resources/TransitionMatrixTwoYear.xlsx"
transition_matrix_2yr = pd.read_excel(infile_2yr, index_col=0)
transition_matrix_2yr.columns = range(transition_matrix_2yr.shape[1])
#Bond rating lookup table
bond_rating_lookup_table_2yr = transition_matrix_2yr.cumsum()

np.random.seed(seed_number)
transition_prob_2yr=pd.DataFrame(np.random.rand(1000,1))
#Two year step:
bond_final_rating_BBB_2yr = pd.DataFrame(np.searchsorted(bond_rating_lookup_table_2yr[3].values, transition_prob_2yr[0].values)).applymap(bond_dict.get)

bond_count_2yr = bond_final_rating_BBB_2yr[0].value_counts()

bond_count_dict_2yr = {}
for i in credit_rating:
	try:
		bond_count_dict_2yr[i] = bond_count_2yr[i]
	except KeyError:
		bond_count_dict_2yr[i] = 0

print("\n#####################\n#One step, two years#\n#####################")

print("\nNumber of bonds in each category at year end:")
for key in bond_count_dict_2yr:
	print("{}:".format(key), bond_count_dict_2yr["{}".format(key)])

print("\nProbability that the BBB bond ends up in each category:")
dict_sum_2yr = sum(bond_count_dict_2yr.values())
bond_prob_dict_2yr = {}
for key in bond_count_dict_2yr:
	bond_prob_dict_2yr[key] = float(bond_count_dict_2yr[key]/dict_sum_2yr)
	print("{}:".format(key), bond_prob_dict_2yr["{}".format(key)])


