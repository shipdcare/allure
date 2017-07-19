#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.stdout = sys.stderr
sys.path.insert(0,"/var/www/allure/")

from allure import app as application
application.secret_key = 'Add your secret key'