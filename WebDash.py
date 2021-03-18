import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

head = html.Div([html.Link(rel="stylesheet",
          href="https://fonts.googleapis.com/css?family=Montserrat")])

sidebar = html.Div([
    html.Div([
        html.H4('Búsqueda'),
        html.Hr(),
        html.Div([
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
    ], className='pretty_container one-half column'),
    html.Div([
        html.H4('Reportes'),
        html.Hr(),
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
        ], className='pretty_container one-half column')
], className='sidebar four columns')

content = html.Div([
    html.Div([
    #     html.Div([
    #         dcc.Graph(id='graph1')
    #     ], className='pretty_container six columns'),
    #     html.Div([
    #         dcc.Graph(id='graph2')
    #     ], className='pretty_container six columns')
    # ], className='row'),
    # html.Div([
    #     dcc.Graph(id='map')
    ], className='pretty_container')
], className='seven columns')

# html.Div(id='output_container', children=[]),
# html.Br(),
# html.Script(src='widgets.js'),
# html.Link(rel='stylesheet', href='styles.css')

## app layout
app.layout = html.Div([
    head,
    html.Div([
        html.H1('Visualización de incidentes de tráfico'),
        html.Hr(),
    ], className='column'),
    html.Div([
        html.Div([
            html.Div([
                html.H4('Búsqueda'),
                html.Hr()
            ], className='pretty_container one-half column'),
            html.Div([
                html.H4('Reportes'),
                html.Hr()
                ], className='pretty_container one-half column')
        ], className='row four columns'),

        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='graph1')
                ], className='pretty_container six columns'),
                html.Div([
                    dcc.Graph(id='graph2')
                ], className='pretty_container six columns')
            ], className='row'),
            html.Div([
                dcc.Graph(id='map')
            ], className='pretty_container')
        ], className='eight columns')
    ], className='container'),
], id='mainContainer')

try:
    app.run_server()
except Exception as e: print(e)