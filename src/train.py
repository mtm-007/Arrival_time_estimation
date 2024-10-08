
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
from sklearn.metrics import root_mean_squared_error

#parameters 
model_choice = 'linear_reg_w_PU_DO'
out_put_file = f'model_{model_choice}.bin'

# ### data summary
# - There are 68211 total records, after filtering by duration > 1 & <=60 there will be 65924 records, which is 96% of the data
def read_and_preprocess(filename):
    df = pd.read_parquet(filename)
    
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    
    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    
    df['duration'] = df['duration'].apply(lambda td: td.total_seconds()/60)
    df['PU_DO'] = df['PULocationID'].astype(str) + '_' + df['DOLocationID'].astype(str)
    
    categorical = ['PU_DO']#'DOLocationID',]
    #categorical = ['PULocationID','DOLocationID']#'DOLocationID',]
    numerical = ['trip_distance']
    
    df[categorical]= df[categorical].astype(str)
    df = df[(df.duration > 1) & (df.duration <=60)]
    return df


df_train = read_and_preprocess('../data/green_tripdata_2023-01.parquet')
df_valid = read_and_preprocess('../data/green_tripdata_2023-02.parquet')


# ### Training pipeline

dv = DictVectorizer()

categorical = ['PULocationID','DOLocationID', 'PU_DO']
numerical = ['trip_distance']

train_dict = df_train[categorical + numerical].to_dict(orient='records')
X_train = dv.fit_transform(train_dict)

val_dict = df_valid[categorical + numerical].to_dict(orient='records')
x_val = dv.transform(val_dict)


target = 'duration'
y_train = df_train[target].values
y_valid = df_valid[target].values


#training
Linear_R = LinearRegression()
Linear_R.fit(X_train,y_train)
#prediction
y_pred = Linear_R.predict(x_val)
#evaluation
rmse = root_mean_squared_error(y_valid,y_pred)
print(f'MSE for Linear_reg: {rmse}')


# save model to pickle

with open(f'../models/{out_put_file}', 'wb') as f_out:
    pickle.dump((dv, Linear_R), f_out)


#With Lasso
lr = Lasso(alpha=0.01)
lr.fit(X_train,y_train)
#prediction
y_pred = lr.predict(x_val)
#evaluation
rmse_lasso= root_mean_squared_error(y_valid,y_pred)
print(f'MSE for Lasson: {rmse_lasso}')

#With Ridge
LR = Ridge()
LR.fit(X_train,y_train)
#prediction
y_pred = LR.predict(x_val)
#evaluation
rmse_ridge = root_mean_squared_error(y_valid,y_pred)
print(f'MSE for Ridge_reg: {rmse_ridge}')

