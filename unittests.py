# Unit tests
import logging
from botocore.client import ClientError

def scraperreturn(results):
	assert(len(results) == 10)

def checkBucketAccess(client, bucketname):
	try:
		client.head_bucket(Bucket=bucketname)
	except Exception as Argument:
		f = open("logfile_clientbucket.txt", "a")
		f.write(str(Argument))
		f.close()
		raise Exception("Unable to connect to bucket")