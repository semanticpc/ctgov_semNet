__author__ = 'praveen'

# load stop words
def load_stop_words(dstop):
    if dstop is None:
        return None

    # Add English Stopwords
    fid = open(dstop+'/english.csv', 'r')
    eng = set()
    for line in fid:
        if len(line) > 0:
            eng.add(line.strip())
    fid.close()
    if not eng:
        eng = set()

    # Add Medical Stopwords
    fid = open(dstop+'/medical.csv', 'r')
    med = set()
    for line in fid:
        if len(line) > 0:
            med.add(line.strip())
    fid.close()
    if not med:
        med = set()
    pmed = set()
    for m in med:
        pmed.add(m + 's')
    med |= pmed
    stop = (eng, med)
    return stop


# load part-of-speech tags
def load_tuis(tui_file):
    # Add English Stopwords
    fid = open(tui_file, 'r')
    tuis = set()
    for line in fid:
        if len(line) > 0:
            tuis.add(line.strip())
    fid.close()
    if not tuis:
        tuis = set()

    return tuis

# load trial ID disease mapping
def load_disease_nctid(mapping_file):
    pass