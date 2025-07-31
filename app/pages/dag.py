import dash
from dash import html, dcc, callback, Input, Output, callback_context as ctx, State, no_update
from shared_dash import recipient_DB
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from global_vars import *





dash.register_page(__name__, path_template="/dags/<dag_id>")


#▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
######################    Layout    ###################################
#▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼

# Define the layout as a FUNCTION.
# Dash will automatically pass the value captured from the URL
# into the argument with the same name (dag_id).
def layout(dag_id=None):
    #error handling if url doesn't correspond with existing dag id
    dag_tasks = None
    try:
        dag_tasks = dag_JSON[dag_id]
    except KeyError:
        return dmc.Center(
                children=[
                    dmc.Text(
                        f"DAG ID '{dag_id}' does not exist",
                        variant="gradient",
                        gradient={"from": "red", "to": "yellow", "deg": 45},
                        style={"fontSize": 40},
                    )
                ]
            )
    


    """
    This function is called by Dash whenever a user navigates to a URL
    matching the path_template.
    """
    add_recipients_modal = dmc.Modal(
                title="Add Recipients",
                id="add-recipients-modal",
                children = [
                    dcc.Store(
                        id="current-dag-id_store",
                        data=dag_id
                    ),
                    #not even sure this store is ever used... would be extremely easy to check... oh well!
                    dcc.Store(
                        id="dag-tasks-store",
                        data=dag_tasks
                    ),
                    dmc.ScrollArea(
                        h="50vh", # height
                        id="xxx",
                        children = populate_add_recipients_tasks_modal(dag_tasks)
                    ),
                    dmc.Flex(
                        [
                            dmc.Button("To",id={"button_type":"send_type_add_recipient","index":"to_"},color=to_bg_color,variant="filled"),
                            dmc.Button("CC",id={"button_type":"send_type_add_recipient","index":"cc"},color=cc_bg_color, variant="outline"),
                            dmc.Button("BCc",id={"button_type":"send_type_add_recipient","index":"bcc"},color=bcc_bg_color,variant="outline")
                        ],
                        justify="center"
                    ),
                    dmc.Text(
                        ("Enter Email's to add to selected tasks (default sendtype is 'to')" )
                    ),
                    dmc.Text([
                        dmc.Text("Emails with invalid format will be ignored. ", c="red", span=True),
                        dmc.Text(
                            "Emails with valid format yet who are not yet registered in the database "
                            "(i.e. a new user) will have a new account automatically created for them.",
                            c="yellow",
                            span=True
                        )
                    ]),
                    dmc.Textarea(
                        placeholder="Can enter one or more comma separated emails. Each email may be encased in quotations. e.x:\n" \
                        "\"jonah@reisner.com\", saifi@usama.com ",
                        id="add-emails-textarea",
                        w="457w",
                        autosize=True,
                        minRows=2,
                        maxRows=5,
                        error=False
                    ),
                    dmc.ScrollArea(
                        style={
                            "display": "flex",
                            "flexDirection": "row-reverse",  # right-to-left
                            "flexWrap": "wrap",              # wrap to next line
                            "gap": "8px",
                        },
                        type="auto",
                        id="email-badges-scrollarea"
                    ),
                    dmc.Button(
                        "Add Email(s) to database",
                        id="submit-new-emails-button",
                        color="green",
                        fullWidth=True
                    )
                ],
                size="50vw",
                padding="xl"
            )

    all_tasks_stack = dmc.Stack(
        [
        
            # Example: A placeholder for a graph
            dmc.ScrollArea(
                h="75vh",  # Corresponds to height: '55vh'
                p="md",    # Corresponds to padding: '10px'
                style={"border": "1px solid #ccc"},
                id='task-container',
                children=populate_task_container(dag_id)
            ),

            # Link to go back home
            dmc.Anchor(

                href="/",
                # dmc.Group is used to add an icon next to the text
                children=dmc.Group([
                    DashIconify(icon="feather:arrow-left"),
                    "Go back to Home"
                ])
            )
        ],
        id="all_tasks_stack"
    )

    sendtype_stack = dmc.Stack(
        [
            dmc.Text(
                "Select Send Type",        # ✅ Title
                size="sm",                 # Small chic text
                fw=500,      # Semi-bold
                c="black",            # Subtle color
                style={"textAlign": "center", "marginBottom": "0px"}  # ✅ Center + flush
            ),
            dmc.ButtonGroup(
                [
                    dmc.Button("To",id={"button_type":"send_type","index":"to_"},color=to_bg_color, 
                               className="glow-button", style={"--glow-color": str(to_bg_color)}, 
                               size="lg", fullWidth=True),
                    dmc.Button("CC",id={"button_type":"send_type","index":"cc"},color=cc_bg_color, 
                        className="glow-button", style={"--glow-color": str(cc_bg_color)}, 
                        size="lg", fullWidth=True),
                    dmc.Button("BCc",id={"button_type":"send_type","index":"bcc"},color=bcc_bg_color, 
                               className="glow-button", style={"--glow-color": str(bcc_bg_color)}, 
                               size="lg", fullWidth=True)
                ],
                style={"width": "100%"}
            )
        ],
        gap=1,                     # Minimal gap between title and buttons
        style={"width": "100%", "alignItems": "center"}  # ✅ Center contents
    )

    add_recipients_button = dmc.Button(
        "Add Recipients",
        id="add-recipients-button",
        variant="gradient",
        gradient={"from": "teal", "to": "lime", "deg": 105},
        className="glow-button",
        size="lg"
    )

    delete_recipients_button = dmc.Button(
        "Delete Recipients",
        id="delete-recipients-button",
        variant="gradient",
        gradient={"from": "red", "to": "pink", "deg": 105},
        className="glow-button",
        style={"--glow-color": "red"},
        size="lg"
    )

    side_buttons_stack = dmc.Stack(
        [
            sendtype_stack,
            add_recipients_button,
            delete_recipients_button
        ],
        id="side-buttons-stack"
    )


    #package everything together and return it
    return dmc.Container(
        [
            add_recipients_modal,
            dcc.Store(id="bg-type-store", storage_type="memory",data=None),
            dmc.Stack([
                dmc.Title(f"Details for DAG: {dag_id}", order=1),
                dmc.Divider(),
                dmc.Grid(
                    [
                        dmc.GridCol(all_tasks_stack, span=85,style={"height": "100%"}),
                        dmc.GridCol(side_buttons_stack, span=15,style={"height": "100%"})
                    ],
                    columns=100,
                    style={"flex": 1, "height": "100%"}
                )
            ])
        ],
        size="fluid",
        bg="var(--mantine-color-blue-light)",
        style={"height": "100vh","flex":1   },
        id="main_container_dag",
    )


#▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
######################    Layout    ###################################
#▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲


#returns color corresponding to (to_cc_bcc) attributes of recipient 
#with matching user_id, dag_id, task_id, and flag_id in id_dict
#   id_dict MUST ONLY contain user_id, dag_id, task_id, and flag_id
def recip_color_from_id_dict(id_dict:dict):
    #get all data pertaining to that recipient.
    #specifically, all we want are (to_,cc,bcc) attributes
    user_dict = recipient_DB.get_recipient_by_dag_task_flag_user(id_dict)

    sendType_dict = {"to_":user_dict["to_"], "bcc":user_dict["bcc"], "cc":user_dict["cc"]}
    return recip_color_from_sendType_dict(sendType_dict)

def recip_color_from_sendType_dict(sendType_dict:dict):
    grad = no_bg_color
    if sendType_dict["to_"]:
        grad = to_bg_color
    if sendType_dict["bcc"]:
        grad = bcc_bg_color
    if sendType_dict["cc"]:
        grad = cc_bg_color
    if sendType_dict["to_"] and sendType_dict["cc"]:
        grad = f'linear-gradient(to right, {to_bg_color} 50%, {cc_bg_color} 50%)'
    if sendType_dict['to_'] and sendType_dict['bcc']:
        grad = f'linear-gradient(to right, {to_bg_color} 50%, {bcc_bg_color} 50%)'
    if sendType_dict["cc"] and sendType_dict["bcc"]:
        grad = f'linear-gradient(to right, {cc_bg_color} 50%, {bcc_bg_color} 50%)'
    if sendType_dict['to_'] and sendType_dict['cc'] and sendType_dict['bcc']:
        # grad = f'linear-gradient(to right, {to_bg_color} 33%, {cc_bg_color} 33%, #20c997 66%, #ffc107 66%)'
        #grad = f'linear-gradient(to right, {to_bg_color} 33%, {cc_bg_color} 33%,3%)'
        #grad = f'linear-gradient(to right, {to_bg_color}, {bcc_bg_color}, {cc_bg_color})'
        grad = f'linear-gradient(to right, {to_bg_color} 33%, {cc_bg_color} 33%, {cc_bg_color} 66%, {bcc_bg_color} 66%)'
    return grad


