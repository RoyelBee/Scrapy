import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from shutil import which
from selenium.webdriver.common.keys import Keys
# for Headless
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import  requests

class UpSpider(scrapy.Spider):
    name = 'up'
    allowed_domains = ['ups.com']
    start_urls = ['http://ups.com/']

    def parse(self, response):
        link = 'http://ot.michaelelectronics2.com/Cglobal/getTracking/2020-12-11T00:00/2020-12-12T00:00/'
        res = requests.get(link).json()
        # ups_tracking_id = []
        # for val in res:
        #     if val['vendor'] == 'UPS':
        #         ups_tracking_id.append(val['tracking'])
        # print(ups_tracking_id)


        ups_tracking_id = ['1Z7A801T3535584776']

        for id in ups_tracking_id:
            print('\n', id, '\n')

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_path = which("chromedriver")

            # driver = webdriver.Chrome(executable_path=chrome_path)
            driver = webdriver.Chrome(executable_path=chrome_path)
            driver.get("https://www.ups.com/track?loc=en_US&requester=ST/")
            time.sleep(20)
            search_input = driver.find_element_by_id("stApp_trackingNumber")
            search_input.send_keys(id)

            search_btn = driver.find_element_by_id("stApp_btnTrack")
            search_btn.click()

            time.sleep(15)
            status = driver.find_element_by_id('stApp_txtPackageStatus').text


            if status == 'Delivered':
                date = driver.find_element_by_id('stApp_deliveredDate')
                day = driver.find_element_by_id('stApp_deliveredDay')
                timef = driver.find_element_by_id('stApp_eodDate')

                deliverState = driver.find_element_by_id('stApp_txtAddress')
                deliverCountry = driver.find_element_by_id('stApp_txtCountry')
                leftat = driver.find_element_by_id('stApp_txtLeftAt')
                Received = driver.find_element_by_id('stApp_txtReceivedBy')

            yield {
                'tracking': "'" + id,
                'status': status,
                'date': date.text,
                'day': day.text,
                'time': timef.text,
                'location': deliverState.text + deliverCountry.text,
                'left_at': leftat.text,
                'receiver': Received.text
            }
            driver.close()

        print("End\n\n")
