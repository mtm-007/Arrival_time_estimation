from google.cloud import storage
from google.oauth2 import service_account
import os

def upload_to_gcp_bucket(
    bucket_name: "nyc_trip_data_bq",
    source_file_path: "/home/MERHAWI/DE_CDSP/data/yellow_tripdata_2023-01.parquet",
    destination_blob_name: str = "yellow_tripdata_2023-01.parquet","https://console.cloud.google.com/bigquery?ws=!1m4!1m3!3m2!1sresonant-time-434823-n0!2snyc_trip_data",
    credentials_path: str =  '/home/MERHAWI/DE_.../terr.../../my_tera_cred.json'
):
    """
    Upload a file to Google Cloud Storage bucket with proper authentication.
    
    Args:
        bucket_name (str): Name of the GCP bucket
        source_file_path (str): Local path to the file to upload
        destination_blob_name (str): Name to give the file in the bucket (if None, uses source filename)
        credentials_path (str): Path to service account JSON key file
    """
    try:
        # If destination blob name not provided, use source filename
        if destination_blob_name is None:
            destination_blob_name = os.path.basename(source_file_path)

        # Initialize storage client with explicit credentials if provided
        if credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
            client = storage.Client(credentials=credentials)
        else:
            # Will use default credentials from environment
            client = storage.Client()

        # Get bucket and create blob
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Upload the file
        blob.upload_from_filename(source_file_path)
        
        print(f"File {source_file_path} uploaded successfully to {bucket_name}/{destination_blob_name}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Method 1: Using service account JSON key file
    upload_to_gcp_bucket(
        bucket_name="nyc_trip_data_bq",
        source_file_path="/home/MERHAWI/DE_CDSP/data/yellow_tripdata_2023-01.parquet",
        credentials_path= "/home/MERHAWI/DE_CD../terraf.../k../my_tera_cred.json"
    )

    # Method 2: Using default credentials
    upload_to_gcp_bucket(
        bucket_name="nyc_trip_data_bq",
        source_file_path="/home/MERHAWI/DE_CDSP/data/yellow_tripdata_2023-01.parquet"
    )