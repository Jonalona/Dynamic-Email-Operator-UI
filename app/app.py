import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from database import DynamicRecipientDB
import dash_mantine_components as dmc
import os

#http://localhost:8887/
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)


# Define the master layout for the entire app.
app.layout = dmc.MantineProvider(
    children=[
         html.Div(
            style={
                "minHeight": "100vh",   
                "display": "flex",
                "flexDirection": "column",
                 "overflow": "hidden" ,
                "width": "100%",        
                "padding": 0           
            },
            children=[
                dash.page_container     # where your pages render
            ]
        ),
        # These components are usually placed outside the main content container.
        dcc.Location(id='url', refresh=True),
        dcc.Store(id="task-email-event-store")
    ]
)
    


#http://localhost:8887/
#enable this when running on local machine
if __name__ == '__main__':
    app.run(debug=True, port=8050, host='0.0.0.0',)


#https://dynamic-email-operator-ui.onrender.com/dags/Click_Me!
#enable this when running through Render.com host site
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 10000))
#     app.run(host="0.0.0.0", port=port)