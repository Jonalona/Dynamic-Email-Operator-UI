import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# A minimal app with JUST ONE dropdown to see if it renders.
# It uses the same theme and external scripts as your main app.
app = dash.Dash(__name__)

app.layout = html.Div([
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

# import dash
# from dash import dcc, html, Input, Output, State, ALL, MATCH, ctx
# import dash_bootstrap_components as dbc
# import json
# import copy
# from datetime import date

if __name__ == '__main__':
    # Use host='0.0.0.0' to make the app accessible in Docker
    app.run(debug=True, host='0.0.0.0')