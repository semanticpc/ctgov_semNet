__author__ = 'praveen'


class DataElement(object):
    def __init__(self):
        pass

    def getCUI(self):
        pass

    def setCUI(self):
        pass

    def getFreq(self,freq, year=None):
        pass

    def setFreq(self, freq, year):
        pass

    def updateFreq(self, freq, year):
        pass

    def setTUI(self, tui):
        pass

    def getTUI(self):
        pass

    def getSemanticCat(self, semCat):
        pass

    def setSemanticCat(self):
        pass

    # Multiple Relations

    def addRelation(self, rel_type):
        pass

    def getRelations(self):
        pass

    def addSentenceID(self):
        pass

    def getSentenceList(self):
        pass

    def addTrialID(self):
        pass

    def getTrialID(self):
        pass


