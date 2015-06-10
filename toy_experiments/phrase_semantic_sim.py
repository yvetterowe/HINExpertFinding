from requests import get
from itertools import combinations
import os

DATA_PATH = os.path.dirname(__file__) + '/../dataset/'
sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"

def sss(s1, s2, type='relation', corpus='webbase'):
    try:
        response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2,'type':type,'corpus':corpus})
        return float(response.text.strip())
    except:
        print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        return 0.0

print sss("heterogen inform network", "heterogeneous information network")


def generate_top_sim_pairs(input_file, output_file):
	phrase_set = set()
	with open(input_file, 'r') as INPUT:
		for line in INPUT.read().split('\n'):
			phrase = line.split('\t')[0]
			phrase_set.add(phrase)
	phrase_pairs = combinations(phrase_set, 2)

	pair_score = dict()
	for phrase_pair in phrase_pairs:
		sim_score = sss(phrase_pair[0], phrase_pair[1])
		pair_score[phrase_pair] = sim_score
		print phrase_pair[0], phrase_pair[1], sim_score

	sorted_pair_score = sorted(pair_score.items(), key=operator.itemgetter(1), reverse=True)
	with open(output_file, 'w') as OUTPUT:
		for item in sorted_pair_score:
			OUTPUT.write("{phrase1}\t{phrase2}\t{score}\n".format(item[0][0], item[0][1], item[1]))

#generate_top_sim_pairs(DATA_PATH+'jiawei_han_stat', DATA_PATH + 'jiawei_han_sim')
