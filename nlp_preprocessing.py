import nltk

'''
    usage:
    text = "Heterogeneous source consensus learning via decision propagation and negotiation."
    phrases = NPChuncker.parse_sentence(text)
    for phrase in phrases:
        print phrase
'''

lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()
stopwords = nltk.corpus.stopwords.words('english')

def normalize_word(word, do_stem=True, do_lemmatize=True):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    if do_stem:
        word = stemmer.stem_word(word)
    if do_lemmatize:
        word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word, min_len=2, max_len=40):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(min_len <= len(word) <= max_len
        and word.lower() not in stopwords)
    return accepted


class NPChuncker(object):
    grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
        {<NNP>+}
        {<NN>+}
    """
    chunker = nltk.RegexpParser(grammar)

    @staticmethod
    def parse_corpus(corpus):
        sentences = nltk.sent_tokenize(corpus)
        for sent in sentences:
            NLTK_Chuncker.parse_sentence(sent)

    @staticmethod
    def parse_sentence(sentence):
        tokens = nltk.word_tokenize(sentence)
        pos_tokens = nltk.tag.pos_tag(tokens)
        tree = NPChuncker.chunker.parse(pos_tokens)
        return NPChuncker._get_phrases(tree)
 
    @staticmethod
    def _get_phrases(tree):
        for leaf in NPChuncker._get_leaves(tree):
            phrase = [normalize_word(w) for w, t in leaf if acceptable_word(w)]
            yield phrase

    @staticmethod
    def _get_leaves(tree):
        """Finds NP (nounphrase) leaf nodes of a chunk tree."""
        for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
            yield subtree.leaves()
