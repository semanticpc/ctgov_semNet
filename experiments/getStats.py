__author__ = 'praveen'


import pickle
import os

def getStat(tot_freq, d_freq, trials, d2t):
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


if __name__ == '__main__':
    tot_freq = dict()
    d_freq = dict()
    d2t = pickle.load(open('/Users/praveen/work/data/clinical/disease_trail_mapping/trial2Disease.pkl'))

    baseDir = '/Users/praveen/work/research/ctgov/output/annotated_trials'
    for pFile in os.listdir(baseDir):
        trials = pickle.load(open(baseDir + '/' + pFile))
        getStat(tot_freq, d_freq, trials, d2t)
    pickle.dump(tot_freq, open('/Users/praveen/work/research/ctgov/output/stats/tot_freq.pkl', 'wb'))
    pickle.dump(d_freq, open('/Users/praveen/work/research/ctgov/output/stats/d_freq.pkl', 'wb'))