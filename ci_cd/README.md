
```bash
docker build -t stream-model-duration:v2 .
```

```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTION_STREAM_NAME="ride_predictions" \
    -e RUN_ID="d4c48152bad344bd9bb991a7e7608484" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="us-west-2" \
    stream-model-duration:v2
```