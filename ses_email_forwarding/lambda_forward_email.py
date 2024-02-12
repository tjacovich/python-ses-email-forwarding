"""
Copy this file into the lambda_function.py file in the lambda function editor.
"""
import smtplib, email
import boto3
import json
import os

def lambda_handler(event, context):
    """
    params:
        dict event: A JSON-formatted document that contains data for a Lambda function to process.
        object context: Methods and properties that provide information about the invocation, function, and runtime environment.

    Called by lambda to handle lambda events.
    See AWS documentation for more details.
    """
    for record in event['Records']:
        process_message(record)
    print("done")

def process_message(record):
    """
    params:
        dict record: The parsed record from the lambda handler.
    
    Processor for individual records sent within lambda events. 
    """
    try:
        s3_key = record['s3']['object']['key']
        print(f"Extracted S3 object key: {s3_key} from forwarded S3 event.")
        forward_ses_email(s3_key)
        
    except Exception as e:
        print("An error occurred")
        raise e

def forward_ses_email(s3_key):
    """
    params: 
        string s3_key: The S3 object key for the email file

    return:
        None

    Collects email file from S3 Object store. 
    Modifies the email to use SES SMTP with user defined sender and recipient.
    Sends email based on user supplied SMTP configuration.

    requires the folowing be defined in the environment (See config.sh):
        smtp_server
        to_addr
        user
        passwd
        bucket
        from_addr
    """

    #Get bucket name from environment
    bucket = os.environ['bucket']

    #Start S3 client. This will fail if $HOME/.aws/credentials does not exist. Follow steps for awscliv2 
    s3_client = boto3.client('s3')

    #read email from s3 bucket and store it as utf-8 string.
    raw_email=s3_client.get_object(Bucket=bucket, Key=s3_key)['Body'].read().decode('utf-8')
    
    # create a Message instance from the email string
    message = email.message_from_string(raw_email)
    
    #save the original sender for the Reply-to field
    reply_to = message["From"]

    #Get sending address (from_addr) and receiving address (to_addr) from environment
    from_addr = os.environ['from_addr']
    to_addr = os.environ['to_addr']

    #Update from address to retain original sender name if possible
    from_addr = str(reply_to.split("<")[0][:-1])+" <"+str(from_addr)+">"

    #Update email header fields
    message.replace_header("To", to_addr)
    message.replace_header("From", from_addr)
    message.replace_header("Return-Path", from_addr)

    #Add Sender and reply-to header fields
    message.add_header("Sender", from_addr)
    message.add_header('reply-to', reply_to)

    #SMTP credentials
    smtp_host = os.environ['smtp_server']
    smtp_port = 587
    user = os.environ['user']
    passwd = os.environ['passwd']

    #Open Connection to SMTP server, login, and send the email
    smtp = smtplib.SMTP(smtp_host, smtp_port)
    smtp.starttls()
    smtp.login(user, passwd)
    smtp.sendmail(from_addr, to_addr, message.as_string())
    smtp.quit()