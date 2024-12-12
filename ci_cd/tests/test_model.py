#unit tests for model.py

import model

def test_base64_decode():
     input_base64= "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMjEwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogNjksCiAgICAgICAgICAgICJ0cmlwX2Rpc3RhbmNlIjogOS45OAogICAgICAgIH0sCiAgICAgICAgInJpZGVfaWQiOiAyNTYKICAgICB9"
     actual_result = model.base64_decode(input_base64)

     expected_result = {
          
          "ride": {
            "DOLocationID": 69,
            "PULocationID": 210,
            "trip_distance": 9.98
        },
        "ride_id": 256
     }

     assert actual_result==expected_result

def test_prepare_features():
    
    model_service =model.ModelService(None)
    ride = {
        "DOLocationID": 69,
        "PULocationID": 210,
        "trip_distance": 9.98
    }
    actual_features = model_service.prepare_features(ride)
    expected_features = {
        "PU_DO":"210_69",
        "trip_distance": 9.98
    }

    assert actual_features == expected_features 

class ModelMock():
    def __init__(self,value):
        self.value = value
    def predict(self, X):
        n = len(X)
        return [self.value]*n
 
def test_predict():
    model_mock = ModelMock(10.0)
    model_service =model.ModelService(model_mock)
    
    features = {
        "PU_DO":"210_69",
        "trip_distance": 9.98
    }
    actual_predictions = model_service.predict(features)
    expected_prediction = 10.0

    assert actual_predictions == expected_prediction

def test_lambda_handler():
    model_mock = ModelMock(10.0)
    model_version = 'Test123'
    model_service =model.ModelService(model_mock, model_version)
    event = {
        "Records": [{
            "kinesis": {
                "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMjEwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogNjksCiAgICAgICAgICAgICJ0cmlwX2Rpc3RhbmNlIjogOS45OAogICAgICAgIH0sCiAgICAgICAgInJpZGVfaWQiOiAyNTYKICAgICB9"  
                        },     
                }]
             }
    
    actual_predictions = model_service.lambda_handler(event)
    expected_predictions = {
        "predictions": [{
            'model' : 'ride_duration_prediction_model',
            'version': model_version,
            'prediction' : {
                'ride duration': 10.0,
                'ride_id': 256
            } 
            }
        ]
    }

    assert actual_predictions == expected_predictions
   