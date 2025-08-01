import dash
from dash import html, dcc, callback, Input, Output, callback_context as ctx, State, no_update
from shared_dash import recipient_DB
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from global_vars import *





dash.register_page(__name__, path_template="/user/<email>")


#▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
######################    Component Definitions    ####################
#▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼

def create_select_user_button():
    button = dmc.Button(
        "View a User's Tasks",
        id="select-user-button",
        className="glow-button", 
        variant="outline",
                color="grey",
                size="sm",
                radius="sm",
                style={"backgroundColor": "rgba(114,160,250,0.5)", "--glow-color": "rgba(114,160,250,0.5)"}
    )

    return button

def create_select_user_modal()->dmc.Modal:
    modal = dmc.Modal(
        title="Select User to View Which DAG and Tasks They're Included In",
        id="select-user-modal",
        children=[
            dmc.TextInput(
                id="filter-input-users-view-2",
                placeholder="Filter users by email",
                radius="xl" # Pill-shaped
            ),
            # dmc.ScrollArea is the Mantine way to handle scrollable content
            dmc.ScrollArea(
                h="55vh", # height
                id="button-container-users-view-2",
                # Children will be populated by the callback
            )
            
        ]
    )

    return modal


#▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
######################    Component Definitions    ####################
#▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲






#▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
######################    Callback logic    ###########################
#▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼

@callback(
    Output("select-user-modal", "opened"),
    Output('filter-input-users-view-2', 'value'),
    Input("select-user-button","n_clicks"),
    prevent_initial_call=True
)
def open_view_users_modal(n_clicks):
    return True, ""







# Callback to update the list of buttons based on the filter
@callback(
    Output('button-container-users-view-2', 'children'),
    Input('filter-input-users-view-2', 'value'),
    prevent_initial_call = True
)
def update_button_list_on_filter(filter_value):
    users_dicts = recipient_DB.get_users()
    all_emails = [user["email"] for user in users_dicts]
    if not filter_value:
        filtered_emails = all_emails
    else:
        filtered_emails = [email for email in all_emails if filter_value.lower() in email.lower()]

    if not filtered_emails:
        return dmc.Text("No users found :(", c="dimmed", p="lg")
    
    # Generate a list of dmc.Buttons inside a dmc.Stack
    new_buttons = dmc.Stack(
        [
            dmc.Stack(
                children=[
                    dmc.Button(
                        email,
                        id={'type': 'email-view-button-2', 'index': email},
                        # "subtle" or "light" variants look great in a list
                        variant="subtle",
                        fullWidth=True, # Makes the button take up the full width
                        justify="center", # Centers the text in the button
                        radius="md"
                    )
                ],
                id={'type':'email-stack-2','index':email}
            ) for email in filtered_emails
        ] 
    ) 
     # Small spacing between buttons in the list
    
    return new_buttons
    


@callback(
    Output('url', 'pathname', allow_duplicate=True), #not even sure what allow_duplicate does...
    Input({'type': 'email-view-button-2', 'index': dash.ALL}, "n_clicks"),
    prevent_initial_call = True
)
def change_url_to_user(n_clicks):
    if not any(n_clicks):
        raise dash.exceptions.PreventUpdate

    triggered_id = dash.callback_context.triggered_id
    email = triggered_id['index']
    return f'/user/{email}'

#▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
######################    Callback logic    ###########################
#▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
