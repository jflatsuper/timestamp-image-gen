import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
bucket_name = os.getenv("S3_BUCKET_NAME")


def upload_to_s3(file_name, file_data):
    try:
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_data)
        return True
    except Exception as e:
        print(e)
        return False
