from google.cloud import storage
import os
from google.oauth2 import service_account

# Set up credentials with proper scopes
credentials = service_account.Credentials.from_service_account_file(
    '/home/MERHAWI/DE_C.../terr.../ke../m...cred.json',
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)


# Initialize the client
client = storage.Client()

# Get the bucket
bucket = client.get_bucket("nyc_trip_data_bq")

# Upload the file
blob = bucket.blob("yellow_tripdata_2023-02.parquet")
blob.upload_from_filename("yellow_tripdata_2023-02.parquet")

print("File uploaded successfully!")