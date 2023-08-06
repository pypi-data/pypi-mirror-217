from botocore.exceptions import ClientError
from boto3 import *

def checkins3(session, s3_bucket, key):
    """
    Checks if an object exists in an Amazon S3 bucket. If the object doesn't exist,
    it creates it in the bucket.

    Args:
        session (boto3.Session): The Boto3 session for interacting with AWS.
        s3_bucket (str): Name of the S3 bucket.
        key (str): Key (name) of the object in the bucket.
    """
    s3_client = session.client('s3')
    try:
        s3_client.head_object(Bucket=s3_bucket, Key=key)
    except:
        s3_client.put_object(Bucket=s3_bucket, Key=key)
        print(f"Object Created s3://{s3_bucket}/{key}.")

def download(session, s3_bucket, key, file_name):
    """
    Downloads an object from Amazon S3 and saves it to a local file.

    Args:
        session (boto3.Session): The Boto3 session for interacting with AWS.
        s3_bucket (str): Name of the S3 bucket.
        key (str): Key (name) of the object in the bucket.
        file_name (str): Name of the local file to save the downloaded object.
    """
    try:
        res = session.download_file(s3_bucket, key, file_name)
        return res
    except Exception as e:
        print(f"Failed to download the object: {e}")

def write(new_line, file_name):
    """
    Writes a new line to a file.
    
    Args:
        new_line (str): New line to write.
        file_name (str): Name of the file.
    """
    fileResult=open(file_name, 'a')
    fileResult.write(new_line)
    fileResult.close()

def upload(session, file_name, bucket, object_name=None):
    """
    Uploads a file to Amazon S3.

    Args:
        session (boto3.Session): The Boto3 session for interacting with AWS.
        file_name (str): Name of the local file to upload.
        bucket (str): Name of the S3 bucket.
        object_name (str, optional): Name of the object in the bucket. If not provided, the name of the local file will be used.

    Returns:
        bool: True if the upload was successful, False otherwise.

    Raises:
        ClientError: If an error occurs while uploading the file.
    """
    if object_name is None:
        object_name = file_name
    s3_client = session.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ContentType': "text/csv"})
    except ClientError as e:
        print(e)
        return False
    return True
