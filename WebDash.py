import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2 as ps
from dash.dependencies import Input, Output, State

from TweetData import keys

app = dash.Dash(__name__)

head = html.Div([html.Link(rel="stylesheet",
          href="https://fonts.googleapis.com/css?family=Montserrat")])

# html.Div(id='output_container', children=[]),
# html.Br(),
# html.Script(src='widgets.js'),
# html.Link(rel='stylesheet', href='styles.css')

# app layout
app.layout = html.Div([
    head,
    html.Div([
        html.H1('Visualización de incidentes de tráfico'),
        html.Hr(),
    ], className='column'),
    html.Div([
        # sección de la izquierda
        html.Div([
            # panel de reportes
            html.Div([
                html.H4('Reportes'),
                html.Hr()
            ], className='pretty_container one-half column'),
            # panel de búsqueda
            html.Div([
                html.H4('Búsqueda'),
                html.Hr()
            ], className='pretty_container one-half column')
        ], className='row four columns'),

        # sección de la derecha
        html.Div([
            # sección de arriba con dos gráficas
            html.Div([
                # gráfica izquierda
                html.Div([
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
                ], className='pretty_container six columns'),
                # gráfica derecha
                html.Div([
                    dcc.Dropdown(id='graph-time-options', options=[
                            {'label': 'Resumen por día', 'value': 'day'},
                            {'label': 'Resumen por semana', 'value': 'week'},
                            {'label': 'Resumen por mes', 'value': 'month'}
                        ],
                        value='day'
                    ),
                    dcc.Graph(id='graph-time'),
                    # dcc.Interval(id='graph-time-update', interval=1000)
                ], className='pretty_container six columns')
            ], className='row'),
            # sección de abajo con el mapa
            html.Div([
                dcc.Graph(id='map')
            ], className='pretty_container'),
            # sección bajo el mapa
            html.Div([
                dcc.Graph(id='others')
            ], className='pretty_container')
        ], className='eight columns')

    ], className='container'),
], id='mainContainer')



@app.callback(
    Output('graph-categ', 'figure'),
    [Input('graph-categ-options', 'value')]
)
def graph_categ(option):
    conn = ps.connect(
        database='traffictwt', user='postgres', password=keys.db_pass)
    cursor = conn.cursor()
    q = '''SELECT
        COUNT(CASE WHEN I.ISACCIDENT THEN 1 END) AS ACCIDENTS,
        COUNT(CASE WHEN I.ISOBSTACLE THEN 1 END) AS OBSTACLES,
        COUNT(CASE WHEN I.ISDANGER THEN 1 END) AS DANGERS
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
            # xaxis=dict(range=[0, len(colnames)]),
            # yaxis=dict(range=[0, max(Y)]),
            height=350,
            margin=go.layout.Margin(autoexpand=True),
        )}


@app.callback(
    Output('graph-time', 'figure'),
    [Input('graph-time-options', 'value')]
)
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
    # Output is the figure with 'data' and 'layout'
    return {
        'data': [data], # data is a list
        'layout': go.Layout( # axis update limits
            title='Prueba',
            xaxis=dict(range=[min(X), max(X)]),
            yaxis=dict(range=[min(Y), max(Y)]),
            height=350,
            margin=go.layout.Margin(l=30, r=30, b=20, t=80, pad=4),
        )}


try:
    app.run_server()
except Exception as e:
    print(e)
