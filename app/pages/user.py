import dash
from dash import html, dcc, callback, Input, Output, callback_context as ctx, State, no_update
from shared_dash import recipient_DB
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from global_vars import *


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


def show_emails_per_task_per_dag(dag_id, dag_tasks, email_filter_str=None):

    """
    This function is called by Dash whenever a user navigates to a URL
    matching the path_template.
    """

        
    all_tasks_stack = dmc.Stack(
        [
        
            # Example: A placeholder for a graph
            dmc.ScrollArea(
                p="md",    # Corresponds to padding: '10px'
                style={"border": "1px solid #ccc"},  
                id='task-container',
                children=populate_task_container(dag_id, email_filter_str)
            ),

        ],
        id="all_tasks_stack"
    )


    #if there's an email filter, we're showing a lot of these below containers.
    #ids were not implemented with dynmaic calls in mind, so no selection/option features. Very simple only
    if email_filter_str is not None:
        return dmc.Container(
            [
                dmc.Title(f"Details for DAG: {dag_id}", order=1),
                all_tasks_stack
            ],
            size="fluid",
            bg="var(--mantine-color-blue-light)",
            id="main_container_dag",
        )
    

def populate_task_container(dag_id, email_filter_str = None):
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
                #if email_Filter is explicitly passed in then only add a recipient if it's email matches up with the filter
                if email_filter_str is not None and recipient["email"] != email_filter_str:
                    continue
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

dash.register_page(__name__, path_template="/user/<email>")


#▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
######################    Layout    ###################################
#▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼

# Define the layout as a FUNCTION.
# Dash will automatically pass the value captured from the URL
# into the argument with the same name (dag_id).
def layout(email):
    email = email.lower()
    all_users = recipient_DB.get_users()
    email_exists = any(user["email"]==email for user in all_users)
    if not email_exists: 
        return return_error_page(email)

    #all dags, and all tasks, but only showing emails matching parameter 'email'
    all_dags_all_tasks_filtered_containers = []
    for dag_id in ALL_DAGS:
        try:
            dag_tasks = dag_JSON[dag_id]
            all_dags_all_tasks_filtered_containers.append(show_emails_per_task_per_dag(dag_id, dag_tasks, email))
        except KeyError:
            print("ERRORORROROROR")
            pass
    
    print(f"LENGTH OF all_dags_all_tasks_filtered_containers: {len(all_dags_all_tasks_filtered_containers)}")

    
    # Link to go back home
    home_link = dmc.Anchor(

        href="/",
        # dmc.Group is used to add an icon next to the text
        children=dmc.Group([
            DashIconify(icon="feather:arrow-left"),
            "Go back to Home"
        ])
    )
    all_dags_all_tasks_filtered_containers.append(home_link)
    all_dags_stack = dmc.ScrollArea(
        children = all_dags_all_tasks_filtered_containers,
        p="md",    # Corresponds to padding: '10px'
        style={"border": "1px solid #ccc"},
    )
    #package everything together and return it
    return dmc.Container(
        children=all_dags_all_tasks_filtered_containers,
        size="fluid",
        bg="var(--mantine-color-blue-light)",
        style={"height": "100%","flex":1   },
        id="main_container_dag",
    )


def return_error_page(email):
    return dmc.Center(
            children=[
                dmc.Text(
                    f"Email '{email}' does not exist",
                    variant="gradient",
                    gradient={"from": "red", "to": "yellow", "deg": 45},
                    style={"fontSize": 40},
                )
            ]
        )
     
#▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
######################    Layout    ###################################
#▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
