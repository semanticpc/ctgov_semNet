__author__ = 'praveen'

class Trial(object):
    def __init__(self, trialID):
        self.trialsID = trialID
        self.title = None
        self.study_type = None
        self.conditions = []
        self.start_date = None
        self.firstreceived_date = None
        self.verification_date = None
        self.lastchanged_date = None
        self.completion_date = None
        self.ec_gender = None
        self.ec_min_age = None
        self.ec_max_age = None
        self.ec_text_inc = None
        self.ec_text_exc = None

        # Information Extraction from EC Text

        # Three levels of nestings
        #   - Sentence
        #       - nGram
        #           - CUI
        self.concepts = []
        self.diseases = []

    def getEC_text(self):
        pass

    def getCDEs(self):
        pass

    def addCDE(self):
        pass

    def setDisease(self):
        pass

    def getDisease(self):
        pass