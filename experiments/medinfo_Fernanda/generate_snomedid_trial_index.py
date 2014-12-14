__author__ = 'praveen'


import collections
import pickle
import os
from dictionary.umls import UMLSDict

# Get score for problem
def build_matrix(mat, nct_ids, trials):

    umls = UMLSDict()
    for t in trials:
        if not t in nct_ids:
            continue
        snomeds = set()
        for sent in trials[t].concepts:
            for window in sent:
                for c in window:
                    if umls.get_snomed(c) != 'None':
                        snomeds.add(umls.get_snomed(c))
        for id in snomeds:
            mat[id].add(t)
    return mat


if __name__ == '__main__':
    disease_name = 'cervical cancer'
    d2t = pickle.load(open('/Users/praveen/work/data/disease_trail_mapping/disease2Trail.pkl'))
    nct_ids = d2t[disease_name]
    mat = collections.defaultdict(set)
    baseDir = '/Users/praveen/work/output/processed_ctgovSep23/annotated_trials'
    for pFile in os.listdir(baseDir):
        print pFile
        trials = pickle.load(open(baseDir + '/' + pFile))
        mat = build_matrix(mat, nct_ids, trials)
    pickle.dump(mat, open('/Users/praveen/work/output/fernanda_medinfo2014/mat.pkl', 'wb'))
