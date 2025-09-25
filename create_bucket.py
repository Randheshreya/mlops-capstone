import boto3

bucket_name = "shreya-mlops-bucket"  # unique bucket name
region_name = "ap-south-1"

s3 = boto3.client(
    "s3",
    region_name=region_name
)

try:
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': region_name}
    )
    print(f"Bucket '{bucket_name}' created successfully!")
except Exception as e:
    print(f"Bucket may already exist or error: {e}")
