__author__ = 'praveen'

import redis

class UMLSDict:

    def __init__(self, host='localhost', port=27017):
        self.redis_dict = redis.StrictRedis('localhost')

    def get_tui(self, cui):
        tuis = []
        for t in self.redis_dict.smembers(cui):
            if t.startswith('T'):
                tuis.append(t)
        return tuis

    def get_snomed(self, cui):
        for t in self.redis_dict.smembers(cui):
            if t.startswith('S:'):
                return t.split(':')[1]
        return 'None'


    def get_rxnorm(self, cui):
        for t in self.redis_dict.smembers(cui):
            if t.startswith('R:'):
                return t.split(':')[1]
        return 'None'

    def get_icd9(self, cui):
        for t in self.redis_dict.smembers(cui):
            if t.startswith('I:'):
                return t.split(':')[1]
        return 'None'

    def get_prfTerm(self, cui):
        prfTerm = ''
        for t in self.redis_dict.smembers(cui):
            if not t.startswith('T') and not t.startswith('I:')\
                    and not t.startswith('R:') and not t.startswith('S:'):
                prfTerm = t
                return prfTerm
        return prfTerm

    def exact_match(self, text):
        return list(self.redis_dict.smembers(text))


if __name__ == '__main__':
    umls = UMLSDict()
    redis_dict = redis.StrictRedis('localhost')
    print redis_dict.smembers('C1524119')
    #cuis = set(redis_dict.keys('breast car*'))
    #print cuis
    #c = cuis.pop()
    #print c, cuis.pop()
    print umls.exact_match('C1524119')
    print umls.exact_match('yoga')
    print umls.exact_match('pregnancy')
    print umls.exact_match('breastfeeding')
    #print umls.get_tui('C0678222')
    #from nltk.stem.porter import PorterStemmer
    #stemmer = PorterStemmer()
    #print stemmer.stem("metastases")
    #print umls.exact_match("liver metastases")#protease inhibitors")

