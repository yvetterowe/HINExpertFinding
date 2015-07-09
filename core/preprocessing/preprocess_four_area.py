import os
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_PATH = os.path.dirname(__file__) + '/../dataset/'

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


def extract_title_abstract(input_file, output_file, output_map):
	with open(input_file,'r') as fin, open(output_file, 'w') as fout, open(output_map, 'w') as fout_map:
		papers = fin.read().split('\n\n')
		for paper in papers:
			attr = paper.split('\n')
			paper_id = int(attr[0].split()[1])
			print paper_id
			corpus_cnt = 1
			fout.write("{title}\n".format(title=attr[1][3:]))
			last_prefix = attr[-1].split()[0]
			if last_prefix == '#!':
				fout.write("{abstract}\n".format(abstract=attr[-1][3:]))
				corpus_cnt = 2
			fout_map.write("{paper_id} {cnt}\n".format(paper_id=paper_id, cnt=corpus_cnt))



def sort_vocabulary_tfidf(input_file, output_file):
	with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
		documents = fin.read().split('\n')
		tfidf_vect = TfidfVectorizer()
		tfidf_mat = tfidf_vect.fit_transform(documents)
		term_id_name = tfidf_vect.get_feature_names()
		tfidf_sorted_indice = np.argsort(tfidf_vect.idf_)[::-1]
		for term_id in tfidf_sorted_indice:
			fout.write("{word}\n".format(word=term_id_name[term_id]))

def blah(input_file, label):
	with open(input_file, 'r') as fin:
		lines = fin.read().split('\n')
		for line in lines:
			phrase_cnt = line.split()
			phrase_cnt[-1] = str(label)
			print ' '.join(phrase_cnt)

def filter_phrases(input_file, output_file):
	with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
		lines = fin.read().split('\n')
		#for line in lines:
		for line_id in xrange(len(lines)):
			if line_id % 2:
				continue
			print line_id
			phrases = list(set(re.findall(r'\[(.+?)\]', lines[line_id]) + re.findall(r'\[(.+?)\]', lines[line_id + 1])))
			fout.write("{phrases}\n".format(phrases=';'.join(phrases)))

# map each paper's title & abstract -> preprocessed phrases
def map_raw_title_abstract_to_phrases(input_raw, input_phrase, output):
	with open(input_raw, 'r') as fin_raw, open(input_phrase, 'r') as fin_phrase, open(output, 'w') as fout:
		papers = fin_raw.read().split('\n\n')
		phrases = fin_phrase.read().split('\n')
		paper_id = 0
		for paper in papers:
			meta = paper.split('\n')
			new_meta = meta[0] + '\n' + '\n'.join(meta[2:-1]) + '\n' + '#! ' + phrases[paper_id]
			paper_id += 1
			fout.write("{paper_meta}\n\n".format(paper_meta=new_meta))

def map_venue_name_to_id(input_file, output_file, venue_dict):
	with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
		pass
		papers = fin.read().split('\n\n')
		for paper in papers:
			meta = paper.split('\n')
			venue = meta[3][3:]
			venue_splits = venue.split()
			find = False
			if venue.find('KDD') != -1 and venue.find("ECML PKDD") == -1 and venue.find("PKDD") == -1 and venue.find("TKDD") != -1:
				print venue

def extract_papers_by_venues(input_file, venue_feature_dict, venue_name_id_dict):
	fouts = dict()
	for key in venue_feature_dict:
		fouts[key] = open(DATA_PATH + 'papers_by_venues/' +'v_' + key, 'w')
	fin = open(input_file, 'r')

	papers = fin.read().split('\n\n')
	cnt = 0
	for paper in papers:
		print cnt
		lines = paper.split('\n')
		line = lines[4][3:].lower()
		#print line
		found = False
		line_venue = None
		for venue, features in venue_feature_dict.items():
			for feature in features:
				if line.find(feature.lower()) != -1:
					found = True
					line_venue = venue
					break
			if found:
				break
		if found:
			#fouts[line_venue].write("{original_venue}\n".format(original_venue=line))
			paper_with_venue_id = '\n'.join(lines[0:4]) + '\n'+ '#c ' + str(venue_name_id_dict[line_venue]) 
			if len(lines) > 5:
				paper_with_venue_id += '\n' + '\n'.join(lines[5:])
			fouts[line_venue].write("{paper_info}\n\n".format(paper_info=paper_with_venue_id))
		cnt += 1
	fin.close()
	for fout in fouts.values():
		fout.close()

