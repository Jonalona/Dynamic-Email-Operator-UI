from sqlalchemy import create_engine, text
from typing import Dict

class DynamicRecipientDB():
    """
    DynamicRecipientDB provides a simple, SQLAlchemy‐backed interface for
    managing email recipients and users in your application. It connects to
    a SQLite database by default. But very easy to use any other sqlalchemy supported
    databases by simply explicitly passing in db_url. 
    There are two tables in the database, `users` and `recipients`—
    and exposes methods to add, remove, update, and query both users and their
    email‐recipient relationships across DAGs and tasks. By encapsulating all
    the SQL logic (including deduplication checks, join queries, and batch
    operations) behind a clean Python API, it lets the rest of your code focus
    on business rules and UI, rather than hand‐crafting SQL each time.
    """
    def __init__(self, db_url:str = "sqlite:///Dynamic_Emails.db", echo=False):
        self.db_url = db_url
        self.engine = create_engine(db_url, echo=echo)
        self.create_schema_if_missing()

    def get_emails_by_send_type(self, dag_id: str, task_id: str, flag_id: str = "DEFAULT") -> Dict[str, list]:
        """
        Returns a dict with keys 'cc', 'bcc', and 'to_' mapping to lists of
        email addresses for recipients who have that send‐type flag set to True
        for the given dag/task/flag.
        """
        sql = text("""
            SELECT u.email, er.cc, er.bcc, er.to_
            FROM recipients AS er
            JOIN users AS u
              ON u.user_id = er.user_id
            WHERE er.dag_id = :dag_id
              AND er.task_id = :task_id
              AND er.flag_id = :flag_id
        """)
        # initialize empty lists
        emails_by_type = {"cc": [], "bcc": [], "to_": []}

        with self.engine.connect() as conn:
            result = conn.execute(sql, {
                "dag_id": dag_id,
                "task_id": task_id,
                "flag_id": flag_id
            })
            for row in result:
                email = row.email.lower()
                if row.cc:
                    emails_by_type["cc"].append(email)
                if row.bcc:
                    emails_by_type["bcc"].append(email)
                if row.to_:
                    emails_by_type["to_"].append(email)

        return emails_by_type

    def create_schema_if_missing(self):
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
        with self.engine.connect() as connection:
            print("Connecting to database and initializing schemas if missing...")
            connection.execute(text(CREATE_TABLE_SQL))
            connection.execute(text(CREATE_USER_TABLE_SQL))
    
    #returns every recipient in 'recipients' table
    def get_recipients(self, dag_id:str=None, task_id:str=None):
        with self.engine.connect() as connected:
            result = connected.execute(
                text("SELECT user_id, dag_id, task_id, flag_id, cc, bcc, to_ FROM recipients")
            )
            # Your code is the same whether it's SQLite or Postgres!
            return [row for row in result]
    
    #returns every user in 'users' table
    def get_users(self):
        with self.engine.connect() as connected:
            result = connected.execute(
                text("SELECT user_id, name, email FROM users")
            )
            return [row._mapping for row in result]
    
    #adds a recipient into the 'recipients' table
    def add_recipient(self, recipient_dict: dict):
        """Adds a new recipient if it doesn't already exist."""
        dag_id = recipient_dict["dag_id"]
        user_id = recipient_dict["user_id"]
        task_id = recipient_dict.get("task_id") or "DEFAULT"
        cc = recipient_dict.get("cc") or 0
        bcc = recipient_dict.get("bcc") or 0
        to_ = recipient_dict.get("to_") or 0
        flag_id = recipient_dict.get("flag_id") or "DEFAULT"

        with self.engine.connect() as connected:
            # Check if the recipient already exists for the same dag/task/flag
            existing = connected.execute(
                text("""
                    SELECT COUNT(1)
                    FROM recipients
                    WHERE user_id = :user_id
                    AND dag_id = :dag_id
                    AND task_id = :task_id
                    AND flag_id = :flag_id
                """),
                {"user_id": user_id, "dag_id": dag_id, "task_id": task_id, "flag_id": flag_id}
            ).scalar()

            if existing == 0:  # Only insert if no existing entry
                connected.execute(
                    text("""
                        INSERT INTO recipients
                        (user_id, dag_id, task_id, flag_id, cc, bcc, to_)
                        VALUES (:user_id, :dag_id, :task_id, :flag_id, :cc, :bcc, :to_)
                    """),
                    {
                        "user_id": user_id, "dag_id": dag_id, "task_id": task_id,
                        "flag_id": flag_id, "cc": cc, "bcc": bcc, "to_": to_
                    }
                )
                connected.commit()
                return True

            return False

    def delete_recipient(self, email: str, dag_id: str, task_id: str, flag_id: str = "DEFAULT") -> bool:
        """
        Deletes a recipient from the recipients table based on the user's email,
        dag_id, task_id, and (optional) flag_id.

        Returns:
            True if a row was deleted, False otherwise.
        """
        with self.engine.connect() as conn:
            # Normalize the email
            email = email.lower()

            # Step 1: Find the user_id for this email
            user_row = conn.execute(
                text("SELECT user_id FROM users WHERE email = :email"),
                {"email": email}
            ).fetchone()

            if not user_row:
                # No user found with that email
                return False

            user_id = user_row.user_id

            # Step 2: Delete the recipient entry
            result = conn.execute(
                text("""
                    DELETE FROM recipients
                    WHERE user_id = :user_id
                    AND dag_id = :dag_id
                    AND task_id = :task_id
                    AND flag_id = :flag_id
                """),
                {
                    "user_id": user_id,
                    "dag_id": dag_id,
                    "task_id": task_id,
                    "flag_id": flag_id
                }
            )

            conn.commit()
            return result.rowcount > 0

   
    def add_user(self, user_dict):
        """
        Tries to add a user.  Returns:
          - "Email Already Exists"   if the email is already in the table (no insert)
          - "Name Already Exists"    if the name is already in the table (still INSERT)
          - "User added successfully" if neither exists (INSERT)
        """
        if user_dict.get("name") == None:
            user_dict["name"] = "NONE"

        #make email lowercase
        user_dict["email"] = user_dict["email"].lower()

        with self.engine.connect() as conn:
            # 1) Check email first (highest precedence)
            email_exists = conn.execute(
                text("SELECT COUNT(1) FROM users WHERE email = :email"),
                {"email": user_dict["email"].lower()}
            ).scalar() > 0

            if email_exists:
                return "Email Already Exists"

            # 2) Check name next
            name_exists = conn.execute(
                text("SELECT COUNT(1) FROM users WHERE name = :name"),
                {"name": user_dict["name"]}
            ).scalar() > 0

            # 3) Insert the row
            conn.execute(
                text("INSERT INTO users (name, email) VALUES (:name, :email)"),
                user_dict
            )
            conn.commit()

            if name_exists:
                return "Name Already Exists"
            
            return "User Added Successfully"
        

    def delete_user(self, email):
        """
        Deletes a user by email. Returns:
        - "User Not Found"            if there was no user with that email (no DELETE)
        - "User Deleted Successfully" if the row was deleted
        """
        with self.engine.connect() as conn:
            # 1) Check that the user exists
            exists = conn.execute(
                text("SELECT COUNT(1) FROM users WHERE email = :email"),
                {"email": email}
            ).scalar() > 0

            if not exists:
                return "User Not Found"

            # 2) Delete the row
            result = conn.execute(
                text("DELETE FROM users WHERE email = :email"),
                {"email": email}
            )
            conn.commit()

            return "User Deleted Successfully"


    def does_user_exist_by_email(self, email: str) -> bool:
        """
        Returns True if a user exists with the given email, False otherwise.
        """

        with self.engine.connect() as conn:
            email_exists = conn.execute(
                text("SELECT COUNT(1) FROM users WHERE email = :email"),
                {"email": email.lower()}
            ).scalar() > 0

        return email_exists

    #gets the singular recipient from recipients table with matching dag,task,flag, and user ids
    def get_recipient_by_dag_task_flag_user(self, id_dict:dict):
        assert(type(id_dict) is dict)

        with self.engine.connect() as connected:
            sql_query = text("""
                SELECT
                    u.user_id,  -- Get the user's ID
                    u.email,          -- Get the user's email from the 'users' table
                    u.name,           -- Get the user's name
                    er.cc,            -- Get the cc flag from the 'recipients' table
                    er.bcc,           -- Get the bcc flag
                    er.to_,            -- Get the to_ flag
                    er.dag_id,
                    er.task_id,
                    er.flag_id
                FROM
                    recipients AS er
                JOIN
                    users AS u ON er.user_id = u.user_id
                WHERE
                    er.dag_id = :dag_id
                    AND er.task_id = :task_id
                    AND er.flag_id = :flag_id
                    AND er.user_id = :user_id;
            """)
            result = connected.execute(sql_query, id_dict)
            rows = result.fetchall()

            user_id = id_dict["user_id"]
            dag_id = id_dict["dag_id"]
            task_id = id_dict["task_id"]
            flag_id = id_dict["flag_id"]
            if len(rows) == 1:
                return dict(rows[0]._mapping)
            elif len(rows) == 0:
                # Handle the case where no records are found
                raise ValueError(f"No match for user_id: {user_id}, dag_id: {dag_id}, task_id: {task_id}, flag_id: {flag_id}")
            else:
                # Handle the case where multiple records are found, which probably indicate a data integrity issue...
                raise ValueError(f"Expected 1 record but found {len(rows)} for user_id: {user_id}, dag_id: {dag_id}, task_id: {task_id}, flag_id: {flag_id}")
    
    #For a given dag_id, task_id, return every recipient
    def get_recipients_by_dag_task(self, dag_id, task_id):
        with self.engine.connect() as connected:
            id_dict = {"dag_id":dag_id,"task_id":task_id}
            # This single query replaces both of your original queries.
            sql_query = text("""
                SELECT
                    u.user_id,  -- Get the user's ID
                    u.email,          -- Get the user's email from the 'users' table
                    u.name,           -- Get the user's name
                    er.cc,            -- Get the cc flag from the 'recipients' table
                    er.bcc,           -- Get the bcc flag
                    er.to_,            -- Get the to_ flag
                    er.dag_id,
                    er.task_id,
                    er.flag_id
                FROM
                    recipients AS er
                JOIN
                    users AS u ON er.user_id = u.user_id
                WHERE
                    er.dag_id = :dag_id
                    AND er.task_id = :task_id;
            """)
            
            # Execute the single, efficient query
            result = connected.execute(sql_query, id_dict)

            return [{"user_id":row.user_id, "name":row.name,"email":row.email,"to_":row.to_,"cc":row.cc,"bcc":row.bcc,
                     "task_id":row.task_id,"dag_id":row.dag_id,"flag_id":row.flag_id} for row in result]


    def add_recipients_by_email_list(self, emails: list[dict]) -> list[bool]:
        """
        Adds multiple recipients based on a list of dicts like:
        {
            "email": str,
            "cc": bool,
            "bcc": bool,
            "to_": bool,
            "dag_id":str,
            "task_id": str,
            "flag_id": str (optional)
        }

        Returns:
            list[bool]: True if successfully added, False if failed.
        """
        results = []

        with self.engine.connect() as conn:
            for email_dict in emails:
                email = email_dict["email"].lower()
                task_id = email_dict["task_id"]
                flag_id = email_dict.get("flag_id", "DEFAULT")
                dag_id = email_dict["dag_id"]
                # 1) Look up the user
                user_row = conn.execute(
                    text("SELECT user_id, name FROM users WHERE email = :email"),
                    {"email": email}
                ).fetchone()

                if not user_row:
                    # Email not found in users table
                    raise ValueError(f"No user found with email: {email}")

                user_id = user_row.user_id

                # 2) Build recipient dict
                recipient_dict = {
                    "user_id": user_id,
                    "dag_id": dag_id,  # or pass dag_id dynamically
                    "task_id": task_id,
                    "flag_id": flag_id,
                    "cc": email_dict["cc"],
                    "bcc": email_dict["bcc"],
                    "to_": email_dict["to_"],
                }

                # 3) Try inserting into recipients
                try:
                    self.add_recipient(recipient_dict)
                    results.append(True)
                except Exception as e:
                    print(f"Error adding recipient for {email}: {e}")
                    results.append(False)

        return results

        

    def update_recipient_send_type(self, id_dict:dict, send_type:str):
        dag_id = id_dict["dag_id"]
        task_id = id_dict["task_id"]
        user_id = id_dict["user_id"]
        flag_id = id_dict.get("flag_id","DEFAULT")
        
        current_state = self.get_recipient_send_types(user_id,dag_id,task_id,flag_id) #3 bool dict corresponding to to_,cc,bcc

        cc = (send_type == "cc") ^ current_state["cc"]
        bcc = (send_type == "bcc") ^ current_state["bcc"]
        to_ = (send_type == "to_") ^ current_state["to_"]
        with self.engine.connect() as connected:
            
            connected.execute(
                text("UPDATE recipients SET to_ = :to_, cc = :cc, bcc = :bcc WHERE user_id = :user_id AND dag_id = :dag_id AND task_id = :task_id AND flag_id = :flag_id"),
                {"dag_id": dag_id, "task_id":task_id, "flag_id":flag_id, "cc":cc, "bcc":bcc, "to_":to_,"user_id":user_id}
            )
            connected.commit()

    
    def get_recipient_send_types(self, user_id: int, dag_id: str, task_id: str, flag_id: str = "DEFAULT") -> Dict[str, bool]:
        """
        Retrieves the send types (to_, cc, bcc) for a single recipient.

        Args:
            user_id: The user's ID.
            dag_id: The DAG ID.
            task_id: The Task ID.
            flag_id: The optional Flag ID (defaults to "DEFAULT").

        Returns:
            A dictionary like {'to_': True, 'cc': False, 'bcc': False} if a record
            is found, otherwise returns None.
        """
        with self.engine.connect() as connected:
            # Define the SELECT query using text() for consistency
            sql_query = text(
                "SELECT to_, cc, bcc FROM recipients WHERE user_id = :user_id AND dag_id = :dag_id AND task_id = :task_id AND flag_id = :flag_id"
            )
            
            # Prepare the parameters for the query
            params = {
                "user_id": user_id,
                "dag_id": dag_id,
                "task_id": task_id,
                "flag_id": flag_id
            }
            
            result = connected.execute(sql_query, params)
            
            # Fetch the first (and hopefully only...) row from the result
            rows = result.fetchall()
        
            # Now, perform your check on the list of rows
            if len(rows) == 1:
                # The 'row' object is a SQLAlchemy Row. We can convert it to a
                # dictionary. The `_mapping` property is the underlying dict.
                return dict(rows[0]._mapping)
            elif len(rows) == 0:
                # Handle the case where no records are found
                raise ValueError(f"No match for user_id: {user_id}, dag_id: {dag_id}, task_id: {task_id}, flag_id: {flag_id}")
            else:
                # Handle the case where multiple records are found, which might indicate a data integrity issue
                raise ValueError(f"Expected 1 record but found {len(rows)} for user_id: {user_id}, dag_id: {dag_id}, task_id: {task_id}, flag_id: {flag_id}")

#WIP: idea was to use this in the custom EmailOperator class which should have read only permissions.
#dangerous to expose DynamicRecipientDB's write functionality when it's not neccessary
class DynamicRecipientFetcher():
    def __init__(self, db_url:str = "sqlite:///Dynamic_Emails.db"):
        self.dynamicRecipients = DynamicRecipientDB(db_url)
    
    
    