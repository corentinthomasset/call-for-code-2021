import logging
import coloredlogs
import click
import attr
import aiohttp
import aiofiles
import asyncio
import json

from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

@attr.s
class ESG(object):
    companylist = attr.ib()

    esg_api_key = attr.ib() 
    esg_api_host = attr.ib()

    cloudant_account = attr.ib() 
    cloudant_apikey = attr.ib()

    check = attr.ib()
    check_url = attr.ib(default='https://api.github.com/events')
    check_db = attr.ib(default='check_db')

    ratings_db = attr.ib(default='esg-ratings-ibm-cfc')
    indicators_db = attr.ib(default='esg-indicators-ibm-cfc')

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

    async def _query(self):
        endpoints = {
                     'indicator': {
                                    'url': (self.check_url if self.check else f'https://{self.esg_api_host}/goals'),
                                    'db': (self._cloudant_client(self.check_db) if self.check else self._cloudant_client(self.indicators_db))
                                  },
                     'rating': {
                                 'url': (self.check_url if self.check else f'https://{self.esg_api_host}/search'),
                                 'db': (self._cloudant_client(self.check_db) if self.check else self._cloudant_client(self.ratings_db))
                               }
                    } 
        async with aiohttp.ClientSession() as session:
            for company in self._company():
                payload = {
                           'q': company,
                           'token': self.esg_api_key
                          } 
                logging.info(f'Company: {company}')
                for endpoint, spec in endpoints.items():
                    logging.info(f'Querying ESG [{endpoint}] for [{company}] ...')
                    try:
                        async with session.get(spec['url'], params=payload) as resp:
                            if resp.status == 200:
                                if spec['db'] is None:
                                    result = await aiofiles.open(f'{company}_{endpoint}.json',
                                                                 mode='w',
                                                                 encoding='utf-8')
                                    await result.write(json.dumps(await resp.json(), indent=2))
                                    await result.close()
                                    logging.info(f'[{endpoint}] for [{company}] saved as: {company}_{endpoint}.json')
                                else:
                                    docs = await resp.json()
                                    for doc in docs:
                                        if spec['db'].create_document(doc).exists():
                                            await asyncio.sleep(0.5)
                                            logging.info(f'[{endpoint}] for [{company}] stored in DB')
                            else:
                                logging.error(f'Request failed for [{company}] ({resp.status}): {resp.text}')
                    except Exception as e:
                        logging.critical(f'Operation failed for [{company}]: {e}')
    
    def crawl(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._query())
        loop.run_until_complete(asyncio.sleep(0.250))
        loop.close()

    def _company(self):
        for line in self.companylist.readlines():
            yield line.decode('utf-8').split('\t')[0]

@click.command()
@click.argument('companylist',
                type=click.File('rb'),
                required=True)
@click.option('--esg-api-key',
              type=str,
              required=True,
              help='ESG Enterprise API key')
@click.option('--esg-api-host',
              type=str,
              required=False,
              default='tf689y3hbj.execute-api.us-east-1.amazonaws.com/prod/authorization',
              show_default=True,
              help='ESG Enterprise API host')
@click.option('--cloudant-account',
              type=str,
              required=True,
              default='77ff9972-4847-45e6-90bc-40060f23f6a0-bluemix', 
              help='IBM Cloudant account')
@click.option('--cloudant-api-key',
              type=str,
              required=True,
              help='IBM Cloudant API key')
@click.option('-c',
              '--check',
              type=bool,
              required=False,
              default=False,
              is_flag=True,
              help='Check settings')
@click.option('-d',
              '--debug',
              type=bool,
              required=False,
              default=False,
              is_flag=True,
              help='Show debug messages')
def main(companylist,
         esg_api_key,
         esg_api_host,
         cloudant_account,
         cloudant_api_key,
         check,
         debug):
    """
    Extract ESG ratings for given companies using ESG Enterprise API

    COMPANYLIST is a file containing company names.
    """

    logging.basicConfig(level=(logging.DEBUG if debug else logging.INFO),
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    coloredlogs.install(level=('DEBUG' if debug else 'INFO'))
    esg = ESG(companylist,
              esg_api_key,
              esg_api_host,
              cloudant_account,
              cloudant_api_key,
              check)
    esg.crawl()

if __name__ == '__main__':
    main()
