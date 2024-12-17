
```bash
docker build -t stream-model-duration:v2 .
```
```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTION_STREAM_NAME="ride_predictions" \
    -e RUN_ID="39ab5b2ee93a4131b17772294371d0ef" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="us-east-1" \
    stream-model-duration:v2
```


```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTION_STREAM_NAME="ride_predictions" \
    -e RUN_ID="Test123" \
    -e MODEL_LOCATION="/app/model" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="us-east-1" \
    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    -v $(pwd)/model:/app/model \
    stream-model-duration:v2
```

aws s3 permissions
```bash
aws iam create-policy --policy-name S3BucketAccessPolicy2 --policy-document file://s3_access_policy.json
aws iam create-user --user-name mle-zm-mlops

aws iam attach-user-policy --user-name mle-zm-mlops --policy-arn arn:aws:iam::869935103158:policy/S3BucketAccessPolicy2

aws iam get-policy --policy-arn arn:aws:iam::869935103158:policy/S3BucketAccessPolicy2

aws iam get-policy-version --policy-arn arn:aws:iam::869935103158:policy/S3BucketAccessPolicy2 --version-id v1

aws s3 ls s3://mlflow-models-zm-mlops-2

mlflow server --backend-store-uri=sqlite:///mlflow.db --default-artifact-root=s3://s3://mlflow-models-zm-mlops-2/

```

```bash
aws --endpoint-url=http://localhost:4566 \
     kinesis list-streams
```

```bash
aws --endpoint-url=http://localhost:4566 \
     kinesis create-stream \
     --stream-name ride_predictions \
     --shard-count 1

```

```bash
SHARD='shardId-000000000000'

aws --endpoint-url=http://localhost:4566 kinesis \
    get-shard-iterator \
        --shard-id ${SHARD} \
        --shard-iterator-type TRIM_HORIZON \
        --stream-name ${PREDICTION_STREAM_NAME} \
        --query 'ShardIterator' \

aws --endpoint-url=http://localhost:4566 kinesis get-records --shard-iterator
```

To prepare the project, run
 
```bash
make setup
```


