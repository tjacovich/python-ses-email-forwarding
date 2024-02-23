from ses_email_forwarding.lambda_forward_email import process_message
import os
import io
from unittest.mock import patch
from unittest import TestCase
import boto3
import moto
import pytest
import json

@pytest.fixture
def empty_bucket():
    """
    Generates an empty S3 bucket using the moto mocking framework.
    """
    moto_fake = moto.mock_s3()
    try:
        moto_fake.start()
        conn = boto3.resource("s3")
        conn.create_bucket(Bucket="test-bucket-name")  # or the name of the bucket you use
        yield conn
    finally:
        moto_fake.stop()

@pytest.mark.usefixtures("empty_bucket")
class TestS3(TestCase):
    def test_upload_download_object(empty_bucket):
        """
        Tests S3 methods for AWS host
        """
        mock_config = {"S3_PROVIDERS": ["AWS"], "AWS_BUCKET_NAME": "test-bucket-name"}
        s3_client = boto3.resource("s3")
        s3_bucket = s3_client.Bucket(mock_config.get("AWS_BUCKET_NAME"))
        
        file_bytes = b"Test_text"
        object_name = "/test_object/name"
        s3_bucket.put_object(Body=file_bytes, Key=object_name)
        
        file_bytes = b"Test_text"
        object_name = "/test_object/name"
        with io.BytesIO() as s3_obj:
            s3_bucket.download_fileobj(object_name, s3_obj)
            s3_obj.seek(0)
            s3_file = s3_obj.read().decode("UTF-8")

class TestLambdaProcess(TestCase):
    def tesst_process_message(empty_bucket):
        with open("./stubdata/example-notification.json", "r") as f:
            record = json.loads(f)
        lambda_forward_email.process_message(record)
