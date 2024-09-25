from mlops.utils_n.analytics.data import load_data

@data_Source
def data(*args, **kwargs):
    return load_data()