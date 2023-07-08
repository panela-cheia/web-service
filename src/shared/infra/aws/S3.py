import os
from dotenv import load_dotenv

from botocore.exceptions import BotoCoreError

import boto3

load_dotenv('.env')

class S3Client:
    def __init__(self):
        self.s3_bucket = os.getenv('S3_BUCKET_NAME')
        self.s3_client = boto3.client('s3')

    def upload(self,file,filename):
        try:
            self.s3_client.upload_fileobj(file, self.s3_bucket, filename)
        except BotoCoreError as e:
            return e
    
    def file_url(self,filename)-> str:
        return f'https://{self.s3_bucket}.s3.amazonaws.com/{filename}'
    
    def delete(self,filename):
        self.s3_client.delete_object(Bucket=self.s3_bucket, Key=filename)


s3 = S3Client()