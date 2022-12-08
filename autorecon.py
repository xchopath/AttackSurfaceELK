#!/usr/bin/env python3 

from functions.enumsubdomain import *
from functions.checkhttp import *
from functions.checkdns import *
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

def doRecon(domain):
	subdomains = enumSubdomain(domain)
	for subdomain in subdomains:
		try:
			http = checkHTTP(subdomain)
			if not http == None:
				for data in http:
					data['checksum'] = getChecksumID(json.dumps(data))
					data['timestamp'] = datetime.datetime.now().isoformat()
					es_index = 'assethttp'
					_id = data['checksum']
					doc_data = json.dumps(data)
					if not elastic.exists(index="{index}".format(index=es_index), id="{_id}".format(_id=_id)):
						elastic.index(index="{index}".format(index=es_index), id="{_id}".format(_id=_id), document=doc_data)
						print('INFO:', es_index, data['url'], 'insert successfully')
					else:
						print('INFO:', es_index, data['url'], 'is duplicate')
		except Exception:
			pass
		try:
			dns = checkDNS(subdomain)
			dns['checksum'] = getChecksumID(json.dumps(dns))
			dns['timestamp'] = datetime.datetime.now().isoformat()
			_id = dns['checksum']
			es_index = 'assetdomain'
			doc_data = json.dumps(dns)
			if not elastic.exists(index="{index}".format(index=es_index), id="{_id}".format(_id=_id)):
				elastic.index(index="{index}".format(index=es_index), id="{_id}".format(_id=_id), document=doc_data)
				print('INFO:', es_index, dns['host'], 'insert successfully')
			else:
				print('INFO:', es_index, dns['host'], 'is duplicate')
		except Exception:
			pass

f = open('domains.lst', 'r')
domains = f.read()
f.close()

for domain in domains.split('\n'):
	print(domain)
	doRecon(domain)
