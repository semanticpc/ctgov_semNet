__author__ = 'praveen'
import collections
import operator
import pickle
import os

# Read problems from problem list
def load_problem_list(filename):
    prob_list = collections.defaultdict()
    for line in open(filename):
        txt = line.split(',')[0].strip()
        snomedid = line.split(',')[1].strip()
        if snomedid.startswith('MGH') or snomedid == '':
            continue
        prob_list[txt] = snomedid
    return prob_list


def runIndriQuery(prob, snomed_id):
    index_loc = '/Users/praveen/work/output/fernanda_medinfo2014/diseaseData_index/breast_cancer'
    query = '\'%s\'' % (prob)
    docCount = 5000
    cmd = 'IndriRunQuery -index=%s -query=%s -count=%s -trecFormat' % (index_loc,  query, docCount)
    print cmd

# Get score for problem
def build_matrix(prob_list):
    score_mat = collections.defaultdict(dict)
    for prob in prob_list:
        snomed_id = prob_list[prob] # Get snomed ID of the problem

        vec = runIndriQuery(prob, snomed_id)
        score_mat[prob] = vec

if __name__ == '__main__':
    prob_list = load_problem_list('/Users/praveen/work/output/fernanda_medinfo2014/problemList/tablet.csv')

    build_matrix(prob_list)
