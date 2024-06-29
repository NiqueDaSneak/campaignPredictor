import boto3
import os

s3 = boto3.client('s3')

def upload_file_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    s3.upload_file(file_name, bucket, object_name)

def download_file_from_s3(bucket, object_name, file_name=None):
    if file_name is None:
        file_name = os.path.basename(object_name)
    s3.download_file(bucket, object_name, file_name)