def populate_task_container(dag_id):
    def recipients_from_dag_task_ids(dag_id, task_id):
        user_dicts = recipient_DB.get_recipients_by_dag_task(dag_id, task_id)
        print([user["email"] for user in user_dicts])
        return user_dicts
    
    
    
    if dag_id not in dag_JSON:
        return [dmc.Alert("DAG not found.", color="red", title="Error")]
    

    task_papers = []
    for task_id in dag_JSON[dag_id]:
        recipient_dicts = recipients_from_dag_task_ids(dag_id, task_id)

        
        email_buttons = []
        for recipient in recipient_dicts:
  
                button = dmc.Button(
                    recipient["email"],
                    id={"type": "sub_task_email", "user_id": recipient["user_id"], "dag_id":dag_id, "task_id":task_id, "flag_id":recipient["flag_id"]},
                    variant="filled", # Ensures the background color is solid
                    size="lg",        # A good, readable size
                    radius="xl",      # Makes it pill-shaped
                    # The style prop allows for custom CSS like our gradient
                    style={"background": recip_color_from_sendType_dict({"to_":recipient["to_"], "bcc":recipient["bcc"], "cc":recipient["cc"]})},
                    className = "glow-button" #expands and glows on hover
                )
                store = dcc.Store(id={"store-type":"delete-email",
                                "task_id":task_id,
                                    "user_id": recipient["user_id"],
                                    "dag_id": dag_id,
                                    "flag_id": recipient["flag_id"]}, 
                                    data=None)
            
                email_buttons.append(button)
                email_buttons.append(store)

        # Use dmc.Paper as a container for each task section
        task_block = dmc.Paper(
            children=[
                dmc.Title(task_id, order=3),
                # dmc.Group is a flex container, perfect for arranging the buttons
                dmc.Group(email_buttons, mt="sm", id={"type":"group-email-buttons", "task_id":task_id, "dag_id":dag_id})
            ],
            withBorder=True,
            shadow="xl",
            p="md", # Padding
            mb="lg",  # Margin-bottom
            style={
                "backgroundColor": "#EBF0F0B2", # Dark gray at 80% opacity
                "boxShadow": "0px 3px 8px 0px rgba(0, 0, 0, 0.25)"
            },
        )
        task_papers.append(task_block)

    return task_papers




@callback(
    Output('main_container_dag', 'bg'),
    Output('bg-type-store','data'),
    Input({"button_type":"send_type","index":dash.ALL},"n_clicks"),
    Input("delete-recipients-button", "n_clicks"),
    State('main_container_dag',"bg"),
    prevent_initial_call=True,
    allow_duplicate=True
)
def handle_options_click_event(n_clicks, n_clicks_delete, current_bg):
    button_id = ctx.triggered_id
    bg_color = None
    clicked=None
    if isinstance(button_id, dict):
        if button_id["index"] == "to_":
            bg_color = to_bg_color
            clicked = "to_"
        if button_id["index"] == "cc":
            bg_color = cc_bg_color
            clicked = "cc"
        if button_id["index"] == "bcc":
            bg_color = bcc_bg_color
            clicked = "bcc"
    elif isinstance(button_id, str):
        if button_id == "delete-recipients-button":
            bg_color = delete_bg_color
            clicked = "delete"
    if (current_bg == to_bg_color and clicked == "to_" or
            current_bg == cc_bg_color and clicked == "cc" or
            current_bg == bcc_bg_color and clicked == "bcc" or
            current_bg == delete_bg_color and clicked == "delete"):
        bg_color = no_bg_color
    return bg_color, clicked

