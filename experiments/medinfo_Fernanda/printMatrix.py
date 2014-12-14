__author__ = 'praveen'



import pickle
import numpy as np
from dictionary.snomed import SNOMEDDict
mat = pickle.load(open('/Users/praveen/work/output/fernanda_medinfo2014/mat.pkl'))
prob_list = pickle.load(open('/Users/praveen/work/output/fernanda_medinfo2014/probList.pkl'))
nct_ids = pickle.load(open('/Users/praveen/work/output/fernanda_medinfo2014/nctids.pkl'))

t_sum = mat.sum(0)
print t_sum
# trialID_indexes = np.argsort(mat.sum(1))

# umls_snomed = SNOMEDDict()
# for i in trialID_indexes:
#     if t_sum[i] == 0:
#         continue
#     snomeds = []
#     snomed_prf = []
#
#     for p_id in np.nditer(np.nonzero(mat[i,])):
#         snomeds.append(prob_list[p_id])
#         snomed_prf.append(umls_snomed.get_prfTerm(prob_list[p_id]))
#
#     print nct_ids[i] + ',' + '|'.join(snomeds) #+ ',' + '|'.join(snomed_prf)
#     #break
