#dynamically generated bt TF
export MODEL_BUCKT_PROD="stg_mlflow_models"
export PREDICTIONS_STREAM_NAME="stg_ride_predictions"
export LAMBDA_FUNCTION="stg_prediction_lambda"

export MODEL_BUCKT_DEV="mlflow-models-zm-mlops-2"


export RUN_ID=$(aws s3api list-objects-v2 --bucket ${MODEL_BUCKT_DEV} \
--query 'sort_by(Contents, &LastModified)[-1].key' --output=text | cut -f2 -d/)

#A Hack, the training pipeline is reponsible to generate those artifacts, not used in prod
#copy model artifacts to newly created prod bucket
aws s3 sync s3://${MODEL_BUCKT_DEV} s3://${MODEL_BUCKT_PROD}

#set new var RUN_ID in existing set of vars
variables="{PREDICION_STREAM_NAME=${PREDICTION_STREAM_NAME}, MODEL_BUCKET=${MODEL_BUCKET_PROD}, RUN_ID=${RUN_ID}}"

aws lambda update-function-configuration --function-name ${LAMBDA_FUNCTION} --environment "Variables=${variables}"