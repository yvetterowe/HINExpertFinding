import operator
import os.path
#from nlp_preprocessing import *
#from nlp_preprocessing import NPChuncker

DATA_PATH = os.path.dirname(__file__) + '/../dataset/'

def filter_by_attr(input_file, output_file, attr_key, attr_value):
	with open(input_file, 'r') as INPUT:
		with open(output_file, 'w') as OUTPUT:
			paper_list = INPUT.read().split('\n\n')
			cnt = 0
			for paper in paper_list:
				attr_list = paper.split('\n')
				#print "aha"
				#print attr_list[0:4]
				valid = False
				if attr_key == 'year':
					paper_year = attr_list[4].split(' ')[1]
					#print paper_year
					valid = paper_year and int(paper_year) >= attr_value
				if valid:
					print cnt
					extract_paper = '\n'.join(attr_list[0:3]) + '\n' + '\n'.join(attr_list[4:])
					OUTPUT.write('{paper}\n\n'.format(paper=extract_paper))
					cnt += 1

def extract_titles_by_author(input_file, output_file, target_author):
	with open(input_file, 'r') as INPUT:
		with open(output_file, 'w') as OUTPUT:
			paper_list = INPUT.read().split('\n\n')
			for paper in paper_list:
				attr_list = paper.split('\n')
				author_list = [author.strip() for author in attr_list[2][3:].split()]
				if target_author in author_list:
					OUTPUT.write('{paper_title}.\n'.format(paper_title=attr_list[1][3:]))

def extract_by_attr(input_file, output_file, attr_id):
	with open(input_file, 'r') as INPUT:
		with open(output_file, 'w') as OUTPUT:
			paper_list = INPUT.read().split('\n\n')
			for paper in paper_list:
				attr_list = paper.split('\n')
				OUTPUT.write('{attr}\n'.format(attr=attr_list[attr_id][3:]))

def write_dict_to_file(input_dict, output_file):
	with open(output_file, 'w') as OUTPUT:
		for key, value in input_dict.items():
			OUTPUT.write('{key}\t{value}\n'.format(key=key, value=value))

def indexify(input_file, output_index_file, output_author_file, black_list):
	with open(input_file, 'r') as INPUT:
		author_name_id = dict()
		paper_list = INPUT.read().split('\n\n')
		author_num = 0

		OUTPUT = open(output_index_file, 'w')
		cnt = 0
		for paper in paper_list:
			print cnt
			cnt += 1
			attr_list = paper.split('\n')
			for attr in attr_list:
				if attr[1] in black_list:
					continue
				elif attr[1] == '@': 
					author_list = [a.strip().lower() for a in attr[3:].split(';')]
					author_index_str = '#@'
					for author in author_list:
						if not author in author_name_id:
							author_name_id[author] = author_num
							author_num += 1
						author_index_str += " " + str(author_name_id[author])
					OUTPUT.write('{authors}\n'.format(authors=author_index_str))
				else:
					OUTPUT.write('{curr_attr}\n'.format(curr_attr=attr))
			OUTPUT.write('\n')		
		OUTPUT.close()

		write_dict_to_file(author_name_id, output_author_file)

def chunck_titles(input_file, output_file):
	with open(input_file, 'r') as INPUT:
		with open(output_file, 'w') as OUTPUT:
			paper_list = INPUT.read().split('\n\n')
			for paper in paper_list:
				attr_list = paper.split('\n')
				for attr in attr_list:
					if attr[1] == '*':
						title = attr[3:]
						phrases = NPChuncker.parse_sentence(title)
						nps = ';'.join([(' '.join(phrase)) for phrase in phrases])
						OUTPUT.write('#* {np_list}\n'.format(np_list=nps))
					else:
						OUTPUT.write('{curr_attr}\n'.format(curr_attr=attr))
				OUTPUT.write('\n')

def generate_author_phrase_rank_list(input_file, output_file):
	phrase_cnt = dict()
	with open(input_file, 'r') as INPUT:
		titles = INPUT.read().decode('utf-8')
		phrase_list = NPChuncker.parse_corpus(titles)
		for word_list in phrase_list:
			phrase = ' '.join(word_list)
			if not phrase in phrase_cnt:
				phrase_cnt[phrase] = 1
			else:
				phrase_cnt[phrase] += 1
	phrase_cnt_sorted = sorted(phrase_cnt.items(), key=operator.itemgetter(1), reverse=True)
	with open(output_file, 'w') as OUTPUT:
		for item in phrase_cnt_sorted:
			OUTPUT.write('{phrase}\t{cnt}\n'.format(phrase=item[0], cnt=item[1]))

