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
