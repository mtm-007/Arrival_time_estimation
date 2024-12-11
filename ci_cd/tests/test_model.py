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


