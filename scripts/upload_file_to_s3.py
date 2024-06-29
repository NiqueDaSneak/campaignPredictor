import boto3
import os

def upload_file_to_s3(bucket_name, file_path, s3_key):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, s3_key)
    print(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")

if __name__ == "__main__":
    bucket_name = 'bucket-for-crowd-ai'
    files_to_upload = [
        {'file_path': 'path/to/your/data.csv', 's3_key': 'data/data.csv'},
        {'file_path': 'path/to/your/model.joblib', 's3_key': 'models/model.joblib'},
    ]

    for file in files_to_upload:
        upload_file_to_s3(bucket_name, file['file_path'], file['s3_key'])
