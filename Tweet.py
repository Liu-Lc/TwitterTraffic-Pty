import re, json
import pandas as pd, numpy as np

stop_words = json.load(open('./others/stop_words.json', encoding='utf8'))

def preprocess(tweet):
    '''Removes next lines, links, mentions, hashtags, stop words, etc.
    Returns a clean tweet text.'''
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
    # lower characters
    tweet = tweet.lower()
    # remove stop words
    tweet = ' '.join([word for word in tweet.split(' ') 
                if not word.lower() in stop_words])
    return tweet

def clean_text(dataframe, column_name):
    '''Receives a dataframe with the text column name and returns
        the dataframe with a clean text column.'''
    df = dataframe[:]
    df['clean'] = df[column_name]
    df['clean'] = df.apply(lambda row: preprocess(row.clean), axis=1)
    return df

def classify_text(dataframe, column_name):
    '''Classifies tweet text depending of the keywords contained.
        Returns dataframe with classification data.'''
    df = dataframe[:]
    # keywords for accident tweets
    df['isAccident'] = np.where(df[column_name].str.contains('accidente|accidentaron|accidentó|choque|chocó|chocaron|choca|chocar|colisión|colisionaron|colisionó|colisiona|colisionado|vuelco|volcó|vuelca|atropello|atropellado'), 1, 0)
    # keywords for obstacles incidents
    df['isObstacle'] = np.where(df[column_name].str.contains('tranque|trancado|embotellamiento|desplazan autos|vistas tráfico|movimiento vehicular|huelga|motín|protesta|protestando|trabajos vía|trabajos|trabajos ruta|cierre|cerraron|cerrado|cierran|cierra|daño|dañó|detuvieron|detenido|detenida|obstáculo|obstaculizando|parado|paro|paño cerrado|tráfico paralizado|tráfico detenido|tráfico afectado|tráfico pesado|tráfico lento|desvío|área acordonada'), 1, 0)
    # keywords for danger incidents
    df['isDanger'] = np.where(df[column_name].str.contains('incendio|incendia|incendiando|incendiado|incendiaron|inundado|inundación|inundó'), 1, 0)
    # finally assigns if it's incident
    df['isIncident'] = np.where(df[['isAccident','isObstacle','isDanger']].sum(axis=1)>0, 1, 0)
    # returns dataframe back
    return df