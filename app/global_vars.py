to_bg_color = '#0d6efd'
cc_bg_color = "#00695C"
bcc_bg_color = "#A695B6"
no_bg_color = "rgba(37, 150, 190,0.1)"
delete_bg_color = "rgb(245, 135, 145)"

dag_JSON = {
    "115_Daily_Performance_Email":["data_pull","email_prep"],
    "115_outbound_optimization_V2":["pull_and_process","prepare_email"],
    "407_Daily_Performance_Email":["data_pull","email_prep"],
    "436_Daily_Performance_Email":["data_pull","email_prep"],
    "499_Daily_Performance_Email":["data_pull","email_prep"],
    "499_outbound_optimization_V2":["pull_and_process","prepare_email"],
    "712_Daily_Performance_Email":["data_pull","email_prep"],
    "Click Me!":["bcg_split_start","remove_previous_upload","count_generator","split_all_files","compressor","uploader","remove_og_files","success_emailer"]
}


ALL_DAGS = list(dag_JSON.keys())
