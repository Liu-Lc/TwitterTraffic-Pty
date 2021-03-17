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
def get_classification(dataframe, column):
    '''Receives dataframe with text and returns dataframe with
     classification and categorization data.'''
    # copies dataframe
    df = dataframe[:]
    ## vectorizes data
    vect_data3 = vectorizer3.transform(df[column])
    vect_data10 = vectorizer10.transform(df[column])
    ## classifies and categorizes data
    df['isIncident'] = xgb_classifier.predict(vect_data10)
    df[['isAccident','isObstacle','isDanger']] = mo_classifier.predict(vect_data3)
    # returns result dataframe
    return df