import logging
import newspaper

import requests
from bs4 import BeautifulSoup

import urllib2

log = logging.getLogger(__name__)

class siteScraper:

    def scrape_stories(self):
        try:
            response = requests.get("http://www.bbc.co.uk/")
            soup = BeautifulSoup(response.content)
            print soup

        except Exception as e:
            print e

x = siteScraper()
x.scrape_stories()