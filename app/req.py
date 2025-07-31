import requests
 
airflow_dags_url = "http://jrd-airflow:8080/api/experimental/dags"
 
try:
    response = requests.get(airflow_dags_url, timeout=5)
    if response.status_code == 200:
        dags_info = response.json()
        dag_ids = [dag['dag_id'] for dag in dags_info['dags']]
        print("Available DAGs:", dag_ids)
    else:
        print(f"Failed to fetch DAGs. Status code: {response.status_code}, Response: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Error connecting to Airflow API: {e}")

   # curl -X GET --user "jreisner:JR_123" "http://jrd-airflow:8080/api/experimental/latest_runs"