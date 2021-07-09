from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re
import time

class MedianCrawler():

    #Creates the MedianCrawler and gets the URL
    def __init__(self, term):
        self.term = term
        URL = 'https://www.dartmouth.edu/reg/transcript/medians/' + term
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
        medians = results.find_all('table')
        courses = medians[0].find_all('tr')
        departments = {}
        courses.pop(0)
        for course in courses:
            data = course.find_all('td')
            department_data =  data[1].renderContents().strip().decode('utf-8').split('-')
            department = department_data[0]
            median = data[3].renderContents().strip().decode('utf-8')
            if department in departments:
                departments.get(department).append(median)
            else:
                departments[department] = [median]
        return departments