import os

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_PATH = os.path.dirname(__file__) + '../dataset/'

# filter out papers without abstract information
def valid_format(input_file, output_file):
	with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
		papers = fin.read().split('\n\n')
		cnt = 0
		for paper in papers:
			attr = paper.split('\n')
			if attr[0].split()[0] != '#index' or \
			attr[1].split()[0] != '#*' or \
			attr[2].split()[0] != '#@' or \
			attr[3].split()[0] != '#t' or \
			attr[4].split()[0] != '#c' or \
			attr[-1].split()[0] != '#!':
				print paper
				print "\n"
				cnt += 1
				continue
			fout.write("{paper_info}\n\n".format(paper_info=paper))
		print "finally: ", cnt


def extract_title_abstract(input_file, output_file):
	with open(input_file,'r') as fin, open(output_file, 'w') as fout:
		papers = fin.read().split('\n\n')
		for paper in papers:
			attr = paper.split('\n')
			fout.write("{title}\n".format(title=attr[1][3:]))
			fout.write("{abstract}\n".format(abstract=attr[-1][3:]))


def sort_vocabulary_tfidf(input_file, output_file):
	with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
		documents = fin.read().split('\n')
		tfidf_vect = TfidfVectorizer()
		tfidf_mat = tfidf_vect.fit_transform(documents)
		term_id_name = tfidf_vect.get_feature_names()
		tfidf_sorted_indice = np.argsort(tfidf_vect.idf_)[::-1]
		for term_id in tfidf_sorted_indice:
			fout.write("{word}\n".format(word=term_id_name[term_id]))



def filter_phrases(input_file, output_file):
	with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
		lines = fin.read().split('\n')
		for line in lines:
			pass

if __name__ == "__main__":
	#valid_format(DATA_PATH + 'AP_after_1996_four_area_index_new',
	#	DATA_PATH + 'AP_after_1996_four_area_index_new_valid_abstract')
	
	#valid_format(DATA_PATH + 'AP_after_1996_four_area_index_new_valid_abstract', DATA_PATH+'aaa')
	#extract_title_abstract(DATA_PATH + 'latest_so_far', DATA_PATH + 'latest_raw_corpus')
	sort_vocabulary_tfidf(DATA_PATH + 'raw_corpus', 'sorted_tfidf_dict')
