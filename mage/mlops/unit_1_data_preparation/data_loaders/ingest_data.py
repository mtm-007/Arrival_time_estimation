import requests
from io import BytesIO
from typing import List

import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(**kwargs) ->pd.DataFrame:
    dfs: List[pd.DataFrame] = []

    for year,months in [(2024 ,(1,3))]:
        for i in range(*months):
            response = requests.get(
                #make sure to use the raw format of the dataset. different that the github page url {change tree to raw}
                   'https://github.com/mage-ai/datasets/raw/master/taxi/green'
                f'/{year}/{i:02d}.parquet'
            )

            if response.status_code != 200:
                raise Exception(response.text)

            #df = pd.read_parquet(BytesIO(response.content))
            df = pd.read_parquet(BytesIO(response.content))
            dfs.append(df)
    
    return pd.concat(dfs)
