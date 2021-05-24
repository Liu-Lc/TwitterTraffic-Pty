#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Created on 
@author: Lucia Liu (lucia.liu@utp.ac.pa)
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.colors as pcol
import plotly.express as px
import plotly.graph_objects as go
import psycopg2 as ps
from dash.dependencies import ClientsideFunction, Input, Output, State
from wordcloud import WordCloud

from io import BytesIO
import base64
import re, random

from TweetData import keys


headers = ['tweetid', 'userid', 'username', 'text', 'link']
tweets_df = pd.DataFrame(columns=headers)

app = dash.Dash(__name__)

# html.Script(src='widgets.js'),
# html.Link(rel='stylesheet', href='styles.css')

# app layout
app.layout = html.Div(id='mainContainer', children=[
    html.Link(rel="stylesheet",
          href="https://fonts.googleapis.com/css?family=Montserrat"),
    html.Div(className='column', children=[
        html.H1('Visualización de incidentes de tráfico'),
        html.Hr(),
    ]),
    html.Div(className='container', children=[
        # sección de la izquierda
        html.Div(className='row four columns', children=[
            # panel de reportes
            html.Div(className='pretty_container column', children=[
                html.H4('Reportes'),
                html.Hr(),
                html.Button('Generate', id='button'),
                html.Div(className='column', children=[
                    html.Ol(id='tweets-list',
                        className='tweet-list', children=[]),
                ]),
                dcc.Interval(id='get-tweets-interval', interval=5000),
                html.Script(src='https://platform.twitter.com/widgets.js')
            ]),
        ]),

        # sección de la derecha
        html.Div(className='eight columns', children=[
            # sección de arriba con dos gráficas
            html.Div(className='row', children=[
                # gráfica izquierda
                html.Div(className='pretty_container six columns', children=[
                    dcc.Dropdown(id='type-options', className='dropdown', options=[
                            {'label': 'Incidentes por categoría', 'value': 'categ'},
                            {'label': 'Incidentes por período de tiempo', 'value': 'time'}
                        ],
                        value='categ'
                    ),
                    dcc.Dropdown(id='subtype-options', className='dropdown'),
                    dcc.Graph(id='graph-type'),
                ]),
                # gráfica derecha
                html.Div(className='pretty_container six columns', children=[
                        dcc.Dropdown(id='wordcloud-options', className='dropdown', 
                            options=[
                                {'label': 'Diario', 'value': 'day'},
                                {'label': 'Semanal', 'value': 'week'},
                                {'label': 'Mensual', 'value': 'month'},
                                {'label': 'Anual', 'value': 'year'}
                            ],
                            value='day'
                        ),
                        dcc.Graph(id='graph-wordcloud'),
                        # html.Img(id="image-wordcloud"),
                ]),
                ## These intervals just put one?
                dcc.Interval(id='graphs-update', interval=5000)
            ]),
            # sección de abajo con el mapa
            html.Div(className='pretty_container', children=[
                dcc.Graph(id='map')
            ]),
            # sección bajo el mapa
            # html.Div(className='pretty_container', children=[
            #     dcc.Graph(id='others')
            # ])
        ])

    ]),
])


## -----------------------------------------

@app.callback(
    Output('tweets-list', 'children'),
    # [Input('get-tweets-interval', 'n_intervals'),
    [Input('button', 'n_clicks'),
    Input('tweets-list', 'children')]
)
## Get streaming tweets
def update_tweets(interval, children):
    conn = ps.connect(
        database='traffictwt', user='postgres', password=keys.db_pass)
    cursor = conn.cursor()
    q = '''SELECT TWEET_ID AS TWEETID, USER_NAME AS USERNAME,
            USER_ID AS USERID, TWEET_TEXT AS TEXT 
            FROM TWEET WHERE ISINCIDENT=TRUE
            ORDER BY TWEET_ID DESC LIMIT 10; '''
    cursor.execute(q)
    results = cursor.fetchall()
    colnames = [desc[0] 
        for desc in cursor.description]
    cursor.close()
    conn.close()

    global tweets_df
    df = pd.DataFrame(results, columns=colnames)

    if len(tweets_df)>0:
        new_data = df[df.tweetid > max(tweets_df.tweetid)].sort_values('tweetid', 
            ascending=False).copy()
    else: new_data = df.copy()

    tweets_df = tweets_df.merge(new_data, 
        how='outer').sort_values('tweetid', ascending=False)
    
    block = []

    for index, tweet in new_data.iterrows():
        block += [html.Li(className='tweet-card', children=[
                html.Div(className='tweet-content', children=[
                    html.Span(
                        html.Strong(tweet.username),
                    ),
                    html.Span(' @' + tweet.userid),
                    html.P(className='tweet-text', children=[tweet.text])
                ])
            ])]

    if children==None: return block
    else: return block + children


@app.callback(
    [Output('subtype-options', 'options'),
    Output('subtype-options', 'value')],
    [Input('type-options', 'value')] 
)
## Dropdown options
def type_option(option): 
    if option=='categ':
        options=[
                    {'label': 'Diario', 'value': 'day'},
                    {'label': 'Semanal', 'value': 'week'},
                    {'label': 'Mensual', 'value': 'month'},
                    {'label': 'Anual', 'value': 'year'}
                ]
    elif option=='time':
        options=[
                    {'label': 'Resumen por día', 'value': 'day'},
                    {'label': 'Resumen por semana', 'value': 'week'},
                    {'label': 'Resumen por mes', 'value': 'month'}
                ]
    return options, 'day'


