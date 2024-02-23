import ses_email_forwarding.lambda_forward_email
import os
import io
from unittest.mock import patch
from unittest import TestCase
import boto3
import moto
import pytest
import json

@pytest.fixture
def test_bucket():
    """
    Generates an empty S3 bucket using the moto mocking framework.
    """
    with moto.mock_s3():
        conn = boto3.resource("s3")
        conn.create_bucket(Bucket="DOC-EXAMPLE-BUCKET")  # or the name of the bucket you use
        s3_bucket=conn.Bucket("DOC-EXAMPLE-BUCKET")
        
        with open("tests/stubdata/example-notification.json", "r") as f:
            record = json.load(f)
            s3_key = record['Records'][0]['s3']['object']['key']
        
        with open("tests/stubdata/test-email.txt","rb") as f:    
            file_bytes = f.read()

        s3_bucket.put_object(Body=file_bytes, Key=s3_key)
        yield conn


class TestLambdaProcess(TestCase):
    def test_lambda_handler(self):
        with open("tests/stubdata/example-notification.json", "r") as f:
            record = json.load(f)
        with patch('ses_email_forwarding.lambda_forward_email.forward_ses_email', return_value=None) as mocked:
            ses_email_forwarding.lambda_forward_email.lambda_handler(record, context=None)
        self.assertTrue(mocked.called)

class TestEmailModification(TestCase):
    def test_modify_email(self):
        with open("tests/stubdata/test-email.txt","r") as f:    
            raw_email = f.read()
        message, from_addr, to_addr = ses_email_forwarding.lambda_forward_email.modify_email_message(raw_email)
        with open("tests/stubdata/test-modified-email.txt") as f:
            test_text = f.read()
        self.assertEqual(message.as_string(), test_text)
        self.assertEqual(from_addr, "Full Name <"+os.environ["from_addr"]+">")
        self.assertEqual(to_addr, os.environ['to_addr'])

@pytest.mark.usefixtures("test_bucket")
class TestSESEmailForwarding(TestCase):
    def test_process_resend_email(self):
        """
        Tests S3 methods for AWS host
        """
        mock_config = {"S3_PROVIDERS": ["AWS"], "AWS_BUCKET_NAME": "DOC-EXAMPLE-BUCKET"}
        s3_client = boto3.resource("s3")
        s3_bucket = s3_client.Bucket(mock_config.get("AWS_BUCKET_NAME"))
        
        with open("tests/stubdata/example-notification.json", "r") as f:
            record = json.load(f)
            s3_key = record['Records'][0]['s3']['object']['key']
        
        with open("tests/stubdata/test-email.txt","rb") as f:    
             file_bytes = f.read()

        with io.BytesIO() as s3_obj:
            s3_bucket.download_fileobj(s3_key, s3_obj)
            s3_obj.seek(0)
            self.assertEqual(file_bytes, s3_obj.read())

        with patch('smtplib.SMTP', autospec=True) as mock_smtp: 
            ses_email_forwarding.lambda_forward_email.forward_ses_email(s3_key)
            self.assertTrue(mock_smtp.called)
