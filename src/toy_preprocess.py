import os.path
import random

def generate_samples(lower, upper, candidates):
	num_sample = random.randint(lower, upper)
	return random.sample(candidates, num_sample)

"""
	generate [lower, uppder] number of phrase from 
	important_phrases and unimportant_phrases
	repectively
"""
def generate_phrase_list_sample(
	important_phrases, l1, u1,
	unimportant_phrases, l2, u2):
    important_samples = generate_samples(l1, u1, important_phrases)
    unimportant_samples = generate_samples(l2, u2, unimportant_phrases)
    return important_samples + unimportant_samples

#topic1
important_phrases = [4357, 1888, 9464, 2360, 3901, 1575, 10198, 3518, 17420, 143, 14765, 2951]
unimportant_phrases = [1745, 3506, 678, 383, 333, 270, 253]

#topic2
#important_phrases = [678, 440, 1848, 4001, 3367, 22881, 1191, 10284, 4531, 482, 6075, 15420, 2000, 3613, 17366]
#unimportant_phraes = [13, 22, 23, 83, 97, 115, 1448]

sample = generate_phrase_list_sample(
	important_phrases, 5, 12,
	unimportant_phrases, 1, 4)
print ' '.join(str(s) for s in sample)