@app.callback(
    Output('graph-type', 'figure'),
    [Input('type-options', 'value'),
    Input('subtype-options', 'value')]
)
## Gráfica de INCIDENTES POR CATEGORÍA O POR PERÍODOS
def graph_type(type, subtype):
    conn = ps.connect(
        database='traffictwt', user='postgres', password=keys.db_pass)
    cursor = conn.cursor()
    if type=='categ':
        q = '''SELECT
            COUNT(CASE WHEN ISACCIDENT THEN 1 END) AS accidentes,
            COUNT(CASE WHEN ISOBSTACLE THEN 1 END) AS obstáculos,
            COUNT(CASE WHEN ISDANGER THEN 1 END) AS peligros
        FROM TWEET WHERE TWEET_CREATED>(
            SELECT DATE_TRUNC('DAY', MAX(TWEET_CREATED) - INTERVAL '%i %s') 
            FROM TWEET
        ); ''' % (
            (7 if subtype=='week' else 1), 
            'day' if subtype=='week' else subtype)
    elif type=='time':
        q = '''SELECT DATE_TRUNC('%s', TWEET_CREATED) AS D, 
                    COUNT(TWEET_CREATED) FROM TWEET 
                    GROUP BY D ORDER BY D; ''' % (subtype)
    cursor.execute(q)
    results = cursor.fetchall()
    colnames = [desc[0] 
        for desc in cursor.description]
    cursor.close()
    conn.close()

    df = pd.DataFrame(results, columns=colnames)
    X = colnames if type=='categ' else df.iloc[-10:, 0]
    Y = df.iloc[0,:] if type=='categ' else df.iloc[-10:, 1]
    
    data = go.Bar(
        x=X,
        y=Y,
        name='graph-bar'
    )

    ## XAxis layout
    if type=='time':
        if subtype=='day': tickformat='%d/%m/%y'
        elif subtype=='week': tickformat='S%V/%Y'
        elif subtype=='month': tickformat='%m/%Y'
    else: tickformat=None

    # # Output is the figure with 'data' and 'layout'
    return {
        'data': [data], # data is a list
        'layout': go.Layout( # axis update limits
            title=go.layout.Title(
                text='Incidentes por %s' % ('categoría' if type=='categ' else 'períodos'),
                y=1, yref='paper', yanchor='bottom',
                pad={ 'b':20 },
                font={ 'size': 20 },
            ),
            xaxis_title='Tipo de incidente' if type=='categ' else 'Fecha',
            xaxis_tickformat=tickformat,
            xaxis_titlefont={ 'size': 16 },
            xaxis_tickfont={ 'size': 13 },
            yaxis_tickfont={ 'size': 13 },
            height=300,
            margin=go.layout.Margin(l=40, r=40, b=70, t=75, pad=10),
        )}


@app.callback(
    Output('graph-wordcloud', 'figure'),
    [Input('wordcloud-options', 'value')]
    # Input('graphs-update', 'n_intervals')]
)
## Nube de palabras
def graph_wordcloud(option):
    conn = ps.connect(
        database='traffictwt', user='postgres', password=keys.db_pass)
    cursor = conn.cursor()
    q = '''SELECT TWEET_TEXT AS TEXT 
            FROM TWEET
            WHERE TWEET_CREATED>(
                SELECT DATE_TRUNC('DAY', MAX(TWEET_CREATED) - INTERVAL '%i %s') 
                FROM TWEET
            ); ''' % (
                (7 if option=='week' else 1), 
                'day' if option=='week' else option)
    cursor.execute(q)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    tweets = [word for word in [t[0].split(' ') for t in results]][:30]
    print(tweets)
    # tweets = ' '.join(re.findall('([A-Z]\S+)', tweets))

    colors = [pcol.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(30)]
    weights = [random.randint(15, 35) for i in range(30)]

    data = go.Scatter(x=[random.choices(range(30), k=30)],
                    y=[random.choices(range(30), k=30)],
                    mode='text',
                    text=tweets,
                    marker={'opacity': 0.3},
                    textfont={'size': weights,
                            'color': colors})
   
    return go.Figure(data = [data], 
        layout = go.Layout(
            title=go.layout.Title(
                text='Incidentes por %s' % ('categoría' if type=='categ' else 'períodos'),
                y=1, yref='paper', yanchor='bottom',
                pad={ 'b':20 },
                font={ 'size': 20 },
            ),
            xaxis={
                'showgrid': False, 'showticklabels': False, 'zeroline': False
            },
            yaxis={
                'showgrid': False, 'showticklabels': False, 'zeroline': False
            },
            # xaxis_title='Tipo de incidente' if type=='categ' else 'Fecha',
            # xaxis_titlefont={ 'size': 16 },
            # xaxis_tickfont={ 'size': 13 },
            # yaxis_tickfont={ 'size': 13 },
            height=300,
            margin=go.layout.Margin(l=40, r=40, b=70, t=75, pad=10)
        ))
    

try:
    app.run_server()
except Exception as e:
    print(e)
