#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import pickle
import pyarrow
import mlflow
import os
import sys
import uuid

from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import root_mean_squared_error



def generate_uuid(n):
    '''
        adding unique identifiers but mostly they are already in the data
    '''
    ride_id = []
    for i in range(n):
        ride_id.append(str(uuid.uuid4()))
    return ride_id
    
def read_dataframe(filename:str):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds()/60
    df = df[(df.duration > 1) & (df.duration <=60)]
    
    df['ride_id'] = generate_uuid(len(df))
    return df

def prepare_dictionaries(df: pd.DataFrame):
    categorical = ['PULocationID','DOLocationID']
    df[categorical]= df[categorical].astype(str)
    
    df['PU_DO'] = df['PULocationID'].astype(str) + '_' + df['DOLocationID'].astype(str)
    categorical = ['PU_DO']
    numerical = ['trip_distance']
    dicts = df[categorical + numerical].to_dict(orient='records')
    return dicts


def load_model(run_id):
    logged_model = f"gs://mlflow-backend-storage-models/1/{run_id}/artifacts/model"
    model = mlflow.pyfunc.load_model(logged_model)
    return model
    
def apply_model(input_file, run_id, output_file):
    print(f'reading data from {input_file}...')
    df = read_dataframe(input_file)
    dict = prepare_dictionaries(df)
    
    print(f'loading model with RUN_ID={run_id}....')
    model = load_model(run_id)
    print(f'applying the model...')
    y_pred = model.predict(dict)
    
    print(f'saving output to {output_file}...')
    df_results = pd.DataFrame()
    df_results['ride_id'] = df['ride_id']
    df_results['lpep_pickup_datetime'] = df['lpep_pickup_datetime']
    df_results['PULocationID'] = df['PULocationID']
    df_results['DOLocationID'] = df['DOLocationID']
    df_results['actual_duration'] = df['duration']
    df_results['predicted_duration'] = y_pred
    df_results['diff'] = df_results['actual_duration'] - df_results['predicted_duration']
    df_results['model_version'] = run_id
    df_results.to_parquet(output_file, index=False)
  


def run():
    taxi_type = sys.argv[1] #'green'
    year = int(sys.argv[2]) #2023
    month = int(sys.argv[3]) #2

    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    output_file =f'output/{taxi_type}/{year:04d}-{month:02d}.parquet'

    run_id = sys.argv[4]#
    #os.getenv('RUN_ID', 'd4c48152bad344bd9bb991a7e7608484')
    

    apply_model(
                input_file=input_file, 
                run_id=run_id, 
                output_file=output_file
                )

if __name__=='__main__':
    run()





