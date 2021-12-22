import boto3
import os
import datetime

# initialise boto3
def client_init():
    client = boto3.client('s3',
                        aws_access_key_id = os.getenv('AWSACCESSKEYID'),
                        aws_secret_access_key = os.getenv('AWSSECRETKEY'))
    return client

# get bucket name
def bucket_name():
    # S3 bucket
    upload_file_bucket = 'snic-final-project'
    return upload_file_bucket

# create filedate names
def filedate_init():
   # initial filename per json output
   now = datetime.datetime.now()
   x = str(now.replace(microsecond=0)).replace(' ', '_')
   datestr = x.replace(':', '.')

   # filedir path 
   y = now.strftime("%D_%HH").replace('/', '-')

   return [x,y] 