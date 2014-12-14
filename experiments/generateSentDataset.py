__author__ = 'praveen'
from parser.ctgov import ClinicalTrial_Parser as CT_Parser
from textAnnotator.conceptMatching import DictionaryMapping
from textAnnotator.filters import ConceptFilters
from dictionary.umls import UMLSDict
from util.log import strd_logger
from multiprocessing import Process
from util.load import load_stop_words, load_tuis
import textAnnotator.nlpUtil as nlpUtil
import argparse
import pickle
import math
import sys


log = strd_logger('annotate-trials')

def annotate_trials(f_data, outPath, nprocs=1):

    # open the clinical trail ids file to process
    nct_ids = []
    for line in open(f_data + '/trial_ids.txt', 'rb'):
        nct_ids.append(line.strip())
    corpus_path = f_data + '/trials_xml/'

    # Get clinical
    # process each clinical trial and store to XML file
    log.info('processing clinical trials')
    procs = []
    chunksize = int(math.ceil(len(nct_ids) / float(nprocs)))
    for i in xrange(nprocs):
        print chunksize * i, chunksize * (i + 1)
        p = Process(target=_worker, args=(nct_ids[chunksize * i:chunksize * (i + 1)], corpus_path, outPath, (i + 1)))
        procs.append(p)
        p.start()

    for p in procs:
        p.join()





def _worker(process_ids, corpusPath, outPath, pid):
    parser = CT_Parser(corpusPath)

    trials = dict()
    # Iterate over NCT trials
    for i in xrange(0, len(process_ids)):
        trial_ID = process_ids[i]
        trial = parser.parse(trial_ID)

        allTxt = ''
        if trial.ec_text_exc is not None:
            allTxt = trial.ec_text_exc

        if trial.ec_text_inc is not None:
            allTxt +=  '\n' + trial.ec_text_inc

        cleanText = nlpUtil.clean_text(allTxt)
        sentences = nlpUtil.get_sentences(cleanText)
        sentID = 1
        for sent in sentences:

            sent = nlpUtil.pre_process(sent)
            tokens = nlpUtil.get_tokens(sent)
            #posTags = nlpUtil.get_POSTags(tokens)

            # degub = False
            # if debug:
            #     if not sent.startswith(' male or female'):
            #         continue
            #         print '\n', ' '.join(tokens) , '\n'

            out = open(outPath + '/' + str(trial_ID) + '-' +  str(sentID) + '.txt', 'w')
            unicode_str = ' '.join(tokens)
            #print '\n', ' '.join(tokens) , '\n'
            out.write(unicode_str.encode('utf8', 'ignore'))
            sentID += 1

        if i % 1000 == 0:
            log.info(' --- core %d: processed %d documents' % (pid, i))



# Main Function

# processing the command line options
def _process_args():
    parser = argparse.ArgumentParser(description='Download and Process Clinical Trials')

    # ids file
    parser.add_argument('-data_folder', default='/Users/praveen/work/data/ctgov_Sep23/',
                        help='file containing clinical ids to process')

    # output path
    parser.add_argument('-out', default='/Users/praveen/work/output/processed_ctgovSep23/sentDataset',
                        help='part-of-speech admitted tag file (default: None)')

    # number of processors to use
    parser.add_argument('-c', default=5, type=int, help='number of processors (default: 1)')
    return parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    args = _process_args()

    annotate_trials(args.data_folder, args.out, args.c)

    # open the clinical trail ids file to process
    # nct_ids = []
    # for line in open(args.data_folder + '/trial_ids.txt', 'rb'):
    #     nct_ids.append(line.strip())
    # corpus_path = args.data_folder + '/trials_xml/'
    #
    # # Get clinical
    # # process each clinical trial and store to XML file
    # log.info('processing clinical trials')
    # procs = []
    # _worker(nct_ids, corpus_path, args.out, 10)