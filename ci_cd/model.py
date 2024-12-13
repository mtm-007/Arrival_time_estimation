import json
import os
import boto3
import base64

import pickle,mlflow
from flask import Flask,request, jsonify
from mlflow import MlflowClient

def get_model_path(RUN_ID):
    model_location = os.getenv('MODEL_LOCATION')

    if model_location is not None:
        return model_location
    
    BUCKET_NAME = os.getenv( 'BUCKET_NAME',"mlflow-models-zm-mlops-2")
    model_location = f"s3://{BUCKET_NAME}/{RUN_ID}/artifacts/model"
    return model_location

def load_model(RUN_ID):
    model_path = get_model_path(RUN_ID)
    model = mlflow.pyfunc.load_model(model_path)
    return model
    
def base64_decode(encoded_data):
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    ride_event = json.loads(decoded_data)
    return ride_event

class ModelService():
    def __init__(self,model, model_version=None, callbacks=None):
        self.model = model 
        self.model_version = model_version
        self.callbacks = callbacks or []

    def prepare_features(self, ride):
        features = {}
        features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
        features['trip_distance'] = ride['trip_distance']
        return features

    def predict(self, features):
        pred = self.model.predict(features)
        return float(pred[0])

    
    def lambda_handler(self, event):
        prediction_events =[]

        for record in event['Records']:
            encoded_data = record['kinesis']['data']
            ride_event= base64_decode(encoded_data)
            
            ride = ride_event['ride']
            ride_id= ride_event['ride_id']

            features = self.prepare_features(ride)
            prediction = self.predict(features)
            prediction_event = {
                'model' : 'ride_duration_prediction_model',
                'version': self.model_version,
                'prediction' : {
                    'ride duration': prediction,
                    'ride_id': ride_id
                } 
            }
            for callback in self.callbacks:
                callback(prediction_event)
            
            prediction_events.append(prediction_event)
        
    
        return{
            "predictions": prediction_events
        }


class KinesisCallback():
    def __init__(self, kinesis_client, prediction_stream_name):
        self.kinesis_client = kinesis_client
        self.prediction_stream_name = prediction_stream_name

    def put_record(self, prediction_event):
        ride_id = prediction_event['prediction']['ride_id']

        self.kinesis_client.put_record(
            StreamName= self.prediction_stream_name,
            Data=json.dumps(prediction_event),
            PartitionKey=str(ride_id)
        )

def create_kinesis_client():
    end_point_url = os.getenv('KINESIS_ENDPOINT_URL')

    if end_point_url is None:
        return boto3.client('kinesis')
    return boto3.client('kinesis',end_point_url=end_point_url )

def init(prediction_stream_name: str,run_id: str, test_run: bool):
    model = load_model(run_id)
    
    callbacks = []
    if not test_run:
        kinesis_client = boto3.client('kinesis') 
        kinesis_callback = KinesisCallback(
            kinesis_client,
            prediction_stream_name
        )
        callbacks.append(kinesis_callback.put_record)

        
    model_service = ModelService(
        model=model, 
        model_version=run_id,
        callbacks=callbacks
        )
    return model_service