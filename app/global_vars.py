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
    "115_Daily_Performance_Email": ["data_pull", "email_prep"],  # unchanged

    "115_outbound_optimization_V2": [
        "ad_spend_reallocator_v2_115",
        "segment_audience_build",
        "score_offers",
        "email_growth_marketing_list"
    ],
    "407_Daily_Performance_Email": [
        "kpi_extract_407",
        "compile_dashboard_artifacts",
        "email_store_mgrs_list"
    ],
    "436_Daily_Performance_Email": [
        "etl_merch_metrics_436",
        "generate_variance_report",
        "email_merchandising_list"
    ],
    "499_Daily_Performance_Email": [
        "daily_perf_499_aggregate",
        "detect_anomalies",
        "attach_csv_exports",
        "email_region_north_list"
    ],
    "499_outbound_optimization_V2": [
        "campaign_scoring_v2_499",
        "rank_channels",
        "budget_allocator",
        "prepare_creative_snapshots",
        "email_outbound_team_list"
    ],
    "712_Daily_Performance_Email": [
        "warehouse_ops_etl_712",
        "pickpack_sla_summary",
        "email_warehouse_ops_list"
    ],
    "BCG_Split": [
        "bcg_manifest_init",
        "generate_bcg_counts",
        "partition_client_files",
        "s3_upload_bcg",
        "notify_bcg_distribution_list"
    ]
}


ALL_DAGS = list(dag_JSON.keys())
