__author__ = 'praveen'


import collections
import operator
import pickle
import os

# Read problems from problem list
def load_problem_list(filename):
    prob_list = collections.defaultdict(list)
    for line in open(filename):
        txt = line.split(',')[0].strip()
        snomedid = line.split(',')[1].strip().split('|')
        if snomedid.startswith('MGH') or snomedid == '':
            continue
        prob_list[txt] = snomedid
    return prob_list

# Read patient data from problem list
def load_patient_data(filename):
    patient_list = collections.defaultdict(list)
    for line in open(filename):
        p_id = line.split(',')[0].strip()
        prob = line.split(',')[1].strip()
        patient_list[p_id].append(prob)
    return patient_list

# Get score for problem
def build_matrix(patient_list, prob_list, mat):
    for p_id in patient_list:
        p_trial_set = collections.defaultdict(int)
        for prob in patient_list[p_id]:
            snomed_ids = prob_list[prob] # Get snomed ID of the problem

            for snomed_id in snomed_ids:
                # Iterate the trial IDs for each snomed_id
                for trialID in mat[snomed_id]:
                    # keep track of the SNOMED counts for each trial
                    p_trial_set[trialID] += 1

        # Sort trials by number of SNOMED Codes it contains and print them in sorted order
        sorted_trials = sorted(p_trial_set.items(), key=operator.itemgetter(1), reverse=True)
        print str(p_id),
        for trialID in sorted_trials:
            print  ',' + trialID[0], #+ '-' + str(trialID[1]),
        print ''


if __name__ == '__main__':
    prob_list = load_problem_list('tablet.csv')
    patient_list = load_patient_data('patient.csv')
    mat = pickle.load(open('mat.pkl'))
    build_matrix(patient_list, prob_list, mat)
