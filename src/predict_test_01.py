import requests

inference_input = {
    "PULocationID": 210,
    "DOLocationID": 69,
    #"PUDO": '110_50',
    "trip_distance": 9.98
}

url = 'http://0.0.0.0:9696/predict'
response = requests.post(url, json=inference_input).json()
print(response)


#print(response)