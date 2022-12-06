#!/usr/bin/env python3
#
# ----- sample.py -----
# from httpscan import *
# data_list = HTTPVulnScan('https://example.com')

import traceback
import subprocess
import json
import hashlib
import sys
import random
import os
import logging
import requests
import validators
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv('.env')

logger = logging.getLogger('LF_WVS')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: {%(filename)s:%(lineno)d} - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

NUCLEI_BIN = os.getenv('NUCLEI_BIN')

def getChecksumID(string):
	try:
		real_string = '{string}'.format(string=string)
		uid = hashlib.md5(real_string.encode('utf-8')).hexdigest()
		return uid
	except Exception:
		logger.error(traceback.format_exc())
		return False

def valid_url_parse(URL):
	try:
		VALID_URL = urlparse(URL)
		if not VALID_URL.scheme == 'http' and not VALID_URL.scheme == 'https':
			logger.error(traceback.format_exc())
			return False
		PARSED_URL = VALID_URL.scheme + '://' + VALID_URL.netloc
		if not validators.url(PARSED_URL) == True:
			logger.error(traceback.format_exc())
			return False
		try:
			requests.get(PARSED_URL)
			return PARSED_URL
		except Exception:
			logger.error(traceback.format_exc())
			return False
	except Exception:
		logger.error(traceback.format_exc())
		return False

def read_nuclei_json_file(file):
	try:
		f = open(file)
		fcontents = f.read()
		f.close()
		items = []
		for fcontent in fcontents.split('\n'):
			try:
				data = json.loads(fcontent)
				timestamp = data['timestamp']
				try:
					del data['timestamp']
				except Exception:
					pass
				try:
					del data['template-url']
				except Exception:
					pass
				try:
					del data['info']['author']
				except Exception:
					pass
				try:
					del data['curl-command']
				except Exception:
					pass
				try:
					del data['template']
				except Exception:
					pass
				items.append(data)
			except Exception:
				pass
		return items
	except Exception:
		logger.error(traceback.format_exc())
		return False

def HTTPVulnScan(TARGET):
	try:
		VALID_URL = valid_url_parse(TARGET)
		if VALID_URL == False:
			return False
		RESULT_FILE = '/tmp/nuclei-{SCAN_ID}.json'.format(SCAN_ID=getChecksumID(random.randint(10000, 99999)))
		subprocess.run(['{NUCLEI_BIN}'.format(NUCLEI_BIN=NUCLEI_BIN), '-u', '{TARGET}'.format(TARGET=VALID_URL), '-retries', '3', '-json', '-o', '{RESULT_FILE}'.format(RESULT_FILE=RESULT_FILE)], capture_output=True, text=True)
		result = read_nuclei_json_file(RESULT_FILE)
		os.unlink(RESULT_FILE)
		return result
	except Exception:
		logger.error(traceback.format_exc())
		return False