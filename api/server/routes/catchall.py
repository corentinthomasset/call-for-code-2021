
import logging
import json
import warnings
import time
import datetime as dt
from ast import literal_eval as make_tuple

from flask import jsonify, abort, Response, request
from server import app, cln_client

from cloudant.error import CloudantException, ResultException
from cloudant.query import Query

import yfinance as yf
import numpy as np
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
import pandas as pd

def ticker_details(symbol, backwards):
    reply = dict()

    dbs = {
           'ratings': 'esg-ratings-ibm-cfc',
           'indicators': 'esg-indicators-ibm-cfc',
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
    
            selector={'$text': symbol}
            try:
                resp = conn.get_query_result(selector,
                                             use_index='byStockSymbol',
                                             raw_result=True,
                                             limit=100)
                #time.sleep(0.3)
            except ResultException as e:
                logging.critical(f'Query/{aspect} failed: {e}')
                reply[aspect] = {}
            else:
                if len(resp['docs']) == 0:
                    logging.warning(f'{aspect} not found for {symbol}')
                    reply[aspect] = {}
                else:
                    result = list()
                    for doc in resp['docs']:
                        result.append(doc)
                    reply[aspect] = result

    return reply

@app.route("/catchall/<string:symbol>")
def catchall(symbol):
    """catchall route"""
    if symbol is None or symbol == '':
        abort(Response(json.dumps({'Error': 'Invalid symbol provided'}), 400))

    backwards = request.args.get('period', '1mo')

    pd.set_option('display.max_rows', None)
    warnings.filterwarnings("ignore")
    yf.pdr_override()

    num_of_years = 1
    start = dt.date.today() - dt.timedelta(days = int(365.25*num_of_years))
    end = dt.date.today()

    tickers = si.tickers_dow()
    tickers.append(symbol)
    dataset = pdr.get_data_yahoo(tickers, start, end)['Adj Close']
    stocks_returns = np.log(dataset/dataset.shift(1))

    pairs_to_drop = set()
    cols = stocks_returns.columns
    for i in range(0, stocks_returns.shape[1]):
        for j in range(0, i+1):
            if i == j:
                pairs_to_drop.add((cols[i], cols[j]))

    au_corr = stocks_returns.corr().abs().unstack()
    au_corr = au_corr.drop(labels=pairs_to_drop)

    final = list()
    for ticker in tickers:
        top = dict()
        top['target'] = ticker
        top['correlation'] = dict()
        for tpl, corr in json.loads(au_corr.to_json()).items():
            pair = make_tuple(tpl)
            if ticker.lower() == pair[0].lower():
                top['correlation'].update({pair[1]: corr})

        top['correlation'] = dict(sorted(top['correlation'].items(), key=lambda item: item[1], reverse=True))
        final.append(top)

    for item in final:
        if item['target'].lower() == symbol.lower():
            item.update(ticker_details(symbol, backwards))
            item['correlations'] = list()
            for corp, corr_value in item['correlation'].items():
                corr_item = dict()
                corr_item['symbol'] = corp
                corr_item['value'] = corr_value
                corr_item.update(ticker_details(corp, backwards))
                item['correlations'].append(corr_item)
            del item['correlation']
            return jsonify(item)
            break
    else:
        abort(Response(json.dumps({'Error': 'Stock/Correlation/ESG details not found for symbol'}), 400))

