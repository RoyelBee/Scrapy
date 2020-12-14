import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from shutil import which
from selenium.webdriver.common.keys import Keys
# for Headless
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests
import json


class UpSpider(scrapy.Spider):
    name = 'fed1'
    allowed_domains = ['fedex.com']
    start_urls = ['http://fedex.com/']

    def parse(self, response):
        link = 'http://ot.michaelelectronics2.com/Cglobal/getTracking/1'
        res = requests.get(link).json()
        fed_tracking_id = []
        for val in res:
            if val['vendor'] == 'FedEx':
                fed_tracking_id.append(val['tracking'])
        print(fed_tracking_id)

        # ids = ['914024657736', '914024657780']
        # fed_tracking_id = ['914024657736']

        for id in fed_tracking_id:
            print('Tracking id: ', id, '\n')

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_path = which("chromedriver")

            # driver = webdriver.Chrome(executable_path=chrome_path)
            driver = webdriver.Chrome(executable_path=chrome_path)  # , chrome_options=chrome_options
            driver.get("https://www.fedex.com/apps/fedextrack/?action=track")

            import time
            time.sleep(20)

            search_input = driver.find_element_by_xpath('//*[@id="track_inbox_track_numbers_area"]')
            search_input.send_keys(id)

            time.sleep(2)
            search_btn = driver.find_element_by_xpath('//*[@id="number"]/div/form/div/div/form/div[1]/div/button')
            time.sleep(2)
            search_btn.click()

            time.sleep(20)

            delevery = driver.find_element_by_xpath(
                '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[2]/h1/div[1]').text

            if delevery == 'Delivered':
                status = delevery
                day = driver.find_element_by_xpath(
                    '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[2]/h1/div[2]').text.split()[
                    0]
                t1 = driver.find_element_by_xpath(
                    '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[2]/h1/div[2]').text.split()[
                    3]
                t2 = driver.find_element_by_xpath(
                    '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[2]/h1/div[2]').text.split()[
                    4]
                times = t1 + ' ' + t2
                dates = driver.find_element_by_xpath(
                    '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[2]/h1/div[2]').text.split()[
                    1]
                signed_by = driver.find_element_by_xpath(
                    '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[2]/div[5]/div/h3[3]').text.split()[
                    3]
                to = driver.find_element_by_xpath(
                    '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[6]/div[2]/div/p[6]').text

                froms = driver.find_element_by_xpath(
                    '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[6]/div[1]/div/p[6]').text


                print("End\n\n")
                time.sleep(2)
                travel_history = ''

            # # Level 02
            pending = driver.find_element_by_xpath(
                '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[2]/h1/div[2]').text

            if pending == 'Pending':
                status = pending
                date_time = driver.find_element_by_xpath(
                    '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[2]/div[1]/div[6]/div/div[3]/ul/li/div[1]').text

                day = date_time.split()[0]
                dates = date_time.split()[2]
                signed_by = ''
                times = ''
                to = ''
                froms = ''

            print('\n')

            yield {
                'tracking': str(id),
                'status': status,
                'day': day,
                'date': dates,
                'time': times,
                'left_at': froms,
                'receiver': signed_by,
                'location': to
            }
            driver.close()

        print("End\n\n")
