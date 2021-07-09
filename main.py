from os import error
import requests
import time
from bs4 import BeautifulSoup
from transcript_crawler import TranscriptCrawler
from median_crawler import MedianCrawler
import statistics

#Prints lines in animated sequence
def delay_print(item):
    for character in item:
        print(character, end='', flush=True)
        time.sleep(0.05)

#Converts lists into string; USED:Summoners,Runes
def list_to_string(list):
    final_string=""
    for thing in list:
        final_string+=thing
        if(thing != list[-1]):
            final_string+=", "
    return final_string
        
#Converts list into fancy string; USED: Build
def list_to_build(list):
    final_string=""
    for item in list:
        final_string+=item
        if(item != list[-1]):
            final_string+=" -> "
    return final_string

#This is the main method that runs the code
def main():
    try:
        list_of_terms = TranscriptCrawler().data_scraper()
        departments = {}
        for term in list_of_terms:
            median = MedianCrawler(term).data_scraper()
            for department in median.keys():
                if department in departments:
                    departments.get(department).extend(median.get(department))
                else:
                    departments[department] = median.get(department)
        median_averages = {}
        weights = {'A': 12/3, 'A/A-': 23/6, 'A-': 11/3, 'A-/B+': 21/6, 'B+': 10/3, 'B+/B':  19/6, 'B': 9/3, 'B/B-': 17/6, 'B-': 8/3, 'B-/C+': 15/6, 'C+': 7/3, 'C+/C': 13/6, 'C': 6/3, 'C/C-': 11/6, 'C-': 5/3, 'D': 3/3, 'E': 0}
        for department in departments.keys():
            medians = departments.get(department)
            grades = []
            for grade in medians:
                grades.append(weights.get(grade))
            median_averages[department] = statistics.mean(grades)
        median_averages_sorted = sorted(median_averages.items(), key=lambda item: item[1], reverse=True)
        for dept, average in median_averages_sorted:
            print(dept, round(average,2))
    except Exception as e:
        print(e)


main()