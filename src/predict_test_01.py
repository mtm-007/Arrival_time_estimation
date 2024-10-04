import requests
import predict


url = 'http://0.0.0.0:9696/predict'

inference_input = {
    "PULocationID": 110,
    "DOLocationID": 50,
    #"PUDO": '110_50',
    "trip_distance": 59.98
}

features = predict.prepare_features(inference_input)
pred = predict.predict(features)
print(f'From new_test: {pred}\n')

#response = requests.post(url, json=inference_input).json()

#print(response)