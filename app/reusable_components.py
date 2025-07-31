import dash
from dash import html, dcc, callback, Input, Output, callback_context as ctx, State, no_update
from shared_dash import recipient_DB
import dash_mantine_components as dmc
from shared_dash import recipient_DB
import json, csv

###########################################################################
#################CREATE NEW USER BUTTON START##############################
###########################################################################

def create_new_user_component():
    # Return both components inside a container (e.g., html.Div)
    return html.Div([
        dmc.NotificationContainer(id="notification-container"),
        dcc.Store(id="new_user_button_close"),
        dmc.Button(
            "Create New User",
            variant="outline",
            color="green",
            size="sm",
            radius="sm",
            id="modal-demo-button", # The ID that triggers the modal
            style={"backgroundColor": "#90EE90BA"}
        ),
        
        # The Modal is now part of the layout returned by this function
        dmc.Modal(
            title="Create a New User",
            id="modal-simple",
            children=[
                dmc.Fieldset(
                    children=[
                        dmc.TextInput(label="Name", id="new_user_name", placeholder="Optional, can leave blank"),
                        dmc.TextInput(label="Email", id="new_user_email",placeholder="jSmith@jetrord.com"),
                     
                    ],
                    
                    disabled=False,
                ),
                dmc.Space(h=20),
                dcc.Store(id="bad-email-store", data=None),
                dmc.Alert(
                    "Try again",
                    title="Invalid email!",
                    id="bad-email-alert",
                    color="red",
                    duration=3000,
                ),
                dmc.Group(
                    [
                        dmc.Button("Submit", id="modal-submit-button"),
                        dmc.Button(
                            "Close",
                            color="red",
                            variant="outline",
                            id="modal-close-button",
                        ),
                    ],
                    justify="flex-end",
                ),
            ],
        )
    ])

#updates a specific dcc Store's data to trigger open/closing create user modal
#works in tandem with close_simple_modal below
@callback(
    Output("new_user_button_close","data"),
    Output("bad-email-store",'data'),
    Input("modal-demo-button", "n_clicks"),
    Input("modal-close-button", "n_clicks"),
    Input("modal-submit-button", "n_clicks"),
    State("modal-simple", "opened"),
    State("new_user_email","value"),
    State("bad-email-store",'data'),
    prevent_initial_call=True
)
def modal_demo(nc1, nc2, nc3, opened, email, bad_email_store):
    #keep modal open if invalid email is entered
    if ctx.triggered_id == "modal-submit-button" and email_is_invalid(email):
        return opened, not bad_email_store
    if ctx.triggered_id == "modal-demo-button":
        return True, True #ensure we keep modal open, and don't set off bad email alert
    return not opened, bad_email_store

#when a specific dcc Store's data is altered it opens/closes the create user modal
#works in tandem with modal_demo above
@callback(
    Output("modal-simple", "opened"),
    Input("new_user_button_close","data"),
    State("modal-simple", "opened"),
    prevent_initial_call=True
)
def close_simple_modal(modal_update, opened):
    return modal_update


