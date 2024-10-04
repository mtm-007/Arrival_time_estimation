import requests


url = 'http://0.0.0.0:9696/predict'

inference_input = {
    "PULocationID": 110,
    "DOLocationID": 50,
    "PUDO": '110_50',
    "trip_distance": 9.98
}

response = requests.post(url, json=inference_input).json()

print(response)