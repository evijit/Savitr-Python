from pymongo import MongoClient
import time
import pandas as pd
##
## reference file for benchmarking
##

def convert(data):
	'''
		gets singular dict, convert unicode to int / str
	'''
	l = []
	for k, v in data.items():
		if not isinstance(v, unicode):
			l.append((str(k), v))
		else:
			l.append((str(k), v.encode('utf8')))
	return dict(l)

def readmongo():
	start = time.time()
	client = MongoClient('localhost:27017')
	db = client.test
	cursor = db.all_tweets.find({})
	df = pd.DataFrame(list(cursor))
	# print df.iloc[0]

	# print len(df.index)
	end = time.time()
	print 'Time taken', end - start, 's'


if __name__ == '__main__':
	readmongo()