@callback(
    Output({"type": "sub_task_email", "user_id": dash.MATCH, "dag_id":dash.MATCH,"task_id":dash.MATCH, "flag_id":dash.MATCH}, 'style'),
    Output({"store-type":"delete-email","task_id":dash.MATCH, "user_id": dash.MATCH, "dag_id":dash.MATCH, "flag_id":dash.MATCH}, "data"), #DONOW
    State("bg-type-store",'data'),
    Input({"type": "sub_task_email", "user_id": dash.MATCH, "dag_id":dash.MATCH,"task_id":dash.MATCH, "flag_id":dash.MATCH}, "n_clicks"),
    Input({"type": "sub_task_email", "user_id": dash.MATCH, "dag_id":dash.MATCH,"task_id":dash.MATCH, "flag_id":dash.MATCH}, "children"),
    prevent_initial_call=True
)
def handle_email_button_click(bg_type, n_clicks, button_label_email):
    print("EMAIL CLICKED")
    button_id = ctx.triggered_id
    if button_id is None or bg_type is None:
        print("handle_email_button_click MISFIRE")
        return no_update, None
    
    send_types = ["to_", "bcc", "cc"]
    if bg_type in send_types:
        id_dict = {"dag_id":button_id["dag_id"], "task_id":button_id["task_id"], "flag_id":button_id.get("flag_id","DEFAULT"), "user_id":button_id["user_id"]}
        recipient_DB.update_recipient_send_type(id_dict, bg_type)
        new_email_color = recip_color_from_id_dict(id_dict)
        
        return {"background": new_email_color}, None
    
    if bg_type == "delete":
        print("DELETE DETECTED")
        return no_update, {"email":button_label_email, "dag_id":button_id["dag_id"], "task_id":button_id["task_id"], "flag_id":button_id.get("flag_id","DEFAULT"), "user_id":button_id["user_id"]}



    
@callback(
        Output({"type":"group-email-buttons", "task_id":dash.MATCH, "dag_id":dash.MATCH}, "children"),
        Input({"store-type":"delete-email","task_id":dash.MATCH, "user_id": dash.ALL, "dag_id":dash.MATCH, "flag_id":dash.ALL}, "data"),
        State({"type":"group-email-buttons", "task_id":dash.MATCH, "dag_id":dash.MATCH}, "children"),
        prevent_initial_call = True
)
def delete_email_store_triggered(datas, current_task_email_buttons):

    print("GOT TO EMAIL DELETE SECTION")
    triggered_id = ctx.triggered_id
    delete_email_id = None #need to set this to the corresponding value in datas
    # ctx.inputs_list is a nested list of dicts with IDs and their properties
    for i, data in enumerate(datas):
        id_dict = ctx.inputs_list[0][i]["id"]  # the ID for this data
        print("Data:", data, " came from ID:", id_dict)
        if data is not None and all(data[k] == triggered_id[k] for k in ["dag_id","task_id"]):
            delete_email_id = data
            break
    
    #the store might've been updated with None, in which case ALL the stores will also be non
    #no delete is called for
    if delete_email_id is None:
        return no_update
    
    #otherwise, a delete is neccesarily in order
    email = delete_email_id["email"]
    dag_id = delete_email_id["dag_id"]
    task_id = delete_email_id["task_id"]
    flag_id = delete_email_id.get("flag_id", "DEFAULT")
    recipient_DB.delete_recipient(email, dag_id, task_id, flag_id)

    new_children = []
    for email_button in current_task_email_buttons:
        #email_button SHOULD be dmc.Button component but just to make sure
        if email_button.get("type") == "Button":  # Only Buttons
            comp_id = email_button["props"]["id"]
            print("Button ID:", comp_id)
            if comp_id["user_id"] != delete_email_id["user_id"]:
                new_children.append(email_button)
        else:
            new_children.append(email_button)
    print("Triggered:", ctx.triggered_id)
    return new_children




#▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
######################Add Recipients###################################
#▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
@callback(
    Output("add-recipients-modal", "opened"),
    Output("task-container", "children"),
    Input("add-recipients-button", "n_clicks"),
    State("add-recipients-modal", "opened"),
    State("task-container", "children"),
    State("current-dag-id_store", "data"),
    prevent_initial_call=True
)
def open_add_recipients_modal(n_clicks, current_modal_state, main_children, dag_id):
    #if add recipients modal is currently open, that means it is about to be closed.
    #Therefore, want want to update the shown email recipients on the main page. 
    #Otherwise, if just opening the add recipients modal, no update is needed.
    if current_modal_state:
        main_children = populate_task_container(dag_id)
    #shows add recipient modal if hidden; hides if shown
    return not current_modal_state, main_children 

    


