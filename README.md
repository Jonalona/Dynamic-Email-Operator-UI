# Dynamic Email Operator UI
**Jonah Reisner**

A full-stack tool that lets non-engineers manage automated email alerts through a web interface. No code changes, no redeploys, no downtime.

**🚀 Try it live:** https://dynamic-email-operator-ui.onrender.com/

Both the web app and its database run on Render, so any changes you make persist and are visible to other visitors. Feel free to click around.

---

## The Problem

Large companies run automated data pipelines (using a tool called **Apache Airflow**) that send status emails: "the nightly report finished," "this job failed," and so on.

The catch is that the list of people who receive each email is written directly into the pipeline's source code. So a request as simple as *"add the new analyst to the failure alerts"* required:

1. An engineer to edit code
2. A code review
3. A redeploy of the production system. Which often had to wait until 3 AM, when no jobs were running.

A five-second change turned into a multi-day ticket that only a developer could close.

## The Solution

I moved the recipient lists out of the code and into a database, then built a web interface on top of it. Now an operations person picks a pipeline, picks a task, and edits the To/CC/BCC lists in a browser. The next email goes to the updated list automatically.

**Result:** a task that took days and required an engineer now takes seconds and requires nobody technical.

---

## What I Built

Four components, all written from scratch and designed to work together:

| Component | What it does |
|---|---|
| **Custom email operator** | A drop-in replacement for Airflow's built-in email tool. Instead of reading recipients from code, it looks them up in the database at send time. Migrating an existing pipeline is a one-line change. |
| **Database layer** | Stores users and per-task recipient rules. Creates its own tables on first run, so there's no manual setup. Works with SQLite out of the box and swaps to Postgres or MySQL by changing a single line. |
| **Airflow API plugin** | Exposes a live, read-only view of which pipelines and tasks exist, so the UI always shows real, current data without being given access to Airflow's internals. |
| **Web interface** | A multi-page app where users search pipelines, view current recipients, and add or remove people through modals and checkboxes. Built for people who have never seen a terminal. |

## Architecture

![System architecture](architecture%20overview/system%20architecture.png)

Each piece talks to the others through simple, well-defined interfaces, so any one of them can be swapped or extended without touching the rest.

The whole system is containerized. A `Dockerfile` and `docker-compose.yml` package the app and its database into a reproducible environment that runs identically on a laptop and in the cloud, which is how the live demo above is deployed. Setup is a single command.

## Technologies Used

**Python 3.12** · **Apache Airflow** · **Dash** (web framework) · **Dash Mantine Components** · **Flask Blueprints** · **SQLAlchemy** (database) · **Docker & Docker Compose** (deployment) · **Render** (hosting)

## Skills Demonstrated

- Extending a production workflow engine with custom operators and plugins
- Database design and ORM work
- REST API design
- Front-end development and UX for non-technical users
- Containerization and cloud deployment
- Identifying an operational bottleneck and designing the full system to remove it

---

# For Engineers

## Implementation Notes

### `DynamicRecipientsEmailOperator`

Subclasses Airflow's `EmailOperator`. At runtime it reads its own `dag_id` and `task_id` out of the execution context rather than taking them as arguments, then queries the database for the To/CC/BCC lists keyed to that task. Behavior is otherwise identical to `EmailOperator`. Only recipient resolution is dynamic.

Because the operator identifies itself, migration is subtractive: swap the class name and delete the `to`, `cc`, and `bcc` parameters. Nothing else in the DAG changes.

### `DynamicRecipientDB`

SQLAlchemy-backed persistence layer for users and per-task recipient rules. On instantiation it calls `create_schema_if_missing()`, so a fresh deployment provisions its own tables with no migration step or manual setup.

Storage is pluggable through a single connection string. It defaults to SQLite and moves to Postgres, MySQL, or anything else SQLAlchemy supports by passing a different URI.

Exposes CRUD helpers (`add_recipient`, `get_emails_by_send_type`, and others) that are shared by both the operator and the UI, so there is one code path for reads and writes rather than two implementations that can drift.

### `Dag_Info_API_Plugin`

A custom Airflow plugin that registers Flask Blueprints against the Airflow webserver:

- `GET /dag_api/dags` returns all DAG IDs
- `GET /dag_api/dags/<dag_id>/tasks` returns task IDs for a given DAG

Internally it uses `DagBag` to introspect the live Airflow environment, so the UI is populated from what is actually deployed rather than from a hand-maintained list. The REST boundary means the UI gets authoritative DAG and task metadata without importing or depending on Airflow internals.

### Dash Web UI

Multi-page Dash application (Dash, Dash Mantine Components, Bootstrap) with componentized pages. It fetches DAG and task lists from the plugin API and recipient state from `DynamicRecipientDB`. Modals and checkboxes handle add/remove and To/CC/BCC flags, with dynamic filtering and bulk operations. Writes go through the same DB layer the operator reads from, so changes take effect on the next DAG run.

## Running It Locally

**1. Clone and build**

```bash
git clone <repo-url>
cd Dynamic-Email-Operator-UI
docker-compose up --build
```

`init_db.py` seeds the database with sample users on startup. Remove its reference in the `Dockerfile` to start empty. The Dash UI listens on port 8050, mapped to 8887 in `docker-compose.yml`.

**2. Register the Airflow plugin**

Drop `Dag_Info_API_Plugin.py` into your Airflow `plugins/` directory and restart the webserver and scheduler.

**3. Use the operator in your DAGs**

Replace every `EmailOperator` with `DynamicRecipientsEmailOperator` and remove the `to`, `cc`, and `bcc` parameters.

```python
from custom_email_operator import DynamicRecipientsEmailOperator

# db_conn_id defaults to SQLite; pass any SQLAlchemy URI to use another engine.
DynamicRecipientsEmailOperator(
    db_conn_id="sqlite:///Dynamic_Emails.db",
    subject="...",
    content="...",
)
```

**4. Manage recipients**

Visit `http://localhost:8887/`.
