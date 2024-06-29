import boto3
import os

def download_file_from_s3(bucket_name, s3_key, download_path):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, s3_key, download_path)
    print(f"Downloaded s3://{bucket_name}/{s3_key} to {download_path}")

if __name__ == "__main__":
    bucket_name = 'bucket-for-crowd-ai'
    files_to_download = [
        {'s3_key': 'data/data.csv', 'download_path': 'path/to/your/data.csv'},
        {'s3_key': 'models/model.joblib', 'download_path': 'path/to/your/model.joblib'},
    ]

    for file in files_to_download:
        download_file_from_s3(bucket_name, file['s3_key'], file['download_path'])
