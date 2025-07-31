#!/bin/bash
curl -X GET \
  --user "jreisner:JR_123" \
  "http://jrd-airflow:8080/api/experimental/dags"