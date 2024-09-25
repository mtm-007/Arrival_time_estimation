import pandas as pd

def clean(
    df: pd.DataFrame,
    include_extreme_durations: bool= False,
)-> pd.DataFrame:
    #convert pickup and dropoff datetime columns to datetime type
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)
     
    if not include_extreme_durations:
        #filter trips with less than 1 minute duration or more than 60 minutes
        df = df[(df.duration >=1) & (df.duration <=60)]

    #convert locationId's to str to treat them as categorical features
    catergorical = ['PULocationID', 'DOLocationID']
    df[catergorical] = df[catergorical].astype(str)

    return df
