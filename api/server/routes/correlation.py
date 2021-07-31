
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

@app.route("/correlation/<string:symbol>")
def correlation(symbol):
    """correlation route"""
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

    top = dict()
    top['target'] = symbol.upper() 
    top['correlation'] = dict()
    for tpl, corr in json.loads(au_corr.to_json()).items():
        pair = make_tuple(tpl)
        if symbol.lower() == pair[0].lower():
            top['correlation'].update({pair[1]: corr})

    top['correlation'] = dict(sorted(top['correlation'].items(), key=lambda item: item[1], reverse=True))

    return jsonify(top)
