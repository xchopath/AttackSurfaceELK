#!/usr/bin/env python3
#
# from enumSubdomain import *
# subdomains = enumSubdomain('example.com')
# print(subdomains)

import os
import sys
import subprocess
import traceback
import logging
from dotenv import load_dotenv

load_dotenv('.env')

logger = logging.getLogger('SUBFINDER')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: {%(filename)s:%(lineno)d} - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

SUBFINDER_BIN = os.getenv('SUBFINDER_BIN')

def enumSubdomain(DOMAIN):
	try:
		SUBFINDER = subprocess.check_output(['{}'.format(SUBFINDER_BIN), '-d', '{}'.format(DOMAIN), '-recursive', '-silent'])
		SUBDOMAINS = []
		for SUBDOMAIN in SUBFINDER.decode('ascii').split():
			SUBDOMAINS.append(SUBDOMAIN)
		SUBDOMAINS.append(DOMAIN)
		TMP_SUBDOMAINS = SUBDOMAINS
		SUBDOMAINS = []
		[ SUBDOMAINS.append(SUBDOMAIN) for SUBDOMAIN in TMP_SUBDOMAINS if SUBDOMAIN not in SUBDOMAINS ]
		return SUBDOMAINS
	except Exception:
		logger.error(traceback.format_exc())
		return False