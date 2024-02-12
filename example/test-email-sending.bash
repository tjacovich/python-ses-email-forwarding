#!/bin/bash

#Activate the environment for the processor
export $(grep -v '^#' ./local_config.sh | xargs)

#Set PYTHONPATH
export PYTHONPATH='../'

#Object key provided on the command line
S3_OBJECT_KEY=$@

#call test script with passed object key
python3 example/test_email_sending.py $S3_OBJECT_KEY