#!/bin/bash

# This example uses the DR MLflow CLI to validate Azure AD Service Principal credentials.
# It's useful in troubleshooting, but not needed after issues are resolved.

export MLOPS_API_TOKEN="not-used-for-auth-check-but-must-be-present"

env PYTHONPATH=./ \
python datarobot_mlflow/drflow_cli.py \
  --verbose \
  --auth-type azure-service-principal \
  --service-provider-type azure-databricks \
	--action validate-auth
