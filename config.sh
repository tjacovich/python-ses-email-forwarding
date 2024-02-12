#####################################################################
##Copy to local_config.sh and then fill out the correct information##
#####################################################################

smtp_server="email-smtp.<AWS_SES_REGION>.amazonaws.com"
to_addr=<SES_TO_EMAIL_ADDRESS>
user=<AWS_SES_SMTP_USER_KEY>
passwd=<AWS_SES_SMTP_USER_PASSWORD>
bucket=<SES_EMAIL_BUCKET_NAME>
from_addr=<SES_FROM_EMAIL_ADDRESS>