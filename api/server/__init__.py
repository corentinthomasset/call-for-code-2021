import os
import sys
import logging
from flask import Flask, abort, session, request, redirect
from flask.json import jsonify
from flask_cors import CORS

import atexit

from cloudant.client import Cloudant
from cloudant.error import CloudantException

logging.basicConfig(level=logging.INFO)
app = Flask(__name__, template_folder="../public", static_folder="../public", static_url_path='')
app.config['JSON_SORT_KEYS'] = False
CORS(app)

try:
    cln_client = Cloudant.iam('77ff9972-4847-45e6-90bc-40060f23f6a0-bluemix',
                              'h4ZvVEx8ky1Q_LMpQ67jWUVtL0KBsQ-HNXECpfKYK_il',
                              connect=True)
except CloudantException as e:
    logging.critical(f'Error connecting to Cloudant: {e}')
    sys.exit(1)
else:
    logging.info('Successfully connected to IBM Cloudant')

from server.routes import *
from server.services import *

initServices(app)

if 'FLASK_LIVE_RELOAD' in os.environ and os.environ['FLASK_LIVE_RELOAD'] == 'true':
	import livereload
	app.debug = False
	server = livereload.Server(app.wsgi_app)
	server.serve(port=os.environ['port'], host=os.environ['host'])

@atexit.register
def shutdown():
    if cln_client:
        logging.info('Closing Cloudant connection ...')
        cln_client.disconnect()
