
from textAnnotator.conceptMatching import DictionaryMapping
from textAnnotator.filters import ConceptFilters
from util.load import load_stop_words, load_tuis
from dictionary.umls import UMLSDict
import textAnnotator.nlpUtil as nlpUtil
from os.path import basename
import sys
import argparse

def processFile(file_path, out_path, f_stopwords, f_tui):
    out = open(out_path, 'wb')
    umls = UMLSDict()

    if f_stopwords is not None:
        stopwords = load_stop_words(f_stopwords)
    else:
        stopwords = []
    if f_tui is not None:
        tuis = load_tuis(f_tui)
    else:
        tuis = []

    cleanText = nlpUtil.clean_text(open(file_path).read())
    filters = ConceptFilters(stopwords, tuis)
    mapper = DictionaryMapping(umls, filters)
    sentences = cleanText.split('\n')#nlpUtil.get_sentences(cleanText)

    for sent in sentences:
        # Pre-process sentence
        sent = nlpUtil.pre_process(sent)
        tokens = nlpUtil.get_tokens(sent.lower())
        tags = mapper.process_sent(tokens, [])

        #tags = umls.exact_match(txt)
        if len(tags) == 0:
            #print ' '.join(tokens[0:len(tokens)])
            out.write(sent.strip() + '|' + '' + '|' + '' + '|' + '' + '\n')

        for window in tags:
            for tag in window:
                out.write(sent.strip() + '|' + tag + '|' + umls.get_snomed(tag) + '|' + umls.get_prfTerm(tag) + '\n')
    out.close()




# processing the command line options
def _process_args():
    parser = argparse.ArgumentParser(description='Annotate the given text file line by line')
    # Accepted TUIs
    parser.add_argument('-tui', default='/Users/praveen/work/data/clinical/tuis/tuis.txt',
                        help='stop word directory')
    # stop word file
    parser.add_argument('-stop', default='/Users/praveen/work/data/clinical/stop-words/',
                        help='stop word directory')

    # ids file
    parser.add_argument('-i', default='/Users/praveen/Downloads/problemList.txt',
                        help='Input File Path')

    parser.add_argument('-o', default='/Users/praveen/Downloads/problemList_res.txt',
                        help='Output File Path')
    return parser.parse_args(sys.argv[1:])

if __name__ == '__main__':
    args = _process_args()
    processFile(args.i, args.o, None, None)#args.stop, args.tui)