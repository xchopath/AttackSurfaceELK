#!/usr/bin/env python3
#
# from checkdns import *
# result = checkDNS('example.com')
# print(result)

import traceback
import subprocess
import logging
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv('.env')

logger = logging.getLogger('CHECK_DNS')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: {%(filename)s:%(lineno)d} - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

DNSX_BIN = os.getenv('DNSX_BIN')

def checkDNS(DOMAIN):
	try:
		domain = subprocess.Popen(["echo", "{DOMAIN}".format(DOMAIN=DOMAIN)], stdout=subprocess.PIPE)
		get_dns = subprocess.run(['{}'.format(DNSX_BIN), '-a', '-aaaa', '-cname', '--resp', '-retry', '3', '-json', '-silent'], stdin=domain.stdout, capture_output=True, text=True)
		data = json.loads(get_dns.stdout)
		timestamp = data['timestamp']
		del data['timestamp']
		del data['resolver']
		del data['all']
		return data
	except Exception:
		logger.error(traceback.format_exc())
		return False