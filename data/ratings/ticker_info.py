import logging
import coloredlogs
import click
import attr
import json
import warnings
import time

from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

import yfinance as yf
import numpy as np
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
import pandas as pd

@attr.s
class Detail(object):
    companylist = attr.ib()
    cloudant_account = attr.ib() 
    cloudant_apikey = attr.ib()
    details_db = attr.ib(default='ticker-details-ibm-cfc')

    def register(self, backwards='1mo'):
        conn = self._cloudant_client(self.details_db)

        for company in self._company():
            detail = dict()
            detail['cfc_company'] = company

            ticker = yf.Ticker(company)
            info = ticker.info
            history = ticker.history(period=backwards)
            missing = list(yf.shared._ERRORS.keys())

            if len(missing) != 0:
                detail['info'] = {}
                detail['market_data'] = {}
            else:
                detail['info'] = info
                detail['market_data'] = json.loads(history.to_json(date_format='iso'))

            try:
                selector={'$text': company}
                avail = conn.get_query_result(selector,
                                              use_index='byStockSymbol',
                                              raw_result=True,
                                              limit=100)
            except ResultException as e:
                logging.critical(f'Query failed: {e}')
            else:
                if len(avail['docs']) == 0:
                    logging.info(f'Details for [{company}] has not been previously processed ... adding')
                    if conn.create_document(detail).exists():
                        logging.info(f'Details for [{company}] stored in DB')
                        time.sleep(0.3)
                else:
                    logging.warning(f'Details for [{company}] has been previously processed ... skipping')

    def _cloudant_client(self, db):
        try:
            client = Cloudant.iam(self.cloudant_account,
                                  self.cloudant_apikey,
                                  connect=True)
            
            conn = client.create_database(db)
        except CloudantException as e:
            logging.critical(f'Error connecting to Cloudant: {e}')
            return None
        else:
            if conn.exists():
                logging.info(f'Using Cloudant database: {db}')
                return conn 
            else:
                return None

    def _company(self):
        for line in self.companylist.readlines():
            yield line.decode('utf-8').split('\t')[0].strip()

@click.command()
@click.argument('companylist',
                type=click.File('rb'),
                required=True)
@click.option('--cloudant-account',
              type=str,
              required=True,
              default='77ff9972-4847-45e6-90bc-40060f23f6a0-bluemix', 
              help='IBM Cloudant account')
@click.option('--cloudant-api-key',
              type=str,
              required=True,
              help='IBM Cloudant API key')
@click.option('-d',
              '--debug',
              type=bool,
              required=False,
              default=False,
              is_flag=True,
              help='Show debug messages')
def main(companylist,
         cloudant_account,
         cloudant_api_key,
         debug):
    """
    Store company details (info and market data) to IBM Cloudant 

    COMPANYLIST is a file containing company names.
    """

    logging.basicConfig(level=(logging.DEBUG if debug else logging.INFO),
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    coloredlogs.install(level=('DEBUG' if debug else 'INFO'))
    symbol_detail = Detail(companylist,
                           cloudant_account,
                           cloudant_api_key)
    symbol_detail.register()

if __name__ == '__main__':
    main()
