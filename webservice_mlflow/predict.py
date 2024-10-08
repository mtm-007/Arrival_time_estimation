import pickle,mlflow,os
from flask import Flask,request, jsonify
from mlflow import MlflowClient

#RUN_ID = "d4c48152bad344bd9bb991a7e7608484"
RUN_ID = os.getenv('RUN_ID')
#logged_model = f"gs://mlflow-backend-storage-models/1/{RUN_ID}/artifacts/model"
logged_model = f"gs://mlflow-backend-storage-models/1/{RUN_ID}/artifacts/model"
model = mlflow.pyfunc.load_model(logged_model)


def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

def predict(ride_input):
    y_pred = model.predict(ride_input) 
    return float(y_pred[0])
    

app = Flask('arrival_prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        "duration": pred,
        "model_version": RUN_ID,
    }

    return jsonify(result)

if __name__=='__main__':
    app.run(debug=True, host = '0.0.0.0', port=9696)
