from sqlalchemy import create_engine, text
from database import DynamicRecipientDB

# The name of your database file
DB_URL = "sqlite:///recipients.db"

# Create an engine to connect to the database
engine = create_engine(DB_URL)
rdDB = DynamicRecipientDB()


#resets the db to hard coded entries
if(False):
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
        {
            "user_id":0,
            "dag_id": "DAG ID 0",
            "task_id":"task id a",
            "flag_id":"DEFAULT",
            "cc": False,
            "bcc": False,
            "to_": True  
        },
        {
            "user_id":1,
            "dag_id": "daily_sales_report",
            "task_id":"task id b",
            "flag_id":"failure",
            "cc": True, 
            "bcc": False,
            "to_": False
        },
        {
            "user_id":2,
            "dag_id": "weekly_marketing_update",
            "task_id":"task id c",
            "cc": False,
            "bcc": False,
            "to_": True
        },
        {
            "user_id":3,
            "dag_id": "BCG_Split",
            "task_id":"bcg_split_start",
            "flag_id": "DEFAULT",
            "cc": False,
            "bcc": True, 
            "to_": False
        },
        {
            "user_id":2,
            "dag_id": "BCG_Split",
            "task_id":"bcg_split_start",
            "flag_id": "DEFAULT",
            "cc": True,
            "bcc": True, 
            "to_": True
        },
        {
            "user_id":2,
            "dag_id": "BCG_Split",
            "task_id":"count_generator",
            "flag_id": "DEFAULT",
            "cc": False,
            "bcc": True, 
            "to_": False
        }
    ]

    users_to_add = [
        {
            "user_id":0,
            "name":"Jonah Reisner",
            "email":"jreisner@jetrord.com"
        },
            {
            "user_id":1,
            "name":"Aniket",
            "email":"aniket@aniket.com"
        },
            {
            "user_id":2,
            "name":"Usama Saifi",
            "email":"saifi@genericEmail.com"
        },
            {
            "user_id":3,
            "name":"Nishit",
            "email":"nishitjain@gmail.com"
        },
            {
            "user_id":4,
            "name":"Dr. Jie",
            "email":"doctorJie@gmail.com"
        },
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