@callback(
    Output("notification-container", "sendNotifications"),
    Input("modal-submit-button", "n_clicks"),
    State("new_user_name","value"),
    State("new_user_email","value")
)
def add_new_user_to_DB(n_clicks, name, email):
    name = name or "NONE"
    if email_is_invalid(email):
        return dash.no_update
    
    creation_alerts = []
    for email in next(csv.reader([email])):

        add_log = recipient_DB.add_user({"email":email,"name":name})
        print(add_log)
        autoCloseTime = 6000
        big_alert_styles = {
                    # override the outer container
                    "root": {
                        "maxWidth": "1000px",    # make it *really* wide
                        "padding": "1.5rem",      
                    },
                    # bump up the title text
                    "title": {
                        "fontSize": "1.5rem",
                        "marginBottom": "0.5rem",
                    },
                    # bump up the body text
                    "description": {
                        "fontSize": "1.25rem",
                    }
                }
        if add_log == "Email Already Exists":
            creation_alerts.append({
                "action": "show",
                #"position":"bottom-center",
                "title": "🚨 User Not Created 🚨",
                "message": f"A record for {email} already exists",
                "color": "red",
                "autoClose": autoCloseTime,
                "style": {
                    "minWidth": "1000px",     # make it wider
                    "fontSize": "40px",      # bigger text
                    "padding": "16px 24px",  # more breathing room
                },
                "styles": big_alert_styles
            })
        elif add_log == "Name Already Exists":
            creation_alerts.append({
                "action": "show",
                "title": f"User '{name}' Successfully Created",
                "message": f"Warning: this name already existed in the database. Added anyways.",
                "color": "yellow",
                "autoClose": autoCloseTime,
                "style": {
                    "minWidth": "2000px",     # make it wider
                    "fontSize": "20px",      # bigger text
                    "padding": "16px 24px",  # more breathing room
                },
                "styles": big_alert_styles
            })
        
        elif add_log == "User Added Successfully":
            creation_alerts.append({
                "action": "show",
                "title": f"User '{email}' Successfully Created",
                "message": f"Database has been updated with no conflicts!",
                "color": "green",
                "autoClose": autoCloseTime,
                "style": {
                    "minWidth": "1000px",     # make it wider
                    "fontSize": "20px",      # bigger text
                    "padding": "16px 24px",  # more breathing room
                },
                "styles":big_alert_styles
            })
        #this should never be shown
        else:
            creation_alerts.append({
                "action": "show",
                "message": "Error, something unexpected happened",
                "autoClose": autoCloseTime,
            })
    return creation_alerts

@callback(
    Output("bad-email-alert", "hide"),
    Input("bad-email-store", "data"),
    prevent_initial_call=True,
)
def alert_auto(bad_email_store_data):
    return bad_email_store_data


def email_is_invalid(email):
    return email is None or "@" not in email

#########################################################################
#################CREATE NEW USER BUTTON END##############################
#########################################################################











def create_view_users_button():
    return html.Div(
        [
            dcc.Store("store-delete-email"),
            dmc.Button(
                "View/Delete Users",
                variant="outline",
                color="grey",
                size="sm",
                radius="sm",
                id="view-users-button",
                style={"backgroundColor": "rgba(250,128,114,0.5)"}
            ),
            dmc.Modal(
                title="View and Delete Users",
                id="modal-view-users",
                children = [
                    dmc.TextInput(
                        id="filter-input-users-view",
                        placeholder="Filter users by email",
                        radius="xl", # Pill-shaped
                    ),
                    # dmc.ScrollArea is the Mantine way to handle scrollable content
                    dmc.ScrollArea(
                        h="55vh", # height
                        id="button-container-users-view",
                        # Children will be populated by the callback
                    )
                ]
            )
        ]
    )


@callback(
    Output("modal-view-users", "opened"),
    Input("view-users-button","n_clicks"),
    prevent_initial_call=True
)
def open_view_users_modal(n_clicks):
    return True



# Callback to update the list of buttons based on the filter
@callback(
    Output('button-container-users-view', 'children'),
    Input('filter-input-users-view', 'value'),
    Input({"type":"button-delete-user","index":dash.ALL}, "n_clicks"),
    State('button-container-users-view', 'children'),
    prevent_initial_call = True
)
def update_button_list_on_filter(filter_value, n_clicks, children):
    print("\n\n\n")
    #get email associated with last triggered component if component is a delete user button
    #the last triggered componetn may also be the input filter, in which case 'email' will be None
    #email = ctx.triggered_id.get("email")
    print(ctx.triggered_id)
    print(n_clicks)
    print(ctx.triggered)

    
    #when a user clicks on a user button, a delete button for that user is created.
    #this triggeres the Input({"type":"button-delete-user","index":dash.MATCH}, "n_clicks")
    #callback for this function. In this case, we do not want to update anything.
    #'children' remains unchanged from the intial state 
    #can't simply check n_clisk==0 becuase n_clicks will be a list. Have to get a little funky
    triggered = ctx.triggered[0]
    raw = triggered["prop_id"]  #eg '{"index":"jonah@gmail.com","type":"button-delete-user"}.n_clicks'
    comp_id_str, prop_name = raw.rsplit(".", 1)    # split off the ".n_clicks"
    try:
        comp_id = json.loads(comp_id_str) # turn the JSON back into a Python dict
        if comp_id.get("type") == "button-delete-user" and triggered["value"] is None:
            print("NO UPDATE")
            return children
    except json.JSONDecodeError:
        print("decode error")
        pass

    #If the filter text fired, just re‑render the filtered list:
    if isinstance(ctx.triggered_id, str) and ctx.triggered_id == "filter-input-users-view":
        #triggered id is either filter input or removing user; shown users must be updated regardless
        return logic_for_update_button_list(filter_value=filter_value)
    
    #this gets triggered when button is pressed to keep a user
    #(because the button with id.type button-delete-user is erased
    if ctx.triggered_id is None:
        return children
    
    email = ctx.triggered_id.get("index")


    
    #n_click_triggered = [n_click for n_click in n_clicks if ]
    #and not isinstance(n_clicks, list) and n_clicks > 0:
    print("DELETE BUTTON PRESSED")
    delete_user_log = recipient_DB.delete_user(email) #returns a success or failure string
    print(delete_user_log)
    return logic_for_update_button_list(filter_value=filter_value)
    


