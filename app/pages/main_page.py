import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from reusable_components import create_new_user_component, create_view_users_button
# Assume ALL_STATES is your list of DAG IDs
ALL_STATES = [
    "115_Daily_Performance_Email", "115_outbound_optimization_V2",
    "407_Daily_Performance_Email", "436_Daily_Performance_Email",
    "499_Daily_Performance_Email", "499_outbound_optimization_V2",
    "712_Daily_Performance_Email", "BCG_Split", "Another_Example_DAG",
    "Some_Really_Long_DAG_Name_To_Test_UI"
]

dash.register_page(__name__, path='/', name="Home") # Example registration

def layout():
    # Use dmc.Paper to create a styled container with a shadow
    return dmc.Container(
        [
            create_new_user_component(),
            create_view_users_button(),
            dmc.Paper(
                # dmc.Stack provides clean vertical spacing between its children
                dmc.Stack(
                    [
                        dmc.Title("DAG IDs", order=2),
                        dmc.TextInput(
                            id="filter-input",
                            placeholder="Type to filter DAGs...",
                            # Add a nice search icon
                            
                            radius="xl", # Pill-shaped
                        ),
                        # dmc.ScrollArea is the Mantine way to handle scrollable content
                        dmc.ScrollArea(
                            h="55vh", # height
                            id="button-container",
                            # Children will be populated by the callback
                        ),
                    ],
                    # Controls the space between the Title, TextInput, and ScrollArea
                ),
                p="lg",        # Padding inside the paper
                shadow="lg",   # Give it a nice shadow
                withBorder=True,
            )
        ],
        size="md",     # Controls the max-width of the container
        pt="5vh",      # Padding-top to move it down from the top of the viewport
    )

# Callback to update the list of buttons based on the filter
@callback(
    Output('button-container', 'children'),
    Input('filter-input', 'value')
)
def update_button_list(filter_value):
    if not filter_value:
        filtered_labels = ALL_STATES
    else:
        filtered_labels = [label for label in ALL_STATES if filter_value.lower() in label.lower()]

    if not filtered_labels:
        return dmc.Text("No DAGs found.", c="dimmed", p="lg")

    # Generate a list of dmc.Buttons inside a dmc.Stack
    new_buttons = dmc.Stack([
        dmc.Button(
            label,
            id={'type': 'dynamic-button', 'index': label},
            # "subtle" or "light" variants look great in a list
            variant="subtle",
            fullWidth=True, # Makes the button take up the full width
            justify="center", # Centers the text in the button
            radius="md"
        ) for label in filtered_labels
    ]) # Small spacing between buttons in the list
    
    return new_buttons

# This callback remains unchanged! It will work perfectly with the new dmc.Buttons.
@callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input({'type': 'dynamic-button', 'index': dash.ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def display_output(n_clicks):
    if not any(n_clicks):
        raise dash.exceptions.PreventUpdate

    triggered_id = dash.callback_context.triggered_id
    button_label = triggered_id['index']
    return f'/dags/{button_label}'