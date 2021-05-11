import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

from TweetData import DBConnect, keys

db = DBConnect.DB_Connection()
db.connect(password=keys.db_pass)

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
                    dcc.Dropdown(options=[
                            {'label': 'Value One', 'value': 'value1'},
                            {'label': 'Value Two', 'value': 'value2'},
                            {'label': 'Value Three', 'value': 'value3'}
                        ],
                        value='value1'
                    ),
                    # dcc.Graph(id='graph-area')
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
    Output('graph-time', 'figure'),
    [Input('graph-time-options', 'value')]
)
def graph_time(option):
    query = '''SELECT DATE_TRUNC('%s', TWEET_CREATED) AS D, 
                COUNT(TWEET_CREATED) FROM TWTTWEET 
                GROUP BY D ORDER BY D; ''' % option
    results = db.query(query)
    df = pd.DataFrame(results, columns=[option, 'count'])
    data = go.Bar(
        x=df.iloc[:, 0],
        y=df.iloc[:, 1],
        name='time-graph-bar',
    )
    X = df.iloc[-10:, 0]
    Y = df.iloc[-10:, 1]
    # Output is the figure with 'data' and 'layout'
    return {
        # data is a list
        'data': [data],
        'layout': go.Layout(
            # axis update limits
            xaxis=dict(range=[min(X), max(X)]),
            yaxis=dict(range=[min(Y), max(Y)]),
            height=350,
            margin=go.layout.Margin(autoexpand=True),
        )}


try:
    app.run_server()
except Exception as e:
    print(e)