#updates the children of the stack component containing all users based on filter_value
#eg if filter_value is "xyz", then the returned list will only contain
#buttons containing users whose email's contain "xyz" substring
#used by update_button_list_on_filter() and delete_user_from_db()
def logic_for_update_button_list(filter_value):
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
                        id={'type': 'email-view-button', 'index': email},
                        # "subtle" or "light" variants look great in a list
                        variant="subtle",
                        fullWidth=True, # Makes the button take up the full width
                        justify="center", # Centers the text in the button
                        radius="md"
                    )
                ],
                id={'type':'email-stack','index':email}
            ) for email in filtered_emails
        ] 
    ) 
     # Small spacing between buttons in the list
    
    return new_buttons

#when an email is clicked, add a confirmation and disconfirmation button to that emails parent Stack
@callback(
    Output({"type":'email-stack', "index":dash.MATCH}, "children"),
    Input({"type":'email-view-button', "index":dash.MATCH},"n_clicks"),
    State({"type":'email-stack', "index":dash.MATCH}, "children"),
    Input({"type":"button-keep-user","index":dash.ALL},"n_clicks"),
    prevent_initial_call=True
)
def delete_user_confirmation(n_clicks, children, n_clicks2):
    print("n_clicks2" + str(n_clicks2))

    triggered = ctx.triggered[0]
    raw = triggered["prop_id"]  #eg '{"index":"jonah@gmail.com","type":"button-keep-user"}.n_clicks'
    comp_id_str, prop_name = raw.rsplit(".", 1)    # split off the ".n_clicks"
    try:
        comp_id = json.loads(comp_id_str) # turn the JSON back into a Python dict
        if comp_id.get("type") == "button-keep-user" and triggered["value"] is not None:
            print("KEEPING")
            print(children)

            kept_children = []
            for child in children:
                pid = child.get("props", {}).get("id")
                # pid will be None for the Group, or a dict for the Button
                if isinstance(pid, dict) and pid.get("type") == "email-view-button":
                    kept_children.append(child)
            return kept_children
        
    except json.JSONDecodeError:
        print("decode error")
        pass











    #if a KEEP/DELETE button group is already in the Stack, don't add another button group. Keep as is
    for child in children:
        # Make sure it’s a dict and has the right type
        if isinstance(child, dict) and child.get("type") == "Group":
            return children
        
    email = ctx.triggered_id["index"]
    button_group = dmc.Group(
        [
            dmc.Button(
                "KEEP",
                id={"type":"button-keep-user","index":email},
                color="green"
            ),
            dmc.Button(
                "DELETE",
                id={"type":"button-delete-user","index":email},
                color="red"
            )
        ],
        justify="center"
    )
    return children + [button_group]



#whenever view users is opened/closed, set the email filter to None
#the main reason for this is to trigger the modal containing user emails
#to be reset; this gets rid of any confirmation/disconfirmation buttons
#that are created when someone clicks on an email to delete it
@callback(
    Output("filter-input-users-view","value"),
    Input("modal-view-users", "opened"),
    prevent_initial_call=True
)
def reset_view_users_filter(opened):
    return None









###############ENCODING/DECODING#########################
import base64

def encode_email(email):
    return base64.urlsafe_b64encode(email.encode()).decode()

def decode_email(encoded):
    return base64.urlsafe_b64decode(encoded.encode()).decode()