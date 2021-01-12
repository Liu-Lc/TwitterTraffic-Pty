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
], id='sidebar')

middlebar = html.Div([
    html.H2('Reportes'),
    html.Hr(), controls
], id='middlebar')

content1 = html.Div([
    dcc.Graph(id='graph_1')
], id='map')

content2 = html.Div([
    dcc.Graph(id='graph_2')
], id='graph1')

content = html.Div([
    html.H1('Visualización de incidentes de tráfico'),
    html.Hr(),
    content1, content2
], id='content')

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
app.layout = html.Div([head, sidebar, middlebar, content], id='container')

try:
    app.run_server()
except Exception as e: print(e)