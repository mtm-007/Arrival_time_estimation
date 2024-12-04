import mlflow
from mlflow.exceptions import MlflowException

# Your run ID
RUN_ID = "d4c48152bad344bd9bb991a7e7608484"
BUCKET_NAME = "mlflow-backend-storage-models"

def load_model():
    # Construct the full GCS path
    model_path = f"gs://{BUCKET_NAME}/1/{RUN_ID}/artifacts/model"
    
    try:
        print(f"Attempting to load model from: {model_path}")
        model = mlflow.pyfunc.load_model(model_path)
        print("Model loaded successfully!")
        return model
    except MlflowException as e:
        print(f"Error loading model: {e}")
        
        # Verify the path exists
        from google.cloud import storage
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"1/{RUN_ID}/artifacts/model/MLmodel")
        
        if blob.exists():
            print("MLmodel file exists in the specified path")
        else:
            print("MLmodel file does not exist in the specified path")
        raise

# Load the model
model = load_model()