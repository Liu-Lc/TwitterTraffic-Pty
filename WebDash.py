import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2 as ps
from dash.dependencies import Input, Output, State, ClientsideFunction

from TweetData import keys

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
                html.Button('Click', id='button', className='column'),
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
                    dcc.Dropdown(id='graph-categ-options', options=[
                            {'label': 'Diario', 'value': 'day'},
                            {'label': 'Semanal', 'value': 'week'},
                            {'label': 'Mensual', 'value': 'month'},
                            {'label': 'Anual', 'value': 'year'}
                        ],
                        value='day'
                    ),
                    dcc.Graph(id='graph-categ'),
                    # dcc.Interval(id='graph-area-update', interval=1000)
                ]),
                # gráfica derecha
                html.Div(className='pretty_container six columns', children=[
                    dcc.Dropdown(id='graph-time-options', options=[
                            {'label': 'Resumen por día', 'value': 'day'},
                            {'label': 'Resumen por semana', 'value': 'week'},
                            {'label': 'Resumen por mes', 'value': 'month'}
                        ],
                        value='day'
                    ),
                    dcc.Graph(id='graph-time'),
                    # dcc.Interval(id='graph-time-update', interval=1000)
                ])
            ]),
            # sección de abajo con el mapa
            html.Div(className='pretty_container', children=[
                dcc.Graph(id='map')
            ]),
            # sección bajo el mapa
            html.Div(className='pretty_container', children=[
                dcc.Graph(id='others')
            ])
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
    q = '''SELECT U.USER_NAME AS USERNAME, T.TWEET_USER_ID AS USERID, 
            T.TWEET_TEXT AS TEXT FROM TWTTWEET AS T 
            LEFT JOIN TWTUSER AS U ON T.TWEET_USER_ID=U.USER_ID
            RIGHT JOIN TWTINCIDENT AS I ON T.TWEET_ID=I.INC_TWEET_ID
            ORDER BY TWEET_CREATED DESC LIMIT 10; '''
    cursor.execute(q)
    results = cursor.fetchall()
    colnames = [desc[0] 
        for desc in cursor.description]
    cursor.close()
    conn.close()

    df = pd.DataFrame(results, columns=colnames)
    block = []

    for index, tweet in df.iterrows():
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
    Output('graph-categ', 'figure'),
    [Input('graph-categ-options', 'value')]
)
## Gráfica de INCIDENTES POR CATEGORÍA
def graph_categ(option):
    conn = ps.connect(
        database='traffictwt', user='postgres', password=keys.db_pass)
    cursor = conn.cursor()
    q = '''SELECT
        COUNT(CASE WHEN I.ISACCIDENT THEN 1 END) AS accidentes,
        COUNT(CASE WHEN I.ISOBSTACLE THEN 1 END) AS obstáculos,
        COUNT(CASE WHEN I.ISDANGER THEN 1 END) AS peligros
    FROM TWTINCIDENT AS I LEFT JOIN TWTTWEET AS T
    ON I.INC_TWEET_ID=T.TWEET_ID
    WHERE T.TWEET_CREATED>(
        SELECT DATE_TRUNC('DAY', MAX(TWEET_CREATED) - INTERVAL '%i %s') 
        FROM TWTTWEET
    ); ''' % (
        (7 if option=='week' else 1), 
        'day' if option=='week' else option)
    cursor.execute(q)
    results = cursor.fetchall()
    colnames = [desc[0] 
        for desc in cursor.description]
    cursor.close()
    conn.close()

    df = pd.DataFrame(results, columns=colnames)
    Y = df.iloc[0,:]
    # print('\n', db.query(q), '\n')
    data = go.Bar(
        x=colnames,
        y=Y,
        name='categ-graph-bar'
    )
    # # Output is the figure with 'data' and 'layout'
    return {
        'data': [data], # data is a list
        'layout': go.Layout( # axis update limits
            title=go.layout.Title(
                text='Incidentes por categoría',
                y=1, yref='paper', yanchor='bottom',
                pad={ 'b':20 },
                font={ 'size': 20 },
            ),
            xaxis_title='Tipo de incidente',
            xaxis_titlefont={ 'size': 16 },
            xaxis_tickfont={ 'size': 13 },
            yaxis_tickfont={ 'size': 13 },
            height=300,
            margin=go.layout.Margin(l=40, r=40, b=70, t=75, pad=10),
        )}


@app.callback(
    Output('graph-time', 'figure'),
    [Input('graph-time-options', 'value')]
)
## Gráfica de INCIDENTES POR PERÍODO DE TIEMPO
def graph_time(option):
    conn = ps.connect(
        database='traffictwt', user='postgres', password=keys.db_pass)
    cursor = conn.cursor()
    q = '''SELECT DATE_TRUNC('{0}', TWEET_CREATED) AS D, 
                COUNT(TWEET_CREATED) FROM TWTTWEET 
                GROUP BY D ORDER BY D; '''.format(option)
    cursor.execute(q)
    results = cursor.fetchall()
    colnames = [desc[0] 
        for desc in cursor.description]
    cursor.close()
    conn.close()

    df = pd.DataFrame(results, columns=colnames)
    # print('\n', df1, '\n')
    data = go.Bar(
        x=df.iloc[:, 0],
        y=df.iloc[:, 1],
        name='time-graph-bar',
    )
    X = df.iloc[-10:, 0]
    Y = df.iloc[-10:, 1]
    ## XAxis layout
    if option=='day': tickformat='%d/%m/%y'
    elif option=='week': tickformat='S%V/%Y'
    elif option=='month': tickformat='%m/%Y'
    # Output is the figure with 'data' and 'layout'
    return {
        'data': [data], # data is a list
        'layout': go.Layout( # axis update limits
            title=go.layout.Title(
                text='Incidentes por períodos',
                y=1, yref='paper', yanchor='bottom',
                pad={ 'b':20 },
                font={ 'size': 20 },
            ),
            xaxis_title='Fecha',
            xaxis_titlefont={ 'size': 16 },
            xaxis_tickformat=tickformat,
            xaxis_tickfont={ 'size': 13 },
            yaxis_tickfont={ 'size': 13 },
            xaxis=dict(range=[min(X), max(X)]),
            yaxis=dict(range=[min(Y), max(Y)]),
            height=300,
            margin=go.layout.Margin(l=40, r=40, b=70, t=75, pad=10),
        )}


try:
    app.run_server()
except Exception as e:
    print(e)
