from textAnnotator.conceptMatching import DictionaryMapping
from dictionary.umls import UMLSDict
import textAnnotator.nlpUtil as nlpUtil
from os.path import basename
import string

def processFolder(folder_path, out_path):
    pass

def processFile(file_path, out_path):
    out = open(out_path + '/' + basename(file_path) + '.otxt', 'wb')
    umls = UMLSDict()
    #mapping = DictionaryMapping(umls)
    to_remove = string.punctuation.replace('-', '')
    table = string.maketrans(to_remove," " * len(to_remove))

    window_size = 5
    cleanText = nlpUtil.clean_text(open(file_path).read())
    sentences = nlpUtil.get_sentences(cleanText)
    print len(sentences)
    c = 0
    for sent in sentences:
        # Print Sentence


        # Pre-process sentence
        #sent = nlpUtil.clean_text(sent)

        sent = str(sent).translate(table)
        tokens = []
        tokens = nlpUtil.get_tokens(sent.lower())
        txt = ' '.join(tokens[0:len(tokens)-1])

        out.write(txt + '\n')

        tags = umls.exact_match(txt)
        if len(tags) == 0:
            print ' '.join(tokens[0:len(tokens)-1])
            #break


        #print tags
        for tag in tags:
            c += 1
            out.write(tag + ':'  + umls.get_prfTerm(tag) + '\n')
    print c
    out.close()




processFile('/Users/praveen/Downloads/fernanda_oldImpl/ovarian_cancer.txt', '/Users/praveen/Downloads/fernanda_oldImpl/')