def extract_papers_by_venues_special_cases(input_file, target_venue, venue_name_id_dict, whitelist, blacklist):
	with open(input_file, 'r') as fin, open(DATA_PATH + 'papers_by_venues/' + 'v_' + target_venue, 'w') as fout:
		papers = fin.read().split('\n\n')
		cnt = 0
		for paper in papers:
			print cnt
			meta = paper.split('\n')
			venue = meta[4][3:].lower()
			valid = False
			for white in whitelist:
				if venue.find(white.lower()) != -1:
					valid = True
					break
			if valid:
				for black in blacklist:
					if venue.find(black.lower()) != -1:
						valid = False
						break
			if valid:
				#fout.write("{original_venue}\n".format(original_venue=venue))
				paper_with_venue_id = '\n'.join(meta[0:4]) + '\n'+ '#c ' + str(venue_name_id_dict[target_venue])
				if len(meta) > 5:
					paper_with_venue_id += '\n' + '\n'.join(meta[5:])
				fout.write("{paper_info}\n\n".format(paper_info=paper_with_venue_id))
			cnt += 1


def filter_by_venue(input_file, output_file, venue_features):
	with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
		papers = fin.read().split('\n\n')
		for paper in papers:
			venue = paper.split('\n')[3][3:].lower()
			for feature in venue_features:
				if venue.find(feature.lower()) != -1:
					fout.write("{venue_name}\n".format(venue_name=venue))
					break

venue_feature_dict = {
	'KDD' : ['acm sigkdd international conference on knowledge discovery and data mining'], 
	'CIKM' : ['CIKM', 'international conference on Information and knowledge management'],
	'WSDM' : ['WSDM', 'ACM International Conference on Web Search and Data Mining'],
	'PAKDD': ['PAKDD'],
	'VLDB' : ['proceedings of the vldb endowment', 'international conference on very large data bases'],
	'SIGMOD' :['SIGMOD', 'International Conference on Management of Data', 'symposium on principles of database systems'],
	'ICDT' : ['international conference on database theory'],
	'TKDE' : ['IEEE Transactions on Knowledge and Data Engineering'],
	'EDBT' : ['Extending Database Technology'],
	'RS' : ['ACM Conference on Recommender Systems'],
	'AAAI': ['AAAI'],
	'IJCAI' : ['IJCAI'],
	'UAI' : ['uncertainty in artificial intelligence'],
	'SIGIR' : ['acm sigir conference on research and development in information retrieval'],
	'JCDL' : ['Joint Conference on Digital Libraries'],
	'ECDL' : ['ECDL'],
	'ECIR' : ['ECIR'],
}

venue_name_id = {
	'KDD' : 0,
	'CIKM' : 1,
	'WSDM' : 2,
	'PAKDD': 3,
	'VLDB' : 4,
	'SIGMOD' : 5,
	'ICDT' : 6,
	'TKDE' : 7,
	'EDBT' : 8,
	'RS' : 9,
	'AAAI': 10,
	'IJCAI' : 11,
	'UAI' : 12,
	'SIGIR' : 13,
	'JCDL' : 14,
	'ECDL' : 15,
	'ECIR' : 16,
	'ICDE' : 17,
	'ICDM' : 18,
	'ICML' : 19,
	'ECML' : 20,
	'PKDD' : 21,
	'ECMLPKDD' : 22,
}

def delete_invalid_citations(input_file, output_file):
	with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
		papers = fin.read().split('\n\n')
		paper_ids = set()
		for paper in papers:
			meta = paper.split('\n')
			paper_id = int(meta[0].split()[1])
			paper_ids.add(paper_id)

		absent_cnt = 0
		total_cnt = 0
		for paper in papers:
			meta = paper.split('\n')
			fout.write("{before_citation}\n".format(before_citation='\n'.join(meta[0:5])))
			for line in meta[5:-1]:
				cite = int(line.split()[1])
				total_cnt += 1
				if not cite in paper_ids:
					absent_cnt += 1	
					print cite
				else:
					fout.write("{cite}\n".format(cite=line))
			last_line_prefix = meta[-1].split()[0]
			if last_line_prefix == '#!':
				fout.write("{abstract}\n".format(abstract=meta[-1]))
			fout.write("\n")
		print "ahahaha finally ", absent_cnt, total_cnt

