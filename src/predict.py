from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
import pickle
from flask import Flask
from flask import request
from flask import jsonify

#parameters
model_choice = 'linear_reg_w_PU_DO'
out_put_file = f'model_{model_choice}.bin'

# modified after moving one model pickle file, to suit for docker
with open(f'{out_put_file}', 'rb') as f_in:
    dv, Linear_R = pickle.load(f_in)

app = Flask('arrival_prediction')
@app.route('/predict', methods=['POST'])

def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

def predict(inference_input):
    #inference_input = request.get_json()

    X_inf = dv.transform([inference_input])
    y_pred = Linear_R.predict(X_inf)
    result  = {
        "Prediction result": float(y_pred),
    }
    return result[0]
    #return jsonify(result)

if __name__=='__main__':
    app.run(debug=True, host = '0.0.0.0', port=9696)

