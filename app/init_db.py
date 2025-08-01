from sqlalchemy import create_engine, text
from database import DynamicRecipientDB

# The name of your database file
DB_URL = "sqlite:///recipients.db"

# Create an engine to connect to the database
engine = create_engine(DB_URL)
rdDB = DynamicRecipientDB()


#resets the db to hard coded entries
if(True):
    # The SQL command to create the table
    # "IF NOT EXISTS" prevents errors if you run this script multiple times
    CLEAR_DB_SQL = "DROP TABLE IF EXISTS email_recipients;"
    CLEAR_DB_SQL_USERS = "DROP TABLE IF EXISTS users;"
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS email_recipients (
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
        print("Table 'dag_email_recipients' created successfully (if it didn't exist).")




    recipients_to_add = [
    # ── existing entries ────────────────────────────────────────────────────────
    {
        "user_id": 0,
        "dag_id": "DAG ID 0",
        "task_id": "task id a",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 1,
        "dag_id": "daily_sales_report",
        "task_id": "task id b",
        "flag_id": "failure",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 2,
        "dag_id": "weekly_marketing_update",
        "task_id": "task id c",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 3,
        "dag_id": "Click_Me!",
        "task_id": "bcg_split_start",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 2,
        "dag_id": "Click_Me!",
        "task_id": "bcg_split_start",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": True,
        "to_": True
    },
    {
        "user_id": 2,
        "dag_id": "Click_Me!",
        "task_id": "count_generator",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 11,
        "dag_id": "115_Daily_Performance_Email",
        "task_id": "email_prep",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 5,
        "dag_id": "407_Daily_Performance_Email",
        "task_id": "data_pull",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 5,
        "dag_id": "407_Daily_Performance_Email",
        "task_id": "email_prep",
        "flag_id": "failure",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 6,
        "dag_id": "499_outbound_optimization_V2",
        "task_id": "prepare_email",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 6,
        "dag_id": "Click_Me!",
        "task_id": "success_emailer",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },

    # ── 15 new recipient entries ────────────────────────────────────────────────
    {
        "user_id": 8,
        "dag_id": "436_Daily_Performance_Email",
        "task_id": "data_pull",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 8,
        "dag_id": "436_Daily_Performance_Email",
        "task_id": "email_prep",
        "flag_id": "failure",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 11,
        "dag_id": "115_outbound_optimization_V2",
        "task_id": "pull_and_process",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 9,
        "dag_id": "115_outbound_optimization_V2",
        "task_id": "prepare_email",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 10,
        "dag_id": "499_Daily_Performance_Email",
        "task_id": "data_pull",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 10,
        "dag_id": "499_Daily_Performance_Email",
        "task_id": "email_prep",
        "flag_id": "failure",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 11,
        "dag_id": "712_Daily_Performance_Email",
        "task_id": "data_pull",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 11,
        "dag_id": "712_Daily_Performance_Email",
        "task_id": "email_prep",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 12,
        "dag_id": "Click_Me!",
        "task_id": "split_all_files",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 12,
        "dag_id": "Click_Me!",
        "task_id": "remove_og_files",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 4,
        "dag_id": "499_outbound_optimization_V2",
        "task_id": "prepare_email",
        "flag_id": "success",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 7,
        "dag_id": "407_Daily_Performance_Email",
        "task_id": "email_prep",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 1,
        "dag_id": "712_Daily_Performance_Email",
        "task_id": "email_prep",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 3,
        "dag_id": "115_Daily_Performance_Email",
        "task_id": "data_pull",
        "flag_id": "failure",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 2,
        "dag_id": "115_outbound_optimization_V2",
        "task_id": "prepare_email",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },
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
        "flag_id": "success",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 2,
        "dag_id": "115_outbound_optimization_V2",
        "task_id": "pull_and_process",
        "flag_id": "failure",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 3,
        "dag_id": "115_outbound_optimization_V2",
        "task_id": "prepare_email",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 4,
        "dag_id": "407_Daily_Performance_Email",
        "task_id": "email_prep",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 5,
        "dag_id": "436_Daily_Performance_Email",
        "task_id": "data_pull",
        "flag_id": "failure",
        "cc": True,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 6,
        "dag_id": "436_Daily_Performance_Email",
        "task_id": "email_prep",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 7,
        "dag_id": "499_Daily_Performance_Email",
        "task_id": "data_pull",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 8,
        "dag_id": "499_Daily_Performance_Email",
        "task_id": "email_prep",
        "flag_id": "failure",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 9,
        "dag_id": "499_outbound_optimization_V2",
        "task_id": "pull_and_process",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": True
    },
    {
        "user_id": 10,
        "dag_id": "499_outbound_optimization_V2",
        "task_id": "prepare_email",
        "flag_id": "success",
        "cc": True,
        "bcc": False,
        "to_": False
    },
    {
        "user_id": 11,
        "dag_id": "712_Daily_Performance_Email",
        "task_id": "data_pull",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": False,
        "to_": True
    },
    {
        "user_id": 12,
        "dag_id": "712_Daily_Performance_Email",
        "task_id": "email_prep",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 0,
        "dag_id": "Click_Me!",
        "task_id": "split_all_files",
        "flag_id": "DEFAULT",
        "cc": False,
        "bcc": True,
        "to_": False
    },
    {
        "user_id": 1,
        "dag_id": "Click_Me!",
        "task_id": "compressor",
        "flag_id": "DEFAULT",
        "cc": True,
        "bcc": False,
        "to_": False
    }

    ]

    users_to_add = [
    # ── existing users ──────────────────────────────────────────────────────────
    {
    "user_id": 0,
    "name": "Jon Snow",
    "email": "jonsnow@winterfell.com"
    },
    {
        "user_id": 1,
        "name": "Daenerys Targaryen",
        "email": "daenerys@dragonstone.com"
    },
    {
        "user_id": 2,
        "name": "Tyrion Lannister",
        "email": "tyrion@casterlyrock.com"
    },
    {
        "user_id": 3,
        "name": "Arya Stark",
        "email": "arya@winterfell.com"
    },
    {
        "user_id": 4,
        "name": "Cersei Lannister",
        "email": "cersei@kingslanding.com"
    },
    {
        "user_id": 5,
        "name": "Sansa Stark",
        "email": "sansa@winterfell.com"
    },
    {
        "user_id": 6,
        "name": "Jaime Lannister",
        "email": "jaime@casterlyrock.com"
    },
    {
        "user_id": 7,
        "name": "Bran Stark",
        "email": "bran@winterfell.com"
    },
    {
        "user_id": 8,
        "name": "Brienne of Tarth",
        "email": "brienne@tarth.com"
    },
    {
        "user_id": 9,
        "name": "Jorah Mormont",
        "email": "jorah@mormont.com"
    },
    {
        "user_id": 10,
        "name": "Samwell Tarly",
        "email": "samwell@oldtown.com"
    },
    {
        "user_id": 11,
        "name": "Theon Greyjoy",
        "email": "theon@i\u0335r\u0335o\u0335n\u0335i\u0335s\u0335l\u0335a\u0335n\u0335d\u0335s\u0335winterfell.com"
    },
    {
        "user_id": 12,
        "name": "Melisandre",
        "email": "melisandre@redtemple.com"
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