def populate_add_recipients_tasks_modal(dag_tasks:list[str]):
    new_buttons = dmc.Stack([
        dmc.Flex(
        [
            dmc.Checkbox(
                id={'type': 'task-checkbox', 'index': task},
                checked=False,
                radius="m",
                size="sm",
                style={"marginRight": "10px"}  # small space before button
            ),
            dmc.Button(
                task,
                id={'type': 'task-button', 'index': task},
                variant="subtle",
                fullWidth=True,  # takes remaining horizontal space
                justify="left",
                radius="md",
                style={"flex": 1}  # ensures it stretches next to the checkbox
            )
        ],
        align="center",  # vertical alignment
        gap="sm",        # horizontal spacing
        style={"width": "100%"}
    )
        for task in dag_tasks
    ], gap="xs", style={"width": "100%"})

    return new_buttons


@callback(
    Output({'type': 'task-checkbox', 'index': dash.MATCH}, 'checked'),
    Input({'type': 'task-button', 'index': dash.MATCH}, 'n_clicks'),
    State({'type': 'task-checkbox', 'index': dash.MATCH}, 'checked'),
    prevent_initial_call=True
)
def toggle_task_checkbox(n_clicks, current_check_state):
    return not current_check_state


@callback(
    #Output("add-emails-textarea", "error"),
    Output("email-badges-scrollarea","children"),
    Input("add-emails-textarea", "value"),
    prevent_initial_call=True
)
def add_users_textarea_update(text_value):
    children = []
    div = html.Div(children=[])
    email_dicts = strip_textarea_for_emails(text_value)
    status_colors = {"INVALID FORMAT":"red", "EMAIL EXISTS":"green", "EMAIL NONEXISTENT":"yellow"}
    for email_dict in email_dicts:
        email = email_dict["email"]
        status = email_dict["status"]
        badge = dmc.Badge(
            email,
            size="xl",
            radius="xl",
            variant="light",
            color=status_colors[status]
        )
        div.children.append(badge)

    info_badges = dmc.Group(
        [
            dmc.Badge(
                "VALID EMAIL, EXISTS IN DATABASE",
                size="s",
                radius="xl",
                variant="light",
                color=status_colors["EMAIL EXISTS"]
            ),
            dmc.Badge(
                "VALID EMAIL, BUT DOESN'T EXISTS IN DATABASE",
                size="s",
                radius="xl",
                variant="light",
                color=status_colors["EMAIL NONEXISTENT"]
            ),
            dmc.Badge(
                "INVALID FORMAT",
                size="s",
                radius="xl",
                variant="light",
                color=status_colors["INVALID FORMAT"]
            )
        ],
        justify="center",
        gap="md",
        grow=False,
        # other props...
    )
    children.append(info_badges)
    children.append(dmc.Space(h=10)) 
    children.append(dmc.Divider(variant="dashed"))
    children.append(dmc.Space(h=10)) 
    children.append(div)
    return children



def strip_textarea_for_emails(text_value:str)->list[dict]:
    '''
    Remove all single ' and double " quotes
    Split the string by commas
    Strip spaces from each item
    Return a list of dicts of the cleaned items. 
    Each dict contains string of cleaned email, and one of three magic strings to
    indicate the following:
        "INVALID FORMAT" - does not follow standard email format (one '@', one or more '.'s)
        "EMAIL EXISTS" - valid format and exists in database
        "EMAIL NONEXISTENT" - valid format but no user associated with email
    '''
    # 1. Remove all single and double quotes
    cleaned = text_value.replace('"', '').replace("'", "")
    # 2. Split by comma
    parts = cleaned.split(",")
    # 3. Strip whitespace and remove empty items

    email_list = [part.strip() for part in parts if part.strip()]


    validated_email_list = []
    for email in email_list:
        if email.count(".") == 0 or email.count("@") != 1:
            validated_email_list.append({"email":email,"status":"INVALID FORMAT"})
        else:
            #check if email exists in database
            if recipient_DB.does_user_exist_by_email(email):
                validated_email_list.append({"email":email,"status":"EMAIL EXISTS"})
            else:
                validated_email_list.append({"email":email,"status":"EMAIL NONEXISTENT"})

    return validated_email_list




