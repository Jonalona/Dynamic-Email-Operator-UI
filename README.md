# Dynamic Email Operator UI - by Jonah Reisner

### 🚀 Live Demo (UI + API on Render)

https://dynamic-email-operator-ui.onrender.com/

Have fun exploring the hosted interface—both the Dash webapp and its backend run on Render. Any changes you make in the UI are saved in the shared database and persist beyond your browser.

A full-stack toolkit for managing email notifications in Apache Airflow without touching DAG code.

## Overview

Airflow’s native `EmailOperator` hard-codes recipients at DAG build time. Updating a distribution list means redeploying code—slow, brittle, and inaccessible to non-developers.
This project introduces an integrated solution that moves recipient management to a database and a web UI, enabling real-time changes that automatically propagate to running DAGs.

## Key Components

### 1. `DynamicRecipientsEmailOperator`
- Subclass of Airflow’s `EmailOperator`.
- Automatically determines its `dag_id` and `task_id` at runtime via the execution context.
- Pulls **To/CC/BCC** recipients from the database instead of requiring parameters in code.
- Behavior mirrors `EmailOperator`; only the recipient list is dynamic.

### 2. `DynamicRecipientDB`
- SQLAlchemy-backed layer for persistent storage of users and per-task recipient rules.
- Defaults to SQLite but can switch to any SQLAlchemy-supported engine by changing a single connection string.
- On instantiation, calls `create_schema_if_missing()` to create tables if they don’t exist—zero manual setup.
- Exposes CRUD helpers (`add_recipient`, `get_emails_by_send_type`, etc.) used by both the operator and the UI.

### 3. `Dag_Info_API_Plugin`
- Custom Airflow plugin that registers Flask endpoints:
  - `GET /dag_api/dags` → list of all DAG IDs.
  - `GET /dag_api/dags/<dag_id>/tasks` → task IDs for a given DAG.
- Internally uses `DagBag` to introspect the Airflow environment, providing a live view of deployed DAGs.
- Serves the UI with authoritative DAG/task data without sharing Airflow’s internal code.

### 4. Dash Web UI
- Multi-page Dash application (Dash + Mantine + Bootstrap) for non-developers.
- Fetches DAG and task lists via the plugin API; displays recipients per task.
- Modals and checkboxes let users add/remove recipients and specify To/CC/BCC flags.
- Changes are persisted through `DynamicRecipientDB`, so updates take effect immediately.

## Architecture

```
          ┌────────────────────────┐
          │   Dash Frontend UI     │
          │  (users manage lists)  │
          └──────────┬─────────────┘
                     │ REST calls
                     ▼
      ┌─────────────────────────────┐
      │ Dag_Info_API_Plugin (Airflow)│
      │ provides DAG & task metadata │
      └──────────┬──────────────────┘
                 │ DB operations
                 ▼
      ┌─────────────────────────────┐
      │ DynamicRecipientDB (SQLAlchemy) │
      └──────────┬──────────────────┘
                 │ runtime lookup
                 ▼
      ┌─────────────────────────────┐
      │ DynamicRecipientsEmailOperator │
      │  (replaces EmailOperator)   │
      └─────────────────────────────┘
```

- All components communicate via simple, well-defined interfaces, making the system modular and extensible.
- Dockerfile & `docker-compose.yml` demonstrate containerized deployment and reproducible environments.

## Features

- **No hard-coded recipients**: Editing a database row updates email lists for the next DAG run—no code changes.
- **Database auto-provisioning**: Tables are created automatically if missing.
- **Pluggable storage**: Switch from SQLite to Postgres, MySQL, etc. by changing one parameter.
- **RESTful DAG discovery**: Plugin exposes DAG/task metadata without giving direct access to Airflow internals.
- **Rich UI**: Multi-page, componentized Dash app with modals, dynamic filtering, and bulk operations.
- **Scalable architecture**: Operator, API plugin, and UI are decoupled yet integrated through stable interfaces.

## Technology Stack

- **Python 3.12**
- **Apache Airflow 1.10.x**
- **Dash & Dash Mantine Components**
- **SQLAlchemy**
- **Docker / Docker Compose**
- **Flask Blueprints (within Airflow plugin)**

## Getting Started

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd Dynamic-Email-Operator-UI
   ```

2. **Build & run the container**
   ```bash
   docker-compose up --build
   ```
   - The `init_db.py` script seeds the database on startup.
   - Dash UI listens on port 8050 (mapped to 8887 in `docker-compose.yml`).

3. **Register the Airflow plugin**
   - Drop `Dag_Info_API_Plugin.py` into your Airflow `plugins/` directory and restart the webserver/scheduler.

4. **Use the operator in DAGs**
   Traditionally, you would use Airflow's 'EmailOperator'. Migrating from 'EmailOperator' is very easy.
   Simply replace every with 'DynamicRecipientsEmailOperator' and remove 'to','cc, and 'bcc' parameters.

   ```python
   from custom_email_operator import DynamicRecipientsEmailOperator
    # db_conn_id parameter defaults to SQLite, but you can easily use another database system by passing in another SQLAlchemy URI.
   DynamicRecipientsEmailOperator(db_conn_id="sqlite:///Dynamic_Emails.db", subject='...', content='...',...)
   ```

6. **Update recipients via UI**
   - Navigate to `http://localhost:8887/` to visit the web app and and manage recipients per DAG/task.

## Why It Matters

- **Faster iteration**: Operations teams can update alert lists in seconds.
- **Reduced risk**: Eliminates code redeploys for contact changes.
- **Demonstrates full-stack expertise**: Airflow internals, REST plugins, SQLAlchemy, Dash UI, and Docker all come together in one cohesive system.

---

This project showcases the design and implementation of a production-style ecosystem: custom Airflow operators, plugins, a dynamic database layer, and a modern UI—each coded from scratch and integrated to streamline email notifications in complex workflows.

