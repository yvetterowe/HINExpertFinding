import numpy as np
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize
import random

def print_list(lst, num_col):
	num_row = len(lst) / num_col
	return '\n'.join([(' '.join([str(x) for x in lst[i*num_col:(i+1)*num_col]])) for i in xrange(num_row)])
#print print_list([1,2,3,4,5,6], 3)


def play_random_lst(lst):
	sample_num = random.randint(0,len(lst)-1)
	return ' '.join([str(x) for x in random.sample(lst, sample_num)])


ll = [i for i in xrange(40,49)]
print play_random_lst(ll)