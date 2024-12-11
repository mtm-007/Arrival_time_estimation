import requests

event = {
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49657905793130352344458786332916805586989760508803940354",
                "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMjEwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogNjksCiAgICAgICAgICAgICJ0cmlwX2Rpc3RhbmNlIjogOS45OAogICAgICAgIH0sCiAgICAgICAgInJpZGVfaWQiOiAyNTYKICAgICB9",
                "approximateArrivalTimestamp": 1732140998.471
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49657905793130352344458786332916805586989760508803940354",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::869935103158:role/lambda-kinesis-role",
            "awsRegion": "us-west-2",
            "eventSourceARN": "arn:aws:kinesis:us-west-2:869935103158:stream/ride_events"
        }
    ]
}

url='http://localhost:8080/2015-03-31/functions/function/invocations'
responce = requests.post(url, json=event)
print(responce.json())