#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv('.env')

ELASTIC_USER = os.getenv('ELASTIC_USER')
ELASTIC_PASS = os.getenv('ELASTIC_PASS')
ELASTIC_SCHEME = os.getenv('ELASTIC_SCHEME')
ELASTIC_HOST = os.getenv('ELASTIC_HOST')
ELASTIC_PORT = os.getenv('ELASTIC_PORT')

elastic = Elasticsearch([{'scheme': '{}'.format(ELASTIC_SCHEME), 'host': '{}'.format(ELASTIC_HOST), 'port': int(ELASTIC_PORT)}], basic_auth=(ELASTIC_USER, ELASTIC_PASS))
