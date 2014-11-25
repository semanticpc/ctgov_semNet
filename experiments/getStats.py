__author__ = 'praveen'
import numpy as np
from scipy.sparse import coo_matrix
import numpy as np
import pickle
import os





def getStat(tot_freq, d_freq ):

    for t in trials:
        for sent in trials[t].concepts:
            for window in sent:
                for c in window:
                    tot_freq.setdefault(c, 0)
                    tot_freq[c] += 1
                    for d in d2t[t]:
                        d_freq.setdefault(c, dict())
                        d_freq[c].setdefault(d, 0)
                        d_freq[c][d] += 1

def getMatrix(tot_freq, d_freq):
    cui_ctr = 0
    disease_ctr = 0
    m  = coo_matrix((len(tot_freq),1300))
    diseases = dict()
    cuis = dict()

    for c in tot_freq:
        if not cuis.has_key(c):
            cuis[c] = cui_ctr
            cui_ctr += 1
        data = [tot_freq[c]]
        col = [0]
        if d_freq.has_key(c):
            for d in d_freq[c]:
                if not diseases.has_key(d):
                    diseases[d] = disease_ctr
                    disease_ctr += 1
                col.append(diseases[d])
                data.append(d_freq[c][d])

        row = [cuis[c]] * len(col)
        m = m + coo_matrix((data, (row,col)), shape=m.get_shape())
    return m

if __name__ == '__main__':
    tot_freq = dict()
    d_freq = dict()
    #m = m + coo_matrix((data, (row,col)), shape=(70000,1300))
    d2t = pickle.load(open('/Users/praveen/work/data/clinical/disease_trail_mapping/trial2Disease.pkl'))


    print 'start'

    baseDir = '/Users/praveen/work/research/ctgov/output/annotated_trials'
    for pFile in os.listdir(baseDir):
        trials = pickle.load(open(baseDir + '/' + pFile))
        getStat(tot_freq, d_freq)#, cui_ctr, disease_ctr)
    print 'done'
    print 'start'
    m = getMatrix(tot_freq, d_freq)
    print 'done'
    pickle.dump(tot_freq, open('/Users/praveen/work/research/ctgov/output/stats/tot_freq.pkl', 'wb'))
    pickle.dump(d_freq, open('/Users/praveen/work/research/ctgov/output/stats/d_freq.pkl', 'wb'))
    pickle.dump(m, open('/Users/praveen/work/research/ctgov/output/stats/mat.pkl', 'wb'))