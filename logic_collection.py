import scrape
import collection_stat
import datetime
import json
import os
import errno
import boto3

client = boto3.client('s3',
                        aws_access_key_id = os.getenv('AWSACCESSKEYID'),
                        aws_secret_access_key = os.getenv('AWSSECRETKEY'))

def uploadCollectionData(results):
   # initial filename per json output
   x = str(datetime.datetime.now().replace(microsecond=0)).replace(' ', '_')
   datestr = x.replace(':', '.')

   # filedir path 
   y = datetime.datetime.now().strftime("%D_%HH").replace('/', '-')

   # S3 bucket
   upload_file_bucket = 'snic-final-project'

   for item in results:
      # produce json strings for top 10 collections
      jsonstr = json.dumps(collection_stat.collection_data(item))

      filename = 'collection/'+y+'/'+item+'_'+datestr+'.json'

      upload_file_key = filename

      if not os.path.exists(os.path.dirname(filename)):
          try:
              os.makedirs(os.path.dirname(filename))
          except OSError as exc: # Guard against race condition
              if exc.errno != errno.EEXIST:
                  raise
      
      with open(filename, 'w') as f:
         f.write(jsonstr)

      with open(filename, 'rb') as f:
         client.upload_fileobj(f, upload_file_bucket, upload_file_key)

# main logic
results = scrape.get_top10_collections()
uploadCollectionData(results)
