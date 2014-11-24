__author__ = 'praveen'
import numpy as np
from scipy.sparse import coo_matrix
import numpy as np
import pickle
import os





def getStat(cuis, diseases, cui_ctr, disease_ctr, m):

    for t in trials:
        for sent in trials[t].concepts:
            for window in sent:
                for c in window:
                    if not cuis.has_key(c):
                        cuis[c] = cui_ctr
                        cui_ctr += 1

                    # Update Matrix
                    col = []
                    for d in d2t[t]:
                        if not diseases.has_key(d):
                            diseases[d] = disease_ctr
                            disease_ctr += 1
                        col.append(diseases[d])

                    row = [cuis[c]] * len(col)
                    data = [1] * len(col)
                    m = m + coo_matrix((data, (row,col)), shape=m.get_shape())
                    # Total
                    m = m + coo_matrix(([1], ([cuis[c]] ,[0])), shape=m.get_shape())
    return m


if __name__ == '__main__':
    cuis = dict()
    diseases = dict()
    cui_ctr = 1
    disease_ctr = 0
    d2t = pickle.load(open('/Users/praveen/work/data/clinical/disease_trail_mapping/trial2Disease.pkl'))

    m  = coo_matrix((70000,1300))

    baseDir = '/Users/praveen/work/research/ctgov/output/annotated_trials'
    for pFile in os.listdir(baseDir):
        trials = pickle.load(open(baseDir + '/' + pFile))
        m = getStat(cuis, diseases, cui_ctr, disease_ctr, m)
    pickle.dump(cuis, open('/Users/praveen/work/research/ctgov/output/stats/cuis.pkl', 'wb'))
    pickle.dump(diseases, open('/Users/praveen/work/research/ctgov/output/stats/diseases.pkl', 'wb'))
    pickle.dump(m, open('/Users/praveen/work/research/ctgov/output/stats/mat.pkl', 'wb'))