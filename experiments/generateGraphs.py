__author__ = 'praveen'


import pickle
import numpy
from operator import itemgetter
import matplotlib.pyplot as plt
from util.load import load_tuis
from dictionary.umls import UMLSDict

def loadData(statsPath):
    mat = pickle.load(open(statsPath + '/' + 'mat.pkl'))
    diseases =  pickle.load(open(statsPath + '/' + 'diseases.pkl'))
    cuis = pickle.load(open(statsPath + '/' + 'cuis.pkl'))

    # Sort the diseases and CUIs hash by value (values are indexes in the matrix)
    sorted_cui = sorted(cuis.items(), key=itemgetter(1))
    sorted_d = sorted(diseases.items(), key=itemgetter(1))
    return (mat, sorted_cui, sorted_d, cuis, diseases)

def genGraphData(mat, sorted_d, outPath):
    out = open(outPath, 'wb')
    d2t = pickle.load(open('/Users/praveen/work/data/disease_trail_mapping/disease2Trail.pkl'))
    b_m = mat.sign()
    concept_sum = b_m.sum(0).getA1()
    d_size = concept_sum.nonzero()[0].size
    sorted_disease_count = concept_sum[1:d_size].argsort(0)
    d_freq = []
    for i in range(0, d_size-1):
        #print sorted_d[sorted_disease_count[i]+1][0] , concept_sum[sorted_disease_count[i]+1]
        d_freq.append(concept_sum[sorted_disease_count[i]+1])
        d_name = sorted_d[sorted_disease_count[i]+1]
        out.write(d_name[0] + '|' +  str(concept_sum[sorted_disease_count[i]+1]) + '|' +  str(len(d2t[d_name[0]])) + '\n')


        #d_freq.append(sum())
        #print sorted_d[sorted_disease_count[i]+1][0] , concept_sum[sorted_disease_count[i]+1]
        #d_freq.append(concept_sum[sorted_disease_count[i]+1])

    #line = plt.plot(range(1,len(d_freq)+1), d_freq)
    #plt.show()
    out.close()


def genFreqCUIs(sorted_cui, mat, disease_name=None):
    umls = UMLSDict()
    if disease_name:
        disease_index = diseases[disease_name]
    else:
        disease_index = 0

    sorted_indexes = numpy.argsort(mat.getcol(disease_index).todense(), 0)
    for i in range(1, 10):
        freq =  mat.getcol(disease_index)[sorted_indexes[len(sorted_indexes)-i],]
        cui = sorted_cui[sorted_indexes[len(sorted_indexes)-i]][0]
        if freq[0,0] <= 0:
            break
        print cui + '|' +  umls.get_prfTerm(cui) + '|' +  ','.join(umls.get_tui(cui)) + '|' + str(freq[0,0])



def genSemanticTypeData(sorted_cui, mat, disease_name=None):
    acc_tuis = load_tuis('/Users/praveen/work/data/tuis/tuis.txt')
    umls = UMLSDict()
    if disease_name:
        disease_index = diseases[disease_name]
    else:
        disease_index = 0

    sorted_indexes = numpy.argsort(mat.getcol(disease_index).todense(), 0)
    freqs = mat.getcol(disease_index).todense()

    tui = dict()
    tot = 0
    for i in range(1, mat.get_shape()[0]):
        cui = sorted_cui[sorted_indexes[len(sorted_indexes)-i]][0]
        freq =  freqs[sorted_indexes[len(sorted_indexes)-i],]

        if freq[0,0] <= 0:
            break
        tot += freq.item(0)
        for t in umls.get_tui(cui):
            tui.setdefault(t, 0)
            tui[t] += freq.item(0)
    s = 0
    for t in tui:
        if t not in acc_tuis:
            continue
        print t, tui[t], (tui[t]/tot) * 100
        s += (tui[t]/tot) * 100
    print s



statsPath = '/Users/praveen/work/output/processed_ctgovSep23/stats'
#d2t = pickle.load(open('/Users/praveen/work/data/disease_trail_mapping/disease2Trail.pkl'))
#print d2t.keys()
(mat, sorted_cui, sorted_d, cuis, diseases) = loadData(statsPath)
#genGraphData(mat, sorted_d, '/Users/praveen/work/output/graphs_disease_stat_uniq.data')
#genFreqCUIs(sorted_cui, mat)



genSemanticTypeData(sorted_cui, mat, 'cervical cancer')