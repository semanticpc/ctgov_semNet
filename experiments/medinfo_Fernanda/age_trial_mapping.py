__author__ = 'praveen'


import collections
import pickle
import os
from dictionary.umls import UMLSDict

# Get score for problem
def build_age_matrix(age_map, nct_ids, trials):
    for t in trials:
        if not t in nct_ids:
            continue
        age_map[t] = (trials[t].ec_min_age,trials[t].ec_max_age)
    return age_map


if __name__ == '__main__':
    disease_name = 'ovarian cancer'
    d2t = pickle.load(open('/Users/praveen/work/data/disease_trail_mapping/disease2Trail.pkl'))
    nct_ids = d2t[disease_name]
    age_map = dict()
    baseDir = '/Users/praveen/work/output/processed_ctgovSep23/annotated_trials'
    for pFile in os.listdir(baseDir):
        print pFile
        trials = pickle.load(open(baseDir + '/' + pFile))
        build_age_matrix(age_map, nct_ids, trials)

    out = open('/Users/praveen/work/output/fernanda_medinfo2014/age/ovarian_cancer.txt', 'wb')
    for age in age_map:
        out.write('%s, %s, %s\n' % (age, age_map[age][0], age_map[age][1]))
    out.close()
    #pickle.dump(mat, open('/Users/praveen/work/output/fernanda_medinfo2014/age/age_mat.pkl', 'wb'))
