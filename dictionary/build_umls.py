__author__ = 'praveen'


from multiprocessing import Process, Manager
from textAnnotator.nlpUtil import get_tokens
from util.log import strd_logger
import redis
import itertools
import string

log = strd_logger('umls-dict-builder')

def filterCUI(in_queue, redis_dict):
    to_remove = string.punctuation.replace('-', '')
    table = string.maketrans(to_remove," " * len(to_remove))
    while True:
        item = in_queue.get()
        line_no, line = item

        # exit signal
        if line == None:
            return
        rows = line.split('|')
        prefText = False
        if rows[1] == 'ENG' and rows[16] == 'N':
            cui = rows[0]

            # Remove puncuation
            text = rows[14].translate(table)

            # Obtain tokens
            text = get_tokens(text.lower())

            if rows[2] == 'P' and rows[6] == 'Y':
                redis_dict.sadd(cui, ' '.join(text))
            #src = rows[11]
            redis_dict.sadd(' '.join(text), cui)

        if (line_no % 10000) == 0:
            log.info('Processed %d lines' % (line_no))


def getTUI(in_queue, redis_dict):
    while True:
        item = in_queue.get()
        line_no, line = item

        # exit signal
        if line == None:
            return
        rows = line.split('|')
        cui = rows[0]
        tui = rows[1]

        redis_dict.sadd(cui, tui)

        if (line_no % 10000) == 0:
            log.info('Processed %d lines' % (line_no))

def build_CUI_db(umls_path, tui_map=False):
    if tui_map:
        umls_path = umls_path + '/MRSTY.RRF'
    else:
        umls_path = umls_path + '/MRCONSO.RRF'
    num_workers = 10
    redis_dict = redis.StrictRedis('localhost')
    manager = Manager()
    results = manager.list()
    work = manager.Queue(num_workers)

    # start for workers
    pool = []
    for i in xrange(num_workers):
        if tui_map:
            p = Process(target=getTUI, args=(work, redis_dict))
        else:
            p = Process(target=filterCUI, args=(work, redis_dict))
        p.start()
        pool.append(p)

    # produce data
    with open(umls_path) as f:
        iters = itertools.chain(f, (None,)*num_workers)
        for num_and_line in enumerate(iters):
            work.put(num_and_line)

    for p in pool:
        p.join()

    print len(set(redis_dict.keys('C*')))

if __name__ == "__main__":
    #umls_path = "/Users/praveen/Downloads/"
    umls_path = "/Users/praveen/Downloads/umls/2014AA/META/"
    redis_dict = redis.StrictRedis('localhost')
    redis_dict.flushall()

    build_CUI_db(umls_path, tui_map=False)
    build_CUI_db(umls_path, tui_map=True)





# def writeToRedis(results, host='localhost', port=27017):
#     client = MongoClient(host, port)
#     db = client.umls
#     collection = db.all_eng
#
#     cnt = 0
#
#     for l in results:
#         cui = l[0]
#         txt = l[2]
#         isPrfTxt = l[1]
#
#         item = collection.find_one( {"_id": cui})
#         if item:
#             lvalue  = list([txt]) if not item else list(item['txt']) + list([txt])
#             collection.update( {"_id":cui},{'$set':{'txt': lvalue}},upsert=True, multi=False)
#             if isPrfTxt:
#                 collection.update( {"_id":cui},{'$set':{'pref': txt}},upsert=True, multi=False)
#         else:
#             if isPrfTxt:
#                 doc = {'_id': cui, 'cui': cui, 'pref': txt, 'txt':[txt]}
#             else:
#                 doc = {'_id': cui, 'cui': cui, 'txt':[txt]}
#             collection.insert(doc)
#         cnt += 1
#         if (cnt % 10000) == 0:
#             log.info('Added %d strings' % (cnt))