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
import time


class UpSpider(scrapy.Spider):
    name = 'all'
    allowed_domains = ['fedex.com']
    start_urls = ['http://fedex.com/']

    def parse(self, response):
        link = 'http://ot.michaelelectronics2.com/Cglobal/getTracking/1'
        res = requests.get(link).json()

        for ven in res:
            if ven['vendor'] == 'UPS':
                id = ven['tracking']
                print('\n UPS ID = ', id)

                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_path = which("chromedriver")

                # driver = webdriver.Chrome(executable_path=chrome_path)
                driver = webdriver.Chrome(executable_path=chrome_path)
                driver.get("https://www.ups.com/track?loc=en_US&requester=ST/")
                import time
                time.sleep(15)
                search_input = driver.find_element_by_id("stApp_trackingNumber")
                search_input.send_keys(id)
                time.sleep(3)
                search_btn = driver.find_element_by_id("stApp_btnTrack")
                search_btn.click()

                time.sleep(15)
                status = driver.find_element_by_id('stApp_txtPackageStatus').text
                print('Status = ', status)

                if status == 'Delivered':
                    dates = driver.find_element_by_id('stApp_deliveredDate').text
                    day = driver.find_element_by_id('stApp_deliveredDay').text
                    times = driver.find_element_by_id('stApp_eodDate').text

                    deliverState = driver.find_element_by_id('stApp_txtAddress')
                    deliverCountry = driver.find_element_by_id('stApp_txtCountry')
                    leftat = driver.find_element_by_id('stApp_txtLeftAt').text
                    Received = driver.find_element_by_id('stApp_txtReceivedBy').text.split()
                    location = deliverState.text + deliverCountry.text

                if status == 'In Transit':
                    dates = driver.find_element_by_id('stApp_ShpmtProg_LVP_milestone_1_date_1').text
                    times = driver.find_element_by_id('stApp_ShpmtProg_LVP_milestone_2_time_1').text
                    location = driver.find_element_by_xpath(
                        '//*[@id="stApp_ShpmtProg_LVP_milestone_1_location_1"]/span').text
                    day = ''
                    leftat = ''
                    Received = ''

                if status == 'Shipment Ready for UPS':
                    dates = driver.find_element_by_id('stApp_ShpmtProg_LVP_milestone_1_date_1').text
                    times = driver.find_element_by_id('stApp_ShpmtProg_LVP_milestone_2_time_1').text
                    location = driver.find_element_by_xpath(
                        '//*[@id="stApp_ShpmtProg_LVP_milestone_1_location_1"]/span').text
                    day = ''
                    leftat = ''
                    Received = ''


            if ven['vendor'] == 'FedEx':
                # # This section is for Fedex
                id = ven['tracking']
                print('Fedex Id = ', id)

                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_path = which("chromedriver")

                # driver = webdriver.Chrome(executable_path=chrome_path)
                driver = webdriver.Chrome(executable_path=chrome_path)  # , chrome_options=chrome_options
                driver.get("https://www.fedex.com/apps/fedextrack/?action=track")

                import time
                time.sleep(15)

                search_input = driver.find_element_by_xpath('//*[@id="track_inbox_track_numbers_area"]')
                search_input.send_keys(id)

                time.sleep(2)
                search_btn = driver.find_element_by_xpath('//*[@id="number"]/div/form/div/div/form/div[1]/div/button')
                time.sleep(2)
                search_btn.click()

                time.sleep(30)

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
                    leftat = ''
                    Received = ''
                    location = ''

                    print("End\n\n")

                # # Level 02
                pending = driver.find_element_by_xpath(
                    '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[2]/h1/div[2]').text

                if pending == 'Pending':
                    status = pending
                    date_time = driver.find_element_by_xpath(
                        '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[2]/div[1]/div[6]/div/div[3]/ul/li/div[1]').text

                    day = date_time.split()[0]
                    dates = date_time.split()[2]
                    times = ''
                    leftat = ''
                    Received = ''
                    location = ''


            yield {
                'tracking': str(id),
                'status': status,
                'day': day,
                'date': dates,
                'time': times,
                'left_at': leftat,
                'receiver': Received,
                'location': location
            }
            driver.close()
