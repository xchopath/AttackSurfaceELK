#!/usr/bin/env python3
#
# from checkhttp import *
# result = checkHTTP('example.com')
# print(result)

import traceback
import subprocess
import logging
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv('.env')

logger = logging.getLogger('CHECK_HTTP')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: {%(filename)s:%(lineno)d} - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

HTTPX_BIN = os.getenv('HTTPX_BIN')

def checkHTTP(DOMAIN):
	try:
		target = subprocess.Popen(["echo", "{DOMAIN}".format(DOMAIN=DOMAIN)], stdout=subprocess.PIPE)
		get_http_list = subprocess.run(['{}'.format(HTTPX_BIN), '-timeout', '5', '-retries', '5', '-status-code', '-tech-detect', '-json', '-silent'], stdin=target.stdout, capture_output=True, text=True)
		result = []
		for http_list in get_http_list.stdout.split('\n'):
			if 'url' in http_list:
				data = json.loads(http_list)
				try:
					tech = data['tech']
				except Exception:
					tech = None
					pass
				try:
					content_type = data['content_type']
				except:
					content_type = None
					pass
				data_parsed = {'url': data['url'], 'status_code': data['status_code'], 'host': data['host'], 'port': data['port'], 'content_type': content_type, 'technologies': tech}
				result.append(data_parsed)
		if result == []:
			return None
		return result
	except Exception as Error:
		logger.error(traceback.format_exc())
		return False
