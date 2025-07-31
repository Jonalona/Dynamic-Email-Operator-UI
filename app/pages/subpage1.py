import dash
from dash import html, dcc, callback, Input, Output


dash.register_page(__name__)

layout = html.Div([
    html.H1("Minimal Dropdown Test", style={'color': 'white'}),
    html.P("Does this dropdown work?", style={'color': 'white'}),
    html.Div([
        dcc.Dropdown(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montreal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value='MTL',
            style={'width': '300px', 'margin': '50px'}
        ),
    ])
], style={'backgroundColor': '#111827', 'padding': '20px'}) # bg-gray-900
