#!/usr/local/bin/python3.6
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/demo/11sevendome/api/")

from app import app as application