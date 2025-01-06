import os
import boto3
import logging
from botocore.exceptions import ClientError


class StorageHandler:
    def __init__(self, local_path=None, s3_bucket=None):
        self.local_path = local_path
        self.s3_bucket = s3_bucket
        if s3_bucket:
            self.s3_client = boto3.client('s3')
        else:
            for path in ["json",'maps','photos']:
                os.makedirs(local_path+'/'+path, exist_ok=True)


    def save_file(self, file_path, content):
        """
        Save a file to local storage or S3.
        """
        if self.s3_bucket:
            # lambda
            try:
                self.s3_client.put_object(Bucket=self.s3_bucket, Key=file_path, Body=content)
            except ClientError as e:
                logging.error(f"Failed to save file to S3: {e}")
                raise
        else:
            # local
            with open(self.local_path+"/"+file_path, 'w',encoding="utf-8") as f:
                f.write(content)

    def load_file(self, file_path):
        """
        Load a file from local storage or S3.
        """
        if self.s3_bucket:
            # S3 mode
            try:
                response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=file_path)
                return response['Body'].read().decode('utf-8')
            except ClientError as e:
                logging.error(f"Failed to load file from S3: {e}")
                raise
        else:
            # Local mode
            try:
                with open(self.local_path+"/"+file_path, 'r',encoding="utf-8") as f:
                    return f.read()
            except OSError as e:
                logging.error(f"Failed to load file locally: {e}")
                raise

    def save_photo(self, file_path, content):
        """
                Save a file to local storage or S3.
                """
        if self.s3_bucket:
            # lambda
            try:
                self.s3_client.put_object(Bucket=self.s3_bucket, Key="/photos/"+file_path, Body=content)
            except ClientError as e:
                logging.error(f"Failed to save file to S3: {e}")
                raise
        else:
            # local

            with open(self.local_path+"/photos/"+file_path, 'wb') as f:
                for chunk in content.iter_content(chunk_size=8192):
                    f.write(chunk)

    def photo_exists(self, file_path):
        """
        Check if a photo exists in local storage or S3.

        :param photo_path: The path to the photo.
        :return: True if the photo exists, False otherwise.
        """
        if self.s3_bucket:
            # S3 mode
            try:
                self.s3_client.head_object(Bucket=self.s3_bucket, Key="/photos/"+file_path)
                return True
            except ClientError as e:
                if e.response['Error']['Code'] == "404":
                    return False
                logging.error(f"Error checking photo existence in S3: {e}")
                raise
        else:
            # Local mode
            return os.path.exists(self.local_path+"/photos/"+file_path)
