import logging
import click
import attr
import aiohttp
import aiofiles
import asyncio
import json

from cloudant.client import Cloudant
from cloudant.result import Result, ResultByKey

@attr.s
class ESG(object):
    companylist = attr.ib()

    esg_api_key = attr.ib(default='a2305eb507f4e7b1c9f2c457927094b8') 
    esg_api_host = attr.ib(default='tf689y3hbj.execute-api.us-east-1.amazonaws.com/prod/authorization')

    cloudant_account = attr.ib(default='77ff9972-4847-45e6-90bc-40060f23f6a0-bluemix') 
    cloudant_apikey = attr.ib(default='h4ZvVEx8ky1Q_LMpQ67jWUVtL0KBsQ-HNXECpfKYK_il')

    ratings_db = attr.ib(default='esg-ratings-ibm-cfc')
    indicators_db = attr.ib(default='esg-indicators-ibm-cfc')

    def _cloudant_client(self, db):
        client = Cloudant.iam(self.cloudant_account,
                              self.cloudant_apikey,
                              connect=True)
        
        conn = client.create_database(db)
        if conn.exists():
            logging.info(f'Using Cloudant database: {db}')
            return conn 
        else:
            return None

    async def _query(self):
        endpoints = {
                     'indicator': {
                                    'url': f'https://{self.esg_api_host}/goals',
                                    'db': self._cloudant_client(self.indicators_db)
                                  },
                     'rating': {
                                 'url': f'https://{self.esg_api_host}/search',
                                 'db': self._cloudant_client(self.ratings_db)
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
                    async with session.get(spec['url'], params=payload) as resp:
                    #async with session.get('https://api.github.com/events') as resp:
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
@click.option('-d',
              '--debug',
              type=bool,
              required=False,
              default=False,
              show_default=True,
              help='Show debug messages')
def main(companylist,
         debug):
    """
    Extract ESG ratings for given companies using ESG Enterprise API

    COMPANYLIST is a file containing company names.
    """

    logging.basicConfig(level=(logging.DEBUG if debug else logging.INFO),
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    esg = ESG(companylist)
    esg.crawl()

if __name__ == '__main__':
    main()
