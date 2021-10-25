#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Uses the vectorizers and models to classify, categorize and geolocate data.

Created on 
@author: Lucia Liu (lucia.liu@utp.ac.pa)
"""

import Preprocessing
import pickle

# load  vectorizers
with open('./models/vectorizer3000', 'rb') as vect1:
    vectorizer3 = pickle.load(vect1)
# load models
with open('./models/rf_est3000', 'rb') as training_model:
    rf_classifier = pickle.load(training_model)
with open('./models/mo_1600_est_3000', 'rb') as training_model:
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
    ## classifies and categorizes data
    df.loc[:,'isIncident'] = rf_classifier.predict(vect_data3)
    df.loc[:, 'prob'] = rf_classifier.predict_proba(vect_data3)[:, 1]
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
    ## classifies and categorizes data
    results['isIncident'] = rf_classifier.predict(vect_data3)[0]
    names = ['isAccident','isObstacle','isDanger']
    values = mo_classifier.predict(vect_data3)[0]
    # adds dictionary like list values
    for name, value in zip(names, values):
        results[name] = value
    return results