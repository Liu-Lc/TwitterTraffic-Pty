import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

head = html.Div([html.Link(rel="stylesheet",
          href="https://fonts.googleapis.com/css?family=Montserrat")])

controls = html.Div([
    html.P('Dropdown', style={'textAlign': 'center'}),
    dcc.Dropdown(
        options=[{
            'label': 'Value One',
            'value': 'value1'
        }, {
            'label': 'Value Two',
            'value': 'value2'
        }, {
            'label': 'Value Three',
            'value': 'value3'
        }],
        value=['value1'],  # default value
        multi=True
    ),
    html.Br()
])

sidebar = html.Div([
    html.H2('Búsqueda'),
    html.Hr(), controls
], className='pretty_container sidebar two columns')

middlebar = html.Div([
    html.H2('Reportes'),
    html.Hr(), controls
], className='pretty_container sidebar two columns')

content1 = html.Div([
    dcc.Graph(id='graph1')
], className='pretty_container six columns')

content2 = html.Div([
    dcc.Graph(id='graph2')
], className='pretty_container six columns')

mapgraph = html.Div([
    dcc.Graph(id='map')
], className='row pretty_container')

content = html.Div([
    html.H1('Visualización de incidentes de tráfico'),
    html.Hr(),
    html.Div([
        content1, content2
    ], className='row flex'),
    mapgraph
], className='six columns')

    # html.Div(id='output_container', children=[]),
    # html.Br(),

    # html.Script(src='widgets.js'),
    # html.Blockquote(className="twitter-tweet", children=[
    #     html.A("", href="https://twitter.com/Lc_L23/status/1348473789613535232?s=20")
    # ]),
    # html.Blockquote(className="twitter-tweet", children=[
    #     html.A("", href="https://twitter.com/Lc_L23/status/1348418144038236160?ref_src=twsrc%5Etfw")
    # ]),
    # html.Blockquote(className="twitter-tweet", children=[
    #     html.A("", href="https://twitter.com/Lc_L23/status/1348437846978400256?s=20")
    # ]),
    # html.Blockquote(className="twitter-tweet", children=[
    #     html.A("", href="https://twitter.com/Lc_L23/status/1348437952439980033?s=20")
    # ]),

    # dcc.Graph(id='graph', figure={}),

    # html.Link(rel='stylesheet', href='styles.css')
# ])

## app layout
app.layout = html.Div([
    head,
    html.Div([
        sidebar, middlebar, content
    ], className='row')
],id='mainContainer')

try:
    app.run_server()
except Exception as e: print(e)