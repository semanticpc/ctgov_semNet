__author__ = 'praveen'
import itertools
from util.log import strd_logger

log = strd_logger('dict-mapping')


class DictionaryMapping(object):
    def __init__(self, umls, filters, ngram=5):
        self.use_scramble_find = True
        self.use_split_dashed_words = True
        self.conj = {'and', 'or'}
        self.umls = umls
        self.ngram = ngram
        self.filters = filters

    def process_sent(self, sent_tokens, sent_pos):
        sent_ptxt = []
        i = 0
        while i <  len(sent_tokens):
            for j in xrange(min(len(sent_tokens), i + self.ngram), i, -1):
                toks = sent_tokens[i:j]
                toks_pos = sent_pos[i:j]

                # Apply the pre-filters
                if not self.filters.accpet_string(toks, toks_pos):
                    continue

                # Dictionary Mapping
                tags = self.map(toks)
                if len(tags) > 0:
                    ntags = []

                    # Filter Semantic Types
                    for tag in tags:
                        for tui in self.umls.get_tui(tag[0]):
                            if self.filters.TUI_filter(tui):
                                ntags.append(tag)
                                break

                    # Add to extracted concepts
                    if len(ntags) > 0: sent_ptxt.append(ntags)

                    # Update window
                    i = j - 1
                    break
            i += 1
        return sent_ptxt

    def map(self, tokens):
        if not self.umls:
            log.warning('UMLS not loaded')
            return []

        # First do direct mapping
        tags = self._direct_mapping(tokens)

        # If simple direct mapping fails, try other options
        #if tags is None and self.use_scramble_find:
            #tags = self._scramble_find(tokens)

        # If scrambling fails, look for dashed words
        #if tags is None and self.use_split_dashed_words:
            #tags = self._split_dashed_words(tokens)


        if tags is None:
            return []
        else:
            return tags

    def _direct_mapping(self, tokens):
        w = ' '.join(tokens).strip()
        hit = self.umls.exact_match(w)
        #print w
        if hit is None or len(hit) == 0 or len(tokens) > self.ngram:
            return None
        else:
            hits = []
            for h in hit:
                hits.append((h, w))
            return hits



    def _scramble_find(self, string):
        if (len(string) > 1) and (len(self.conj & set(string)) > 0):
            stag = set()
            comb = set(itertools.permutations(string))
            for c in comb:
                if len(c) == 1:
                    continue
                t = self._direct_mapping(c)
                if t is not None:
                    if type(t) is list:
                        for i in range(0, len(t)):
                            stag.add(t[i])
                    else:
                        stag.add(t)
            return list(stag)
        else:
            return None

    def _split_dashed_words(self, tokens):
        if len(tokens) > 1:
            return None

        tkn = ' '.join(tokens[0].split('-'))

        local_tags = []
        mt = self._direct_mapping([tkn])
        if mt is not None:
            local_tags += mt
        else:
            if len(tkn) > 1:
                for t in tkn:
                    if len(t) == 0:
                        continue
                    mt = self._direct_mapping([t])
                    if mt is not None:
                        local_tags += mt

        if len(local_tags) != 0:
            return local_tags
        else:
            return None

    # Private Methods
    def _acronym_greedy(self, dpt, tokens):
        tkn = dpt.split()
        if len(tkn) == len(tokens):
            init = set(tokens)
            acr = len(tkn)
            for t in tkn:
                if t[0] in init:
                    acr -= 1
            if acr == 0:
                return dpt
        else:
            return None