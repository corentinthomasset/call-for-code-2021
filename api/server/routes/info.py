
import logging
import json
import warnings
import time

from flask import jsonify, abort, Response, request
from server import app, cln_client

from cloudant.error import CloudantException, ResultException
from cloudant.query import Query

@app.route("/info/<string:symbol>")
def info(symbol):
    """info route"""
    if symbol is None or symbol == '':
        abort(Response(json.dumps({'Error': 'Invalid symbol provided'}), 400))

    reply = dict()

    dbs = {
           'details': 'ticker-details-ibm-cfc'
          }

    for aspect, db in dbs.items():
        try:
            conn = cln_client.create_database(db)
        except CloudantException as e:
            logging.critical(f'DB/{aspect} connection failure: {e}')
            reply[aspect] = {}
        else:
            if conn.exists():
                logging.info(f'Using existing {aspect} DB: {db}')
    
            selector={'cfc_company': symbol.upper()}
            try:
                resp = conn.get_query_result(selector,
                                             raw_result=True,
                                             limit=100)
                time.sleep(0.075)
            except ResultException as e:
                logging.critical(f'Query/{aspect} failed: {e}')
                abort(Response(json.dumps({'Error': 'Details not found for symbol'}), 400))
            else:
                if len(resp['docs']) == 0:
                    logging.warning(f'{aspect} not found for {symbol}')
                    abort(Response(json.dumps({'Error': 'Details not found for symbol'}), 400))

                result = list()
                for doc in resp['docs']:
                    result.append(doc)

    return jsonify(result)
