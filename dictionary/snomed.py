__author__ = 'praveen'

import redis

class SNOMEDDict:

    def __init__(self, host='localhost', port=27017):
        self.redis_dict = redis.StrictRedis('localhost', port=6380)

    def get_tui(self, id):
        tuis = []
        for t in self.redis_dict.smembers(id):
            if t.startswith('T'):
                tuis.append(t)
        return tuis

    def get_cui(self, id):
        cui = ''
        for t in self.redis_dict.smembers(id):
            if t.startswith('C'):
                cui = t
                return cui
        return cui

    def get_prfTerm(self, id):
        prfTerm = ''
        for t in self.redis_dict.smembers(id):
            if not t.startswith('C'):
                prfTerm = t
                return prfTerm
        return prfTerm

    def exact_match(self, text):
        return list(self.redis_dict.smembers(text))


if __name__ == '__main__':
    d = SNOMEDDict()

    print d.get_prfTerm('289908002')
    print d.get_cui('289908002')
    print d.exact_match('yoga')
    print d.exact_match('pregnancy')
    print d.exact_match('breastfeeding')

