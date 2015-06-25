import numpy as np
from scipy.sparse import csr_matrix

'''test = csr_matrix([[0,400,300],[100,0,0],[0,0,200]])
print test
print '\n'
print test.data
print '\n'
print test.indices
print '\n'
print test.indptr'''


'''test = np.array([0.03388814, 0.05621686, 0.13096799, 0.10606396,  0.00401314,  0.0111855, 0.15701421,  0.21770816,  0.10638193,  0.1765601 ])
norm = np.linalg.norm(test)
norm_test = test/norm'''



'''docs = [["hello", "world", "hello"], ["goodbye", "cruel", "world"]]
indptr = [0]
indices = []
data = []
vocabulary = {}
for d in docs:
     for term in d:
         index = vocabulary.setdefault(term, len(vocabulary))
         indices.append(index)
         data.append(1)
     indptr.append(len(indices))

print vocabulary
print data
print indices
print indptr
print csr_matrix((data, indices, indptr), dtype=int).toarray()'''

'''docs_authors = [[1,2],[0,2,3]]
indptr = [0]
indices = []
data = []
for doc_authors in docs_authors:
    for author in doc_authors:
        indices.append(author)
        data.append(1)
    indptr.append(len(indices))

tt = csr_matrix((data, indices, indptr), dtype=int)
print tt
print tt.toarray()'''

x,y,z = [0], [0], [0]
print x,y,z