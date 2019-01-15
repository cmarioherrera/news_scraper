import argparse
import logging
from common import config

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def _news_scraper(news_site_uid):
    hots = config()['news_sites'][news_site_uid]['url']
    logging.info('Begining scraper for {} '.format(hots))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    news_site_chioces = list(config()['news_sites'].keys())

    parser.add_argument('news_site', 
                        help='The news site that want to scrape',
                        type=str,
                        choices=news_site_chioces)

    args = parser.parse_args()
    _news_scraper(args.news_site)                    