'''
	1. lower
	2. normalize (stem & lemitazaion)
'''
def norm_file(input_file, output_file, lower=True, stem=False):
	with open(input_file, 'r') as INPUT:
		with open(output_file, 'w') as OUTPUT:
			for line in INPUT.read().split('\n'):
				if lower:
					line = line.lower()
				if stem:
					segs = line.split()
					line = " ".join([normalize_word(w) for w in segs[:-1]]) + "\t" + segs[-1]
				OUTPUT.write("{line}\n".format(line=line))


'''
input: a list of authors (id), paper meta data file
output: all paper meta data of authors (one file for each authors)
'''
def extract_paper_by_author(author_list, input_file):
	OUTPUT_PATH = DATA_PATH + 'author/'
	with open(input_file, 'r') as fin:
		# create output handler for each author
		fouts = dict()
		for author in author_list:
			fouts[author] = open(OUTPUT_PATH + str(author), 'w')

		# ran through all file and write
		paper_list = fin.read().split('\n\n')
		for paper in paper_list:
			attr_list = paper.split('\n')
			authors = [int(a) for a in attr_list[2][3:].strip().split()]
			valid_authors = [a for a in author_list if a in authors]
			for a in valid_authors:
				fouts[a].write('{p}\n\n'.format(p=paper))


def main():
	#filter_by_attr(DATA_PATH + 'test_input', DATA_PATH+ "test_output", 'conference', CONFERENCE_LIST)
	#filter_by_attr(DATA_PATH + 'AP_after_1996', DATA_PATH+ "AP_after_1996_four_area", 'conference', CONFERENCE_LIST)
	#extract_titles_by_author(DATA_PATH+'AP_after_1996_four_area', DATA_PATH+'JIAWEI_HAN', 'Jiawei Han')
	#extract_titles_by_author(DATA_PATH+'AP_after_1996_four_area', DATA_PATH+'JIAWEI_HAN_TOP', 'Jiawei Han')
	#extract_by_attr(DATA_PATH+'AP_after_1996_four_area', DATA_PATH+'titles_all', 1)

	#indexify(DATA_PATH + 'AP_after_1996_four_area', DATA_PATH + 'AP_after_1996_four_area_index', DATA_PATH+'author_id_name', ['!'])

	'''test extracting titles of different authors'''
	#extract_titles_by_author(DATA_PATH + 'AP_after_1996_four_area_index', DATA_PATH + 'jiawei_han', '961')
	#extract_titles_by_author(DATA_PATH + 'AP_after_1996_four_area_index', DATA_PATH + 'yizhou_sun', '19945')
	#extract_titles_by_author(DATA_PATH + 'AP_after_1996_four_area_index', DATA_PATH + 'jie_tang', '12695')
	#extract_titles_by_author(DATA_PATH + 'AP_after_1996_four_area_index', DATA_PATH + 'xin_dong', '13021')

	'''test chucking titles'''
	#chunck_titles(DATA_PATH + 'toy_dataset', DATA_PATH + 'toy_dataset_output')

	'''output phrase - cnt pairs for a particular author'''
	#generate_author_phrase_rank_list(DATA_PATH + 'jiawei_han', DATA_PATH + 'jiawei_han_stat')
	#generate_author_phrase_rank_list(DATA_PATH + 'jie_tang', DATA_PATH + 'jie_tang_stat')
	#generate_author_phrase_rank_list(DATA_PATH + 'yizhou_sun', DATA_PATH + 'yizhou_sun_stat')
	#generate_author_phrase_rank_list(DATA_PATH + 'xin_dong', DATA_PATH + 'xin_dong_stat')

	'''normalize phrase_cnt files...'''
	#norm_file(DATA_PATH + 'topic_ir.txt', DATA_PATH + 'topic_ir')
	#norm_file(DATA_PATH + 'topic_ir', DATA_PATH + 'topic_ir_norm', False, True)

	'''extract papers for candidate authors'''
	#extract_paper_by_author(
	#	[961, 9413, 2438, 2, 578, 968, 1849, 3214, 19945, 12695, 3861],
	#	DATA_PATH + 'AP_after_1996_four_area_index')
	#filter_by_attr(DATA_PATH + 'AMiner-Paper.txt', DATA_PATH + 'AMiner-Paper-after1996.txt', 'year', 1996)
	indexify(DATA_PATH + 'AMiner-Paper-after1996-23venues.txt', DATA_PATH + 'AMiner-Paper-after1996-23venues-authorid.txt', DATA_PATH+'author_id', [])

if __name__ == '__main__':
	main()