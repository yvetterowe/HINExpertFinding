def get_vocabulary(input_file, output_file):
	with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
		data = fin.read().split('\n')
		for data_point in data:
			word = data_point.split()[0]
			fout.write("{word}\n".format(word=word))


if __name__ == "__main__":
	get_vocabulary('latest_raw_corpus-vectors-phrase2.bin', 'sorted_vocab')