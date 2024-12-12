import requests
import json

from deepdiff import DeepDiff

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
actual_responce = requests.post(url, json=event).json()

print('actual_responce: ')

print(json.dumps(actual_responce, indent=2))

expected_response = {
    'predictions': [{
        'model': 'ride_duration_prediction_model', 
        'version': 'Test123', 
        'prediction': 
            {
                'ride duration': 28.14, 
                'ride_id': 256  
            }
        }]}

diff = DeepDiff(actual_responce, expected_response,significant_digits=1)

print(f'diff={diff}')

assert 'type_changes' not in diff
assert 'values_changed' not in diff