def reindex_paper(input_file, output_file):
	with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
		papers = fin.read().split('\n\n')
		paper_ids = dict()
		new_id = 0
		for paper in papers:
			meta = paper.split('\n')
			print meta[0]
			old_id = int(meta[0].split()[1])
			paper_ids[old_id] = new_id
			new_id += 1

		for paper in papers:
			meta = paper.split('\n')
			old_id = int(meta[0].split()[1])
			fout.write("#index {new_id}\n".format(new_id=paper_ids[old_id]))
			fout.write("{before_citation}\n".format(before_citation='\n'.join(meta[1:5])))
			for line in meta[5:-1]:
				old_cite_id = int(line.split()[1])
				fout.write("#% {new_cite_id}\n".format(new_cite_id=paper_ids[old_cite_id]))
			last_line_prefix = meta[-1].split()[0]
			if last_line_prefix == '#!':
				fout.write("{abstract}\n".format(abstract=meta[-1]))
			fout.write("\n")


if __name__ == "__main__":
	#valid_format(DATA_PATH + 'AP_after_1996_four_area_index_new',
	#	DATA_PATH + 'AP_after_1996_four_area_index_new_valid_abstract')
	#valid_format(DATA_PATH + 'AP_after_1996_four_area_index_new_valid_abstract', DATA_PATH+'aaa')
	extract_title_abstract(DATA_PATH + 'AMiner-Paper-after1996-23venues-authorid-validcites-reindex.txt', 
		DATA_PATH + 'title_abstract_corpus_raw',
		DATA_PATH + 'paper_cnt_map')
	#sort_vocabulary_tfidf(DATA_PATH + 'raw_corpus', 'sorted_tfidf_dict')
	#blah(DATA_PATH + 'topic_ir', 1)
	#filter_phrases(DATA_PATH + 'parsed.txt', DATA_PATH + 'parsed_phrases.txt')
	#filter_phrases(DATA_PATH + 'segment_title_abstract_corpus', DATA_PATH + 'title_abstract_phrases')

	#map_raw_title_abstract_to_phrases(DATA_PATH + 'latest_so_far', DATA_PATH + 'title_abstract_phrases', DATA_PATH + 'latest_so_far_phrases')

	#map_venue_name_to_id(DATA_PATH + 'latest_so_far_phrases', DATA_PATH + 'latest_so_far_phrases_ids', {})

	#filter_by_venue(DATA_PATH + 'AMiner-Paper.txt', DATA_PATH + 'v_sigkdd', ['ACM SIGKDD'])

	'''extract_papers_by_venues(DATA_PATH + 'AMiner-Paper-after1996.txt', venue_feature_dict, venue_name_id)
	
	extract_papers_by_venues_special_cases(DATA_PATH + 'AMiner-Paper-after1996.txt',
		'ICDE',
		venue_name_id,
		['International Conference on Data Engineering','ICDE'],
		['ICDEW', 'ICDEM'],
		)
	extract_papers_by_venues_special_cases(DATA_PATH + 'AMiner-Paper-after1996.txt',
		'ICDM',
		venue_name_id,
		['ICDM', 'IEEE International Conference on Data Mining'],
		['ICDMW', 'ICDMA'],
		)
	extract_papers_by_venues_special_cases(DATA_PATH + 'AMiner-Paper-after1996.txt',
		'ICML',
		venue_name_id,
		['International Conference on Machine Learning'],
		['ICMLA', 'ICMLC', 'mldm', 'mlmi' ,'mlcw'],
		)
	extract_papers_by_venues_special_cases(DATA_PATH + 'AMiner-Paper-after1996.txt',
		'ECML',
		venue_name_id,
		['ECML'],
		['ECML PKDD', 'ECML/PKDD'],
		)
	extract_papers_by_venues_special_cases(DATA_PATH + 'AMiner-Paper-after1996.txt',
		'PKDD',
		venue_name_id,
		['PKDD'],
		['ECML PKDD', 'ECML/PKDD'],
		)
	extract_papers_by_venues_special_cases(DATA_PATH + 'AMiner-Paper-after1996.txt',
		'ECMLPKDD',
		venue_name_id,
		['ECML PKDD', 'ECML/PKDD'],
		[],
		)'''
	#delete_invalid_citations(DATA_PATH + 'AMiner-Paper-after1996-23venues-authorid.txt', DATA_PATH + 'AMiner-Paper-after1996-23venues-authorid-validcites.txt')
	#reindex_paper(DATA_PATH + 'AMiner-Paper-after1996-23venues-authorid-validcites.txt', DATA_PATH + 'AMiner-Paper-after1996-23venues-authorid-validcites-reindex.txt')



