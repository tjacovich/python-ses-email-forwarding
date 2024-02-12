from ses_email_forwarding.lambda_forward_email import process_message
import argparse
import os

#CLI parser defined for handling the S3 Object key.
parser = argparse.ArgumentParser(
                    prog='process_message',
                    description='process a test message from an S3 bucket and send a test email from Amazon SES')

#S3 key provided on the command line.
parser.add_argument('key')
args = parser.parse_args()

#Test record.
record = {"s3": {"object":{"key": args.key}}}

#We bypass the lambda handler for this test and pass the parsed record directly to the processer.
process_message(record)