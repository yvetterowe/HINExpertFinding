make
sed -e "s/’/'/g" -e "s/′/'/g" -e "s/''/ /g" < latest_raw_corpus | tr -c "A-Za-z'_ \n" " " > latest_raw_corpus-norm0
time ./word2phrase -train latest_raw_corpus-norm0 -output latest_raw_corpus-norm0-bigram -threshold 100 -debug 2
time ./word2phrase -train latest_raw_corpus-norm0-bigram -output latest_raw_corpus-norm0-trigram -threshold 100 -debug 2
tr A-Z a-z < latest_raw_corpus-norm0-trigram > latest_raw_corpus-norm1-trigram
time ./word2vec -train latest_raw_corpus-norm1-trigram -output latest_raw_corpus-vectors-phrase2.bin -cbow 1 -size 200 -window 10 -negative 25 -hs 0 -sample 1e-5 -threads 20 -binary 0 -iter 15
./distance latest_raw_corpus-vectors-phrase1.bin