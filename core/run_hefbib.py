import os

import hefbib.build_hin as bhin
import hefbib.bibrank as bibrank
import hefbib.doc_meta as dmeta
import hefbib.expert_finder as efinder
import utils.file_io as fio

def run_hefbib(input_file, output_file):
	# read data 
	doc_meta_lst = fio.read_data(input_file)
	# Todo: generate topical phrase distribution

	# run ExpertFinder 
	expert_finder = efinder.ExpertFinder(
		K=k,
        docs_meta=docs,
        P=p,
        A=a,
        V=v,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
        dist_phrase=phrase_dist,
        )
	efinder.expert_finding_learning(expert_finder, 200)

	# build HIN
	hin = bhin.HIN()

	# run BibRank
	bibrank = bibrank.BibRank(expert_finder, 1, hin,
								  gamma_da=0.5,gamma_dv=0.5, gamma_dd=0.0,
    							  gamma_ad=1.0, gamma_aa=0.0)

	bibrank.propagte_with_bibrank(bibrank, 250)

	# output results
	fio.write_results(bibrank, output_file)



if __name__ == '__main__':
	run_hefbib()