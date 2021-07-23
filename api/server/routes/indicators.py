
import logging
import json

from flask import jsonify, abort, Response
from server import app, cln_client

from cloudant.error import CloudantException, ResultException
from cloudant.query import Query

@app.route("/indicators/<string:symbol>")
def indicators(symbol):
    if symbol is None or symbol == '':
        abort(Response(json.dumsp({'Error': 'Invalid symbol provided'}), 400))

    try:
        db = 'esg-indicators-ibm-cfc'
        conn = cln_client.create_database(db)
    except CloudantException as e:
        abort(Response(json.dumps({'Error': f'DB connection failure: {e}'}), 503))
    else:
        if conn.exists():
            logging.info(f'Using existing ratings DB: {db}')
    
    selector={'$text': symbol}
    try:
        resp = conn.get_query_result(selector,
                                     use_index='byStockSymbol',
                                     raw_result=True,
                                     limit=100)
    except ResultException as e:
        logging.critical(f'Query failed: {e}')
        abort(Response(json.dumps({'Error': f'DB query failed: {e}'}), 503))
    else:
        if len(resp['docs']) == 0:
            abort(Response(json.dumps({'Error': f'Stock symbol not found - {symbol}'}), 404))

        result = list()
        for doc in resp['docs']:
            result.append(doc)

        return jsonify(result)
