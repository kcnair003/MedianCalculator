from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re
import time

class TranscriptCrawler():

    #Creates the MedianCrawler and gets the URL
    def __init__(self):
        URL = 'https://www.dartmouth.edu/reg/transcript/medians/'
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(URL, headers=hdr)
        try:
            self.page = urlopen(req)
        except HTTPError as e:
            if e.code == "500":
                time.sleep(5)
                self.page = urlopen(req)
            else:
                raise e

    #Scrapes web page for data
    def data_scraper(self):
        soup = BeautifulSoup(self.page, 'html.parser')
        results = soup.find('div', class_="b6")
        list_of_terms = results.find_all('a')
        terms = []
        for term in list_of_terms:
            term_link = term.get('href')
            terms.append(term_link[-8:])
        return terms