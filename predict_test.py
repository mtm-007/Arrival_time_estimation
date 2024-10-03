import requests

url = 'http://0.0.0.0:9696/predict'

inference_input = {
    "PULocationID": 11,
    "DOLocationID": 50,
    "PU_DO": "11_50",
    "trip_distance": 0.0
}

response = requests.post(url, json=inference_input).json()

print(response)