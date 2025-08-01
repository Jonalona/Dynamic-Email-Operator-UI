import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from database import DynamicRecipientDB
import dash_mantine_components as dmc
import os

#http://localhost:8887/
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

dark_theme_shadows = {
    "xs": "1px 1px 3px rgba(255, 255, 255, 0.05)",
    "sm": "1px 1px 4px rgba(255, 255, 255, 0.1)",
    "md": "2px 2px 6px rgba(255, 255, 255, 0.1)",
    "lg": "3px 3px 8px rgba(255, 255, 255, 0.1)",
    "xl": "4px 4px 12px rgba(255, 255, 255, 0.12)", # <-- This is the one you are using
}

# Define the master layout for the entire app.
# The key is to wrap everything in a dmc.MantineProvider.
app.layout = dmc.MantineProvider(

    children=[
        # This container will wrap all of your pages and ensure
        # they have a full-width area to render in.
         html.Div(
            style={
                "minHeight": "100vh",   # full screen (slightly taller than viewport)
                "display": "flex",
                "flexDirection": "column",
                 "overflow": "hidden" ,
                "width": "100%",        # ensure full width
                "padding": 0            # replaces Mantine's p=0
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
    





#Render specific only
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)













dag_JSON = {
    "115_Daily_Performance_Email":["data_pull","email_prep"],
    "115_outbound_optimization_V2":["pull_and_process","prepare_email"],
    "407_Daily_Performance_Email":["data_pull","email_prep"],
    "436_Daily_Performance_Email":["data_pull","email_prep"],
    "499_Daily_Performance_Email":["data_pull","email_prep"],
    "499_outbound_optimization_V2":["pull_and_process","prepare_email"],
    "712_Daily_Performance_Email":["data_pull","email_prep"],
    "BCG_Split":["bcg_split_start","remove_previous_upload","count_generator","split_all_files","compressor","uploader","remove_og_files","success_emailer"]
}
