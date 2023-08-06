#!/bin/bash

ACTION=sync
#ACTION=delete-all-dr-keys
#ACTION=list-mlflow-keys

DR_MODEL_ID="63d7ac836eafed6f9f557abc"

env PYTHONPATH=./ \
python datarobot_mlflow/drflow_cli.py \
	--mlflow-url http://localhost:8080 \
 	--mlflow-model diabetes-1  \
        --mlflow-model-version 1 \
        --dr-model $DR_MODEL_ID \
        --dr-url https://staging.datarobot.com \
        --with-artifacts \
        --verbose \
	--action $ACTION
