from typing import Callable, Dict, Tuple, Union

from pandas import Series
from scipy.sparse._csr import csr_matrix
from sklearn.base import BaseEstimator

from mlops.utils_n.logging import track_experiment
from mlops.utils_n.models.sklearn import load_class, tune_hyperparameter

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def hyperparameter_tuninig(
    training_set: Dict[str, Union[Series, csr_matrix]],
    model_class_name: str,
    *args,
    **kwargs,
)->Tuple[
    Dict[str, Union[bool,float,int, str]],
    csr_matrix,
    Series,
    Callable[...,BaseEstimator],
]:
    
    X,X_train,X_val, y, y_train, y_val, _= training_set['build_block']

    model_class = load_class(model_class_name)

    hyperparameters = tune_hyperparameter(
        model_class,
        X_train=X_train,
        y_train = y_train,
        X_val = X_val,
        y_val= y_val,
        max_evaluation = kwargs.get('max_evaluation',10),
        random_state = kwargs.get('random_state', 3),
        callback = lambda **opts: track_experiment(**{**opts, **kwargs})
    )
    return hyperparameters, X,y, dict(cls=model_class, name= model_class_name)


