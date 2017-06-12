#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")

from FlaskApp import app as application
application.secret_key = 'dsasafsafdsnjofbiwer8yfgc3479fe76f5x53ez5tzew4zr8e6237'