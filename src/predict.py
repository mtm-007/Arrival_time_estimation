import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
import pickle
import pyarrow
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

#parameters
model_choice = 'linear_reg'
out_put_file = f'model_type_{model_choice}.bin'

#load model with pickle
with open(f'../models/{out_put_file}', 'rb') as f_in:
    dv, Linear_R = pickle.load(f_in)

inference_input =  'To be Defined'
X_inf = dv.tranform([inference_input])
Y_inf_pred = model.predict(X_inf)

print(f'Inference input: {inference_input}')
print(f'Prediction output: {Y_inf_pred}s')