import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from shutil import which
from selenium.webdriver.common.keys import Keys
# for Headless
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import requests


class UpSpider(scrapy.Spider):
    name = 'usps'
    allowed_domains = ['usps.com']
    start_urls = ['https://www.usps.com']



    def parse(self, response):
        link = 'http://ot.michaelelectronics2.com/Cglobal/getTracking/1'
        res = requests.get(link).json()

        for ven in res:
            if ven['vendor'] == 'USPS':
                id = ven['tracking']
                print('\n USPS ID = ', id)

                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_path = which("chromedriver")

                # driver = webdriver.Chrome(executable_path=chrome_path)
                driver = webdriver.Chrome(executable_path=chrome_path)
                driver.get("https://www.usps.com/manage/")
                import time
                time.sleep(5)
                search_input = driver.find_element_by_xpath('//*[@id="track-package--input"]')
                search_input.send_keys(id)
                time.sleep(3)
                search_btn = driver.find_element_by_xpath('//*[@id="track-package--form"]/div/input[2]')
                search_btn.click()

                time.sleep(15)
                status = driver.find_element_by_xpath(
                    '//*[@id="tracked-numbers"]/div/div/div/div/div[1]/div[2]/h2/strong').text
                print('Status = ', status)

                def listToString(s):
                    str1 = ""
                    for ele in s:
                        str1 += ' ' + ele
                    return str1

                if status == 'Delivered':
                    full_date = driver.find_element_by_xpath('//*[@id="tracked-numbers"]/div/div/div/div/div[1]/div[2]/div/p[1]').text.split()[0:3]
                    day = ''
                    date =  listToString(full_date)
                    t = driver.find_element_by_xpath(
                        '//*[@id="tracked-numbers"]/div/div/div/div/div[1]/div[2]/div/p[1]').text.split()[4:]
                    time = listToString(t)

                    location = driver.find_element_by_xpath('//*[@id="tracked-numbers"]/div/div/div/div/div[1]/div[2]/div/p[3]').text
                    leftat = ''
                    Received = ''

                if status == 'Status Not Available':
                    day = ''
                    date = ''
                    time = ''
                    location = ''
                    leftat = ''
                    Received = ''

                yield {
                'tracking': str(id),
                'status': status,
                'date': date,
                'day': day,
                'time': time,
                'location': location,
                'left_at': leftat,
                'receiver': Received
                }
                driver.close()

    print("End\n\n")
