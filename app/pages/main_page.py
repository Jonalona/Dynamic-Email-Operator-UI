import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from reusable_components import create_new_user_component, create_view_users_button
from select_user import create_select_user_button, create_select_user_modal
from global_vars import *
# Assume ALL_DAGS is your list of DAG IDs


dash.register_page(__name__, path='/', name="Home") # Example registration

def layout():
    # Use dmc.Paper to create a styled container with a shadow
    return dmc.Container(
        [
            dmc.Text("hi")
        ]
    )
