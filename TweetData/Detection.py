#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Uses the vectorizers and models to classify, categorize and geolocate data.

Created on 
@author: Lucia Liu (lucia.liu@utp.ac.pa)
"""


from fuzzywuzzy import fuzz, process
import Preprocessing
import pickle

# load  vectorizers
with open('./models/vectorizer_1200', 'rb') as vect1:
    vectorizer3 = pickle.load(vect1)
# load models
with open('./models/rf_model', 'rb') as training_model:
    rf_classifier = pickle.load(training_model)
with open('./models/mo_model', 'rb') as training_model:
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
    results['clean_text'] = txt
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

def get_geo(text, places_list, roads_list):
    """Receives text and assigns geolocation with possible road and place name data.

    Args:
        text (string): Tweet text.

    Returns:
        dict: Dictionary with road and place data.
    """

    geo = {'tweet':text, 'place':None, 'road':None}
    intweet = []; possible = []

    ## Iteration of the places in the database
    for index_place, place in places_list.iterrows():
        if len(place['name'])>5:
            if place['name'] in text:
                # Insert the ratio and place ID
                intweet.append([fuzz.token_sort_ratio(place['name'], text), place['osm_id']])
            elif (fuzz.token_set_ratio(place['name'], text)==100 
                and fuzz.token_sort_ratio(place['name'], text)>50) or (fuzz.token_set_ratio(place['name'], text)>90):
                possible.append([fuzz.token_sort_ratio(place['name'], text), place['osm_id']])
    if len(intweet)>0:
        #tweets.loc[index, 'contains_place'] = max(intweet)[1]
        geo['place'] = max(intweet)[1]
    elif len(possible)>0:
        # tweets.loc[index, 'possible_place'] = max(possible)[1] # np.array(possible)
        geo['place'] = max(possible)[1]

    ## Same process with roads
    intweet = []; possible = []
    ## Iteration of roads
    for index_road, road in roads_list.iterrows():
        if len(road['nombre'])>5:
            if road['nombre'] in text:
                # Insert the ratio and road ID
                intweet.append([fuzz.token_sort_ratio(road['nombre'], text), road['gid']])
            elif (fuzz.token_set_ratio(road['nombre'], text)==100 
                and fuzz.token_sort_ratio(road['nombre'], text)>50) or (fuzz.token_set_ratio(road['nombre'], text)>90):
                possible.append([fuzz.token_sort_ratio(road['nombre'], text), road['gid']])
    if len(intweet)>0:
        geo['road'] = max(intweet)[1]
    elif len(possible)>0:
        geo['road'] = max(possible)[1]
    
    return geo