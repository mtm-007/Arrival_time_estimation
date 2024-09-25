from typing import Tuple, List, Union
from pandas import DataFrame, Index 


def split_on_value(
    df: DataFrame,
    features: str,
    value: Union[float, str, int],
    drop_feaure: bool=True,
    return_indexes: bool = False,
) -> Union[Tuple[DataFrame, DataFrame], Tuple[Index, Index]]:
    df_train = df[df[features] < value]
    df_val = df[df[features] >= value]

    if return_indexes:
        return df_train.index, df_val.index
    
    if drop_feaure:
        df_train = df_train.drop(columns= [features])
        df_val = df_val.drop(columns = [features])

    return df_train, df_val