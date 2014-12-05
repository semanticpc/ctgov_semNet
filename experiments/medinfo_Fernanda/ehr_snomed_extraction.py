__author__ = 'praveen'

import collections
import operator
import pickle
import os
from dictionary.snomed import SNOMEDDict
from dictionary.umls import UMLSDict
from textAnnotator.conceptMatching import DictionaryMapping
from textAnnotator.filters import ConceptFilters
import textAnnotator.nlpUtil as nlpUtil
from itertools import chain

# Read problems from problem list
def load_problem_list(filename):
    prob_list = []
    for line in open(filename):
        txt = line.split(',')[0].strip()
        prob_list.append(txt)
    return prob_list

def getSNOMEDID(prob_list, outPath):
    umls = UMLSDict()
    filters = ConceptFilters([], [])
    mapper = DictionaryMapping(umls, filters)
    out = open(outPath, 'wb')
    for prob in prob_list:
        # pre-process
        cleanText = nlpUtil.clean_text(prob)
        sent = nlpUtil.pre_process(cleanText)
        tokens = nlpUtil.get_tokens(sent.lower())
        tags = mapper.process_sent(tokens, [])
        snomed = []
        for tag in  list(chain.from_iterable(tags)):
            if umls.get_snomed(tag[0]) != 'None':
                snomed.append(umls.get_snomed(tag[0]))
        out.write(prob + ',' + '|'.join(snomed) + '\n')
    out.close()



if __name__ == '__main__':
    prob_list = load_problem_list('/Users/praveen/work/output/fernanda_medinfo2014/problemList/ehr.csv')
    outPath = '/Users/praveen/work/output/fernanda_medinfo2014/problemList/ehr_auto.csv'
    getSNOMEDID(prob_list, outPath)