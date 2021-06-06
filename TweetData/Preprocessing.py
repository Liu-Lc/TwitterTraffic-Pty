import re, json
import pandas as pd, numpy as np

stop_words = json.load(open('./files/stop_words.json', encoding='utf8'))

def preprocess(tweet):
    """Removes next lines, links, mentions, hashtags, stop words, etc.

    Args:
        tweet (string): Tweet text.

    Returns:
        string: Tweet text cleaned.
    """
    # remove next lines
    tweet = re.sub('\n', ' ', tweet)
    # remove links
    tweet = re.sub('http\S+\s*', '', tweet)
    # remove between parentesis
    tweet = re.sub('\[.*\]','', tweet)
    # remove mentions
    tweet = re.sub("@\w+", "", tweet)
    # remove hashtags
    tweet = re.sub("#\w+", "", tweet)
    # alphanumeric and hashtags
    tweet = re.sub("[^a-zA-Z0-9ñáéíóúÁÉÍÓÚüÜ]", " ", tweet)
    # remove multiple spaces
    tweet = re.sub("\s+", " ", tweet)
    tweet = re.sub('^\s+', '', tweet)
    # lower first character
    try: tweet = tweet[0].lower() + tweet[1:]
    except: pass
    # remove stop words
    tweet = ' '.join([word for word in tweet.split(' ') 
                if not word.lower() in stop_words])
    #replace tildes
    tweet = re.sub('á', 'a', tweet)
    tweet = re.sub('é', 'e', tweet)
    tweet = re.sub('í', 'i', tweet)
    tweet = re.sub('ó', 'o', tweet)
    tweet = re.sub('ú', 'u', tweet)
    tweet = re.sub('ü', 'u', tweet)
    return tweet

def clean_text(dataframe, column_name):
    """Receives a dataframe with the text column name and returns
        the dataframe with a clean text column.

    Args:
        dataframe (Pandas.DataFrame): Tweets data table.
        column_name (string): Tweet text column name.

    Returns:
        Pandas.DataFrame: Dataframe with a clean text column.
    """
    df = dataframe.copy()
    df.loc[:,'clean'] = df.loc[:,column_name].copy()
    df.loc[:,'clean'] = df.apply(lambda row: preprocess(row.clean), axis=1)
    return df