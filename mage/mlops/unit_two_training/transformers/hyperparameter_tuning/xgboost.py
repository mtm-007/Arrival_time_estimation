from typing import Tuple, Union,Dict   
import numpy as np
import xgboost as xgb 
from pandas import Series 
from scipy.sparse._csr import csr_matrix  

from mlops.utils_n.logging import track_experiment
from mlops.utils_n.models.xgboost import build_data, tune_hyperparameters

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def hyperparameter_tuning(
    training_set: Dict[str, Union[Series, csr_matrix]],
    **kwargs,
)-> Tuple[
    Dict[str, Union[bool, float, int, str]],
    csr_matrix,
    Series,
]:
    X, X_train, X_val, y, y_train, y_val,_ = training_set['build_block']

    training = build_data(X_train, y_train)
    validation  = build_data(X_val, y_val)

    best_hyperparameters = tune_hyperparameters(
        training, 
        validation,
        callback= lambda **opts: track_experiment(**{**opts, **kwargs}),
        # max_evaluations = kwargs.get('max_evaluations', 50)
        # early_stopping_rounds = kwargs.get('early_stopping_rounds', 40)
        **kwargs,
    )

    return best_hyperparameters, X_train, y_train