#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Uses the vectorizers and models to classify and
categorize data.

Created on 
@author: Lucia Liu (lucia.liu@utp.ac.pa)
"""

import Preprocessing
import pickle

# load  vectorizers
with open('./models/vectorizer3000', 'rb') as vect1:
    vectorizer3 = pickle.load(vect1)
with open('./models/vectorizer10000', 'rb') as vect2:
    vectorizer10 = pickle.load(vect2)
# load models
with open('./models/xgb_10000', 'rb') as training_model:
    xgb_classifier = pickle.load(training_model)
with open('./models/mo_3000', 'rb') as training_model:
    mo_classifier = pickle.load(training_model)

# asdf
def get_classifications(dataframe, column):
    """Receives dataframe with text and returns dataframe with
    classificacion and categorization data.

    Args:
        dataframe (Pandas.DataFrame): Table with tweets data.
        column (string): Name of column with tweet text.

    Returns:
        Pandas.DataFrame: Returns dataframe with classification
        and categorization.
    """
    # copies dataframe
    df = dataframe.copy()
    # cleans data
    df = Preprocessing.clean_text(df, 'text')
    ## vectorizes data
    vect_data3 = vectorizer3.transform(df[column])
    vect_data10 = vectorizer10.transform(df[column])
    ## classifies and categorizes data
    df.loc[:,'isIncident'] = xgb_classifier.predict(vect_data10)
    df.loc[:,['isAccident','isObstacle','isDanger']] = mo_classifier.predict(vect_data3)
    # returns result dataframe
    return df

def get_classification(text):
    """Receives text, classifies and categorizes the data.

    Args:
        text (string): Tweet text.

    Returns:
        dict: Dictionary with classification and
        categorization data.
    """
    # clean text
    txt = Preprocessing.preprocess(text)
    results = {} # creates a dictionary
    # vectorize data
    vect_data3 = vectorizer3.transform([txt])
    vect_data10 = vectorizer10.transform([txt])
    ## classifies and categorizes data
    results['isIncident'] = xgb_classifier.predict(vect_data10)[0]
    names = ['isAccident','isObstacle','isDanger']
    values = mo_classifier.predict(vect_data3)[0]
    # adds dictionary like list values
    for name, value in zip(names, values):
        results[name] = value
    return results