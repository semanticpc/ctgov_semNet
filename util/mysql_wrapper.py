__author__ = 'praveen'

def add_trial(cur, trial, allTxt):
    sql = """INSERT INTO Trials (TrialID, Study_Type, Title, Start_Date, First_Verified_Date, Verification_Date, Last_Changed_Date, Completion_Date, EC_Gender, EC_Min_Age, EC_Max_Age, EC_Raw_Text)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    data = (trial.trialsID, trial.study_type, trial.title, trial.start_date, trial.firstreceived_date, trial.verification_date, trial.lastchanged_date, trial.completion_date, trial.ec_gender, trial.ec_min_age, trial.ec_max_age, allTxt)
    cur.execute(sql, data)

def add_sentence(cur, sentID, trialID, sent_text, type):
    sql = """INSERT INTO Sentence (SentenceID, TrialID, Sent_Text, Type)  VALUES (%s, %s, %s, %s)"""
    data = (sentID, trialID, sent_text, type)
    cur.execute(sql, data)

def add_concepts(cur, cui, concept_text, sentID, trialID):
    sql = """INSERT INTO Concepts (CUI, Concept_Text, SentID, TrialID)  VALUES (%s, %s, %s, %s)"""
    data = (cui, concept_text, sentID, trialID)
    cur.execute(sql, data)