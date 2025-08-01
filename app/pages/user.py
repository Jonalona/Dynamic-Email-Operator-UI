import dash
from dash import html, dcc, callback, Input, Output, callback_context as ctx, State, no_update
from shared_dash import recipient_DB
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from global_vars import *
from pages.dag import show_emails_per_task_per_dag




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
