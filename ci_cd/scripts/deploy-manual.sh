#manul deployment, getting the environment variables
# not in production
export RUN_ID=$(aws s3api list-objects-v2 --bucket ${MODEL_BUCKET_DEV} \
--query 'sort_by(Contents, &LastModified)[-1].key' --output=text | cut -f2 -d/)