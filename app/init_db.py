from sqlalchemy import create_engine, text
from database import DynamicRecipientDB

# The name of your database file
DB_URL = "sqlite:///Dynamic_Emails.db"

# Create an engine to connect to the database
engine = create_engine(DB_URL)
rdDB = DynamicRecipientDB()


#resets the db to hard coded entries
if(True):
    # The SQL command to create the table
    # "IF NOT EXISTS" prevents errors if you run this script multiple times
    CLEAR_DB_SQL = "DROP TABLE IF EXISTS recipients;"
    CLEAR_DB_SQL_USERS = "DROP TABLE IF EXISTS users;"
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS recipients (
        user_id INTEGER,
        dag_id TEXT NOT NULL,
        task_id TEXT DEFAULT "DEFAULT",
        flag_id TEXT DEFAULT "DEFAULT",
        cc BOOL DEFAULT 0,
        bcc BOOL DEFAULT 0,
        to_ BOOL DEFAULT 0
    );
    """

    CREATE_USER_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT DEFAULT "DEFAULT"
    );
    """
    # Connect and execute the table creation command
    with engine.connect() as connection:
        print("Connecting to the database...")
        connection.execute(text(CLEAR_DB_SQL))
        connection.execute(text(CLEAR_DB_SQL_USERS))
        connection.execute(text(CREATE_TABLE_SQL))
        connection.execute(text(CREATE_USER_TABLE_SQL))
        print("Table 'dag_recipients' created successfully (if it didn't exist).")




    recipients_to_add = [
    # ── existing entries (left intact if DAG/task is outside your dag_JSON) ─────
 
 

    # ── BCG_Split updated to new task ids ──────────────────────────────────────
    {
        "user_id": 3,
        "dag_id": "BCG_Split",
        "task_id": "bcg_manifest_init",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 2,
        "dag_id": "BCG_Split",
        "task_id": "generate_bcg_counts",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": True,
        "to_": True
    },
    {
        "user_id": 2,
        "dag_id": "BCG_Split",
        "task_id": "partition_client_files",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },

    # ── 115_Daily_Performance_Email (unchanged task set) ───────────────────────
    {
        "user_id": 11,
        "dag_id": "115_Daily_Performance_Email",
        "task_id": "email_prep",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },

    # ── 407_Daily_Performance_Email updated ────────────────────────────────────
    {
        "user_id": 5,
        "dag_id": "407_Daily_Performance_Email",
        "task_id": "kpi_extract_407",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 5,
        "dag_id": "407_Daily_Performance_Email",
        "task_id": "email_store_mgrs_list",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },

    # ── 499_outbound_optimization_V2 updated ───────────────────────────────────
    {
        "user_id": 6,
        "dag_id": "499_outbound_optimization_V2",
        "task_id": "budget_allocator",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },

    # ── BCG_Split updated ──────────────────────────────────────────────────────
    {
        "user_id": 6,
        "dag_id": "BCG_Split",
        "task_id": "notify_bcg_distribution_list",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },

    # ── 436_Daily_Performance_Email updated ────────────────────────────────────
    {
        "user_id": 8,
        "dag_id": "436_Daily_Performance_Email",
        "task_id": "etl_merch_metrics_436",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 8,
        "dag_id": "436_Daily_Performance_Email",
        "task_id": "generate_variance_report",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },

    # ── 115_outbound_optimization_V2 updated ───────────────────────────────────
    {
        "user_id": 11,
        "dag_id": "115_outbound_optimization_V2",
        "task_id": "ad_spend_reallocator_v2_115",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 9,
        "dag_id": "115_outbound_optimization_V2",
        "task_id": "email_growth_marketing_list",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },

    # ── 499_Daily_Performance_Email updated ────────────────────────────────────
    {
        "user_id": 10,
        "dag_id": "499_Daily_Performance_Email",
        "task_id": "daily_perf_499_aggregate",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 10,
        "dag_id": "499_Daily_Performance_Email",
        "task_id": "detect_anomalies",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },

    # ── 712_Daily_Performance_Email updated ────────────────────────────────────
    {
        "user_id": 11,
        "dag_id": "712_Daily_Performance_Email",
        "task_id": "warehouse_ops_etl_712",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 11,
        "dag_id": "712_Daily_Performance_Email",
        "task_id": "email_warehouse_ops_list",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": True,
        "to_": False
    },

    # ── BCG_Split updated ──────────────────────────────────────────────────────
    {
        "user_id": 12,
        "dag_id": "BCG_Split",
        "task_id": "partition_client_files",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 12,
        "dag_id": "BCG_Split",
        "task_id": "s3_upload_bcg",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },

    # ── 499_outbound_optimization_V2 updated ───────────────────────────────────
    {
        "user_id": 4,
        "dag_id": "499_outbound_optimization_V2",
        "task_id": "email_outbound_team_list",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },

    # ── 407_Daily_Performance_Email updated ────────────────────────────────────
    {
        "user_id": 7,
        "dag_id": "407_Daily_Performance_Email",
        "task_id": "email_store_mgrs_list",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },

    # ── 712_Daily_Performance_Email updated ────────────────────────────────────
    {
        "user_id": 1,
        "dag_id": "712_Daily_Performance_Email",
        "task_id": "email_warehouse_ops_list",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },

    # ── 115_Daily_Performance_Email (unchanged task set) ───────────────────────
    {
        "user_id": 3,
        "dag_id": "115_Daily_Performance_Email",
        "task_id": "data_pull",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },

    # ── 115_outbound_optimization_V2 updated ───────────────────────────────────
    {
        "user_id": 2,
        "dag_id": "115_outbound_optimization_V2",
        "task_id": "segment_audience_build",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },

    # ── (second block begins here in your list) ────────────────────────────────
    # 115_Daily_Performance_Email (unchanged task set)
    {
        "user_id": 0,
        "dag_id": "115_Daily_Performance_Email",
        "task_id": "data_pull",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 1,
        "dag_id": "115_Daily_Performance_Email",
        "task_id": "email_prep",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },

    # 115_outbound_optimization_V2 updated
    {
        "user_id": 2,
        "dag_id": "115_outbound_optimization_V2",
        "task_id": "ad_spend_reallocator_v2_115",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 3,
        "dag_id": "115_outbound_optimization_V2",
        "task_id": "email_growth_marketing_list",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": True
    },

    # 407_Daily_Performance_Email updated
    {
        "user_id": 4,
        "dag_id": "407_Daily_Performance_Email",
        "task_id": "email_store_mgrs_list",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },

    # 436_Daily_Performance_Email updated
    {
        "user_id": 5,
        "dag_id": "436_Daily_Performance_Email",
        "task_id": "etl_merch_metrics_436",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 6,
        "dag_id": "436_Daily_Performance_Email",
        "task_id": "email_merchandising_list",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },

    # 499_Daily_Performance_Email updated
    {
        "user_id": 7,
        "dag_id": "499_Daily_Performance_Email",
        "task_id": "daily_perf_499_aggregate",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 8,
        "dag_id": "499_Daily_Performance_Email",
        "task_id": "attach_csv_exports",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },

    # 499_outbound_optimization_V2 updated
    {
        "user_id": 9,
        "dag_id": "499_outbound_optimization_V2",
        "task_id": "campaign_scoring_v2_499",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": True
    },
    {
        "user_id": 10,
        "dag_id": "499_outbound_optimization_V2",
        "task_id": "prepare_creative_snapshots",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },

    # 712_Daily_Performance_Email updated
    {
        "user_id": 11,
        "dag_id": "712_Daily_Performance_Email",
        "task_id": "warehouse_ops_etl_712",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 12,
        "dag_id": "712_Daily_Performance_Email",
        "task_id": "email_warehouse_ops_list",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": True,
        "to_": False
    },

    # BCG_Split updated
    {
        "user_id": 0,
        "dag_id": "BCG_Split",
        "task_id": "partition_client_files",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 1,
        "dag_id": "BCG_Split",
        "task_id": "s3_upload_bcg",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
    "user_id": 0,
    "dag_id": "115_outbound_optimization_V2",
    "task_id": "ad_spend_reallocator_v2_115",
    "flag_id": "DEFAULT",
    "cc": False,
    "bcc": False,
    "to_": True
    },
    {
        "user_id": 1,
        "dag_id": "115_outbound_optimization_V2",
        "task_id": "segment_audience_build",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 2,
        "dag_id": "115_outbound_optimization_V2",
        "task_id": "score_offers",
        "flag_id": "success",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 3,
        "dag_id": "115_outbound_optimization_V2",
        "task_id": "email_growth_marketing_list",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 4,
        "dag_id": "407_Daily_Performance_Email",
        "task_id": "kpi_extract_407",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 5,
        "dag_id": "407_Daily_Performance_Email",
        "task_id": "compile_dashboard_artifacts",
        "flag_id": "failure",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 6,
        "dag_id": "407_Daily_Performance_Email",
        "task_id": "email_store_mgrs_list",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 7,
        "dag_id": "436_Daily_Performance_Email",
        "task_id": "etl_merch_metrics_436",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 8,
        "dag_id": "436_Daily_Performance_Email",
        "task_id": "generate_variance_report",
        "flag_id": "success",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 9,
        "dag_id": "436_Daily_Performance_Email",
        "task_id": "email_merchandising_list",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 10,
        "dag_id": "499_Daily_Performance_Email",
        "task_id": "daily_perf_499_aggregate",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 11,
        "dag_id": "499_Daily_Performance_Email",
        "task_id": "detect_anomalies",
        "flag_id": "failure",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 12,
        "dag_id": "499_Daily_Performance_Email",
        "task_id": "attach_csv_exports",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 0,
        "dag_id": "499_Daily_Performance_Email",
        "task_id": "email_region_north_list",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 1,
        "dag_id": "499_outbound_optimization_V2",
        "task_id": "campaign_scoring_v2_499",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": True
    },
    {
        "user_id": 2,
        "dag_id": "499_outbound_optimization_V2",
        "task_id": "rank_channels",
        "flag_id": "success",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 3,
        "dag_id": "499_outbound_optimization_V2",
        "task_id": "budget_allocator",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 4,
        "dag_id": "499_outbound_optimization_V2",
        "task_id": "prepare_creative_snapshots",
        "flag_id": "failure",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 5,
        "dag_id": "499_outbound_optimization_V2",
        "task_id": "email_outbound_team_list",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 6,
        "dag_id": "712_Daily_Performance_Email",
        "task_id": "warehouse_ops_etl_712",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 7,
        "dag_id": "712_Daily_Performance_Email",
        "task_id": "pickpack_sla_summary",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 8,
        "dag_id": "712_Daily_Performance_Email",
        "task_id": "email_warehouse_ops_list",
        "flag_id": "success",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 9,
        "dag_id": "115_Daily_Performance_Email",
        "task_id": "data_pull",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 10,
        "dag_id": "115_Daily_Performance_Email",
        "task_id": "email_prep",
        "flag_id": "failure",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 11,
        "dag_id": "BCG_Split",
        "task_id": "bcg_manifest_init",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 12,
        "dag_id": "BCG_Split",
        "task_id": "generate_bcg_counts",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 0,
        "dag_id": "BCG_Split",
        "task_id": "partition_client_files",
        "flag_id": "success",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 1,
        "dag_id": "BCG_Split",
        "task_id": "s3_upload_bcg",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 2,
        "dag_id": "BCG_Split",
        "task_id": "notify_bcg_distribution_list",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": True,
        "to_": False
    }
]

    for recip in recipients_to_add:
        rdDB.add_recipient(recipient_dict=recip)
    for user in users_to_add:
        rdDB.add_user(user_dict=user)

print("\n\n\n--------------------Recipients----------------------")
print(rdDB.get_recipients())
print("\n\n\n--------------------Users----------------------")
print(rdDB.get_users())

# rdDB.get_recipients_by_dag_task("DAG ID 0","task id a")
