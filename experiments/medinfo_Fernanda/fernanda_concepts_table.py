__author__ = 'praveen'

import pickle
from dictionary.umls import UMLSDict
import os
def generate_table(nctids, umls, annotated_trials_path, output_path):

    out = open(output_path, 'w')
    for trialID in nctids:
        if not os.path.exists(annotated_trials_path + '/' + trialID):
            continue
        infile = open(annotated_trials_path + '/' + trialID)
        for line in infile:
            cols = line.split('|')
            trialID = cols[0].strip()
            text = cols[1].strip()
            cui = cols[2].strip()
            prfTerm = umls.get_prfTerm(cui)
            tuis = ','.join(umls.get_tui(cui))
            snomed = umls.get_snomed(cui)
            out.write(trialID + '|' + text + '|' + cui + '|' + snomed + '|' + prfTerm + '|' + tuis + '\n' )

    out.close()

if __name__ == '__main__':
    d2t = pickle.load(open('/Users/praveen/work/data/disease_trail_mapping/disease2Trail.pkl'))
    umls = UMLSDict()

    data_path = '/Users/praveen/work/output/processed_ctgovSep23/annotated_trials_txt'
    base_outpath = '/Users/praveen/work/output/fernanda_medinfo2014'
    generate_table(d2t['breast cancer'], umls, data_path, base_outpath + '/' + 'breast_cancer.txt')
    generate_table(d2t['ovarian cancer'], umls, data_path, base_outpath + '/' + 'ovarian_cancer.txt')
    generate_table(d2t['cervical cancer'], umls, data_path, base_outpath + '/' + 'cervical_cancer.txt')
