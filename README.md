## SES Email Forwarder

### Introduction
This is the definition of an AWS lambda function for forwarding emails sent to an SES email address and forwarded to an S3 Bucket. The lambda function is designed to be triggered on any PUT call to the specific S3 bucket. The actual lambda function is defined in `lambda_forward_email.py`.

### Testing
In the `example` folder there are two scripts`
- `test-email-sending.bash`: A bash that exports the config file `local_config.sh` to the shell and then calls `test_email_sending.py`
- `test_email_sending.py`: A python script that calls the `process_message` function from `ses_email_forwarding.lambda_forward_email` on a test S3 Object key.

The example script can be invoked using: 
```bash
$ ./example/test-email-sending.bash $S3_OBJECT_KEY
```

In order for this to work a `python3` virtual environment should first be created using
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```
the following things must be configured:
```bash
#This is needed for boto3 to be able to connect to S3
$ awscliv2 configure
#Alternatively, you can directly create $HOME/.aws/credentials
```

[SES email forwarding](https://repost.aws/knowledge-center/ses-receive-inbound-emails) must be set up to send emails to an S3 bucket, and SES must also be enabled to [send emails programatically](https://docs.aws.amazon.com/ses/latest/dg/send-using-smtp-programmatically.html).

Once `awscliv2` and `SES` email storage and sending are configured, the next step is to create the `local_config.sh` file. Simply run
```bash
$ cp config.sh local_config.sh
```
and then write the relevant values into the environment variables in `local_config.sh`.
Note: `from_addr` must be an email address or domain registered with amazon SES.

As final note, in order for the example script to work, `S3_OBJECT_KEY` must be an object that exists in the SES email bucket.

### Deployment
When to deploying to a lambda function, all the values defined in `config.sh` must be defined as environment variables in the lambda function, and the lambda function must be set up to trigger on `PUT` requests to the S3 bucket, and the IAM role must have a [policy](https://repost.aws/knowledge-center/lambda-execution-role-s3-bucket) added that gives it `List` and `Get` access permissions for the relevant bucket. The contents of `ses_email_forwarding/lambda_forward_email.py` can then be copied into `lambda_function.py` and the function can be tested and deployed.

### Development
***COMING SOON***

### Maintainers
Taylor Jacovich <tjacovich@astrophysicist-adjacent.com>
