import os.path

import doc_meta as dmeta

def read_data(input_file):
	doc_meta_lst = []
	with open(input_file, 'r') as fin:
		papers = fin.read().split('\n\n')
		for paper in papers:
			attr_lst = paper.split('\n')
			paper_id = int(attr_lst[0].split()[1])
			authors = [int(a) for a in attr_lst[1][3:].split()]
			year = int(attr_lst[2].split()[1])
			venue = int(attr_lst[3].split()[1])
			citations = set()
			for citation in attr_lst[4:-1]:
				citations.add(int(citation.split()[1]))
			phrases = dict()
			for phrase in attr_lst[-1][3:].split(';'):
				phrases.setdefault(phrase, 1)
			doc_meta_lst.append(dmeta.DocMeta(
				doc_id=paper_id,
				phrases=phrases,
				authors=authors,
				venue=venue,
				citations=citations))
	return doc_meta_lst

def write_results(output_file):
	pass


if __name__ == '__main__':
	DATA_PATH = os.path.dirname(__file__) + '../dataset/'
	doc_meta_lst = read_data(DATA_PATH + 'AMiner-Paper-after1996-23venues-authorid-validcites-reindex-phrases.txt')
	print len(doc_meta_lst)
	for doc_meta in doc_meta_lst[:3]:
		print doc_meta.doc_id
		print doc_meta.phrases
		print "\n"
