#!/usr/bin/env python3

from functions.httpscan import *
from functions.elastic import *
import hashlib
import datetime
import json

# check_dns = checkDNS('example.com')
# check_http = checkHTTP('example.com')
# subdomains = enumSubdomain('example.com')

def getChecksumID(string):
	try:
		real_string = '{string}'.format(string=string)
		uid = hashlib.md5(real_string.encode('utf-8')).hexdigest()
		return uid
	except Exception:
		logger.error(traceback.format_exc())
		return False

res = elastic.search(index="assethttp", body={"query": {"match_all": {}}, 'size': 10000})
for i in res['hits']['hits']:
	try:
		target = i['_source']['url']
		results = HTTPVulnScan(target)
		for result in results:
			result['checksum'] = getChecksumID(json.dumps(result))
			result['timestamp'] = datetime.datetime.now().isoformat()
			_id = result['checksum']
			es_index = 'httpscan'
			doc_data = json.dumps(result)
			try:
				if not elastic.exists(index="{index}".format(index=es_index), id="{_id}".format(_id=_id)):
					elastic.index(index="{index}".format(index=es_index), id="{_id}".format(_id=_id), document=doc_data)
					print('INFO:', es_index, target, 'insert successfully')
				else:
					print('INFO:', es_index, target, 'is duplicate')
			except Exception:
				pass
	except Exception:
		pass