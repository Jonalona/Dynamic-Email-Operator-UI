from database import DynamicRecipientDB
recipient_DB = DynamicRecipientDB()

to_bg_color = '#0d6efd'
cc_bg_color = "#00695C"
bcc_bg_color = "#A695B6"
no_bg_color = "rgba(37, 150, 190,0.1)"
delete_bg_color = "rgb(245, 135, 145)"


"""
dag_JSON (and by extension ALL_DAGS) should really be pulling the dag information from API
within the Airflow server. This API already exists within a custom python file, but is not
yet in the server so can't be acccessed.
Find this file in 'airflow-server-plugins/Dag_Info_API_PlugIn.py'
"""
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


ALL_DAGS = list(dag_JSON.keys())
