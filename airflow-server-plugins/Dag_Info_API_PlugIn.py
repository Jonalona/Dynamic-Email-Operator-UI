# ############################################################################
# Jonah Reisner, July 18th 2025
#
# curl -X GET  "http://localhost:8080/dag_api/dags"
#
# This is a custom Airflow Plugin for AIRFLOW 1.10.15.
# It creates a simple, read-only REST API to list DAGs and their tasks.
#
# How to install:
# 1. Place this file in the `plugins` folder of your Airflow project.
# 2. Restart the Airflow Webserver and Scheduler for the plugin to be loaded.
#
# ############################################################################

from airflow.plugins_manager import AirflowPlugin
from airflow.models import DagBag
from airflow.utils.db import provide_session
from flask import Blueprint, jsonify # Flask is the web framework that Airflow's UI is built on.


# 1. CREATE THE FLASK BLUEPRINT
dag_api_bp = Blueprint(
    'dag_api_bp',
    __name__,
    url_prefix='/dag_api'
)


# 2. DEFINE THE API ENDPOINT TO LIST ALL DAGs
@dag_api_bp.route('/dags', methods=['GET'])
@provide_session  # Use the decorator imported from airflow.utils.db
def get_all_dags(session=None):
    """
    Returns a JSON list of all DAG IDs found by the DagBag.
    """
    dagbag = DagBag()
    dag_ids = sorted(dagbag.dags.keys())
    return jsonify(dags=dag_ids)


# 3. DEFINE THE API ENDPOINT TO LIST TASKS FOR A SPECIFIC DAG
# ============================================================================
@dag_api_bp.route('/dags/<string:dag_id>/tasks', methods=['GET'])
@provide_session
def get_tasks_for_dag(dag_id, session=None):
    """
    For a given DAG ID, returns a JSON list of its Task IDs.
    Returns a 404 error if the DAG ID is not found.
    """
    dagbag = DagBag()
    
    if dag_id not in dagbag.dags:
        error_response = {'error': f"Dag ID '{dag_id}' not found."}
        return jsonify(error_response), 404

    dag = dagbag.get_dag(dag_id)
    task_ids = sorted([task.task_id for task in dag.tasks])
    return jsonify(dag_id=dag_id, tasks=task_ids)


# 4. REGISTER THE PLUGIN WITH AIRFLOW
# ============================================================================
class DagApiPlugin(AirflowPlugin):
    name = "dag_api_plugin"
    flask_blueprints = [dag_api_bp]