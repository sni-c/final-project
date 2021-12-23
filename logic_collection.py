import scrape
import collection_stat
import json
import os
import errno
import unittests
import bucket_init

def uploadCollectionData(results):
   # get today's dates for filenames
   datestr = bucket_init.filedate_init()[0]
   y = bucket_init.filedate_init()[1]

   for item in results:
      # produce json strings for top 10 collections
      jsonstr = json.dumps(collection_stat.collection_data(item))

      filename = 'raw_collection/'+y+'/'+item+'_'+datestr+'.json'

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
   return filename

# main logic
client = bucket_init.client_init()
upload_file_bucket = bucket_init.bucket_name()

unittests.checkBucketAccess(client, upload_file_bucket)
results = scrape.get_top10_collections()

unittests.scraperreturn(results)
uploadCollectionData(results)

