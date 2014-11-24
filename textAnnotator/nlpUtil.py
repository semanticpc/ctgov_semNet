__author__ = 'praveen'

import nltk
import string
from util.log import strd_logger
# Extract sentences from the given text
log = strd_logger('nlpUtil')

def clean_text(text):
    """
    Clean the text and takes care of encoding issues

     copied from django's force_text function
    """
    encoding = 'utf-8'
    errors = 'strict'
    # Handle the common case first for performance reasons.
    if isinstance(text, unicode):
        return text
    try:
        if not isinstance(text, basestring):
            if hasattr(text, '__unicode__'):
                text = unicode(text)
            else:
                text = unicode(bytes(text), encoding, errors)
        else:
            # Note: We use .decode() here, instead of six.text_type(s, encoding,
            # errors), so that if s is a SafeBytes, it ends up being a
            # SafeText at the end.
            text = text.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(text, Exception):
            raise Exception(text, *e.args)
        else:
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            text = ' '.join([clean_text(arg) for arg in text])
    return text


def pre_process(text):

    to_remove = string.punctuation.replace('-', '')
    table = string.maketrans(to_remove," " * len(to_remove))
    try:
        sent = str(text).translate(table)
    except UnicodeEncodeError:
        return text
    return sent

def get_sentences(text):
    sent = []
    for s in text.split('\n'):
        s= s.replace('- ', ' - ').replace(' -', ' - ')
        for b in s.split(' - '):
            sent += nltk.tokenize.sent_tokenize(b)
    return sent

def get_tokens(sent):
    return nltk.tokenize.word_tokenize(sent)

def get_POSTags(tokens):
    pos = [t[1] for t in nltk.pos_tag(tokens)]
    if len(tokens) != len(pos):
        log.error('Length of POS tags not equal to length of words ')
    return pos

def get_chunks(tokens, pos, type='ngram'):
    pass