@callback(
    Output({"button_type":"send_type_add_recipient","index":"to_"}, "variant"),
    Input({"button_type":"send_type_add_recipient","index":"to_"}, "n_clicks"),
    State({"button_type":"send_type_add_recipient","index":"to_"}, "variant"),
    State({"button_type":"send_type_add_recipient","index":"cc"}, "variant"),
    State({"button_type":"send_type_add_recipient","index":"bcc"}, "variant"),
    prevent_initial_call=True
)
def add_recipients_to_button(n_clicks, to_variant, cc_variant, bcc_variant):
    if to_variant == "outline":
        return "filled"
    elif cc_variant == "outline" and bcc_variant == "outline":
        return "filled" #same thing as returning dash.no_update; explicitly keep it outline
    else:
        return "outline"
    

@callback(
    Output({"button_type":"send_type_add_recipient","index":"cc"}, "variant"),
    Input({"button_type":"send_type_add_recipient","index":"cc"}, "n_clicks"),
    State({"button_type":"send_type_add_recipient","index":"to_"}, "variant"),
    State({"button_type":"send_type_add_recipient","index":"cc"}, "variant"),
    State({"button_type":"send_type_add_recipient","index":"bcc"}, "variant"),
    prevent_initial_call=True
)
def add_recipients_to_button(n_clicks, to_variant, cc_variant, bcc_variant):
    if cc_variant == "outline":
        return "filled"
    elif to_variant == "outline" and bcc_variant == "outline":
        return "filled" #same thing as returning dash.no_update; explicitly keep it outline
    else:
        return "outline"
    



@callback(
    Output({"button_type":"send_type_add_recipient","index":"bcc"}, "variant"),
    Input({"button_type":"send_type_add_recipient","index":"bcc"}, "n_clicks"),
    State({"button_type":"send_type_add_recipient","index":"to_"}, "variant"),
    State({"button_type":"send_type_add_recipient","index":"cc"}, "variant"),
    State({"button_type":"send_type_add_recipient","index":"bcc"}, "variant"),
    prevent_initial_call=True
)
def add_recipients_to_button(n_clicks, to_variant, cc_variant, bcc_variant):
    if bcc_variant == "outline":
        return "filled"
    elif cc_variant == "outline" and to_variant == "outline":
        return "filled" #same thing as returning dash.no_update; explicitly keep it outline
    else:
        return "outline"
    



#add users to the database
#closes modal by incrementing output which triggers "opened" attribute of modal to change
@callback(
    Output("add-recipients-button", "n_clicks"),
    Input("submit-new-emails-button","n_clicks"),
    State("add-emails-textarea", "value"),
    State({"button_type":"send_type_add_recipient","index":"to_"}, "variant"),
    State({"button_type":"send_type_add_recipient","index":"cc"}, "variant"),
    State({"button_type":"send_type_add_recipient","index":"bcc"}, "variant"),
    State({'type': 'task-checkbox', 'index': dash.ALL}, "id"),
    State({'type': 'task-checkbox', 'index': dash.ALL}, "checked"),
    State("current-dag-id_store", "data"),
    prevent_initial_call = True
)
def submit_new_recipients(n_clicks, inputemails_text, to_variant, cc_variant, bcc_variant, all_ids, all_checkmarks, dag_id):

    checked_task_ids = [id_["index"] for i, id_ in enumerate(all_ids) if all_checkmarks[i]] #get every task_id whose corresponding chechbox is ticked
    emails_dict = strip_textarea_for_emails(inputemails_text)
    new_recipients_list = []
    for email_dict in emails_dict:
        email = email_dict["email"]
        status = email_dict["status"]
        #skip to next email
        if status == "INVALID FORMAT":
            continue
        #create user for email if none exists
        elif status == "EMAIL NONEXISTENT":
            recipient_DB.add_user({"email":email}) #name defaults to "NONE"
        
        for task_id in checked_task_ids:
            new_recipient = {"to_":to_variant=="filled", "cc":cc_variant=="filled", "bcc":bcc_variant=="filled", "email":email, "task_id":task_id, "dag_id":dag_id}
            new_recipients_list.append(new_recipient)
    
    for p in new_recipients_list:
        print(p)
    recipient_DB.add_recipients_by_email_list(new_recipients_list)

    #this return will trigger add recipients modal to close
    return n_clicks + 1




#▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
######################     Add Recipients     ###################################
#▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲













