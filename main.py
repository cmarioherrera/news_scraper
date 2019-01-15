import argparse
import logging
import re

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

import news_page_objects as news
from common import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_well_formed_link = re.compile(r'^https?://.+/.+') #https://exampla.com/hello
is_root_path = re.compile(r'^/.+$') # /somte-text

def _news_scraper(news_site_uid):
    hots = config()['news_sites'][news_site_uid]['url']
    logging.info('Begining scraper for {} '.format(hots))
    homepage = news.HomePage(news_site_uid,hots)
    

    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid,hots,link)

        if article:
            logger.info('Article fetched!!!')
            articles.append(article)
            print(article.title)
    print('Numbers of articles {}'.format(len(articles)))


def _fetch_article(news_site_uid,host,link):
    logger.info('Start fetching article at {}'.format(link))
    article = None
    try:
        article = news.ArticlePage(news_site_uid,_build_link(host,link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error while fetching the article', exc_info=False)

    if article and not article.body:
        logger.warning('Invalid article. There is no body')
        return None

    return article    
        

def _build_link(host,link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host,link)
    else:
        return '{hots}/{uri}'.format(host=host, uri=link)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    news_site_chioces = list(config()['news_sites'].keys())

    parser.add_argument('news_site', 
                        help='The news site that want to scrape',
                        type=str,
                        choices=news_site_chioces)

    args = parser.parse_args()
    _news_scraper(args.news_site)                    