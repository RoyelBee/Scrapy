import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from shutil import which
from selenium.webdriver.common.keys import Keys
# for Headless
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time


class UpSpider(scrapy.Spider):
    name = 'up'
    allowed_domains = ['ups.com']
    start_urls = ['http://ups.com/']

    def parse(self, response):
        df = pd.read_csv('G:/Scrapy/ups/tracking_id.csv')
        ids = df['id']

        for id in ids:
            print('\n', id, '\n')

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_path = which("chromedriver")

            # driver = webdriver.Chrome(executable_path=chrome_path)
            driver = webdriver.Chrome(executable_path=chrome_path)
            driver.get("https://www.ups.com/track?loc=en_US&requester=ST/")
            time.sleep(10)
            search_input = driver.find_element_by_id("stApp_trackingNumber")
            search_input.send_keys(id)

            search_btn = driver.find_element_by_id("stApp_btnTrack")
            search_btn.click()

            time.sleep(10)
            delivery = driver.find_element_by_id('stApp_txtPackageStatus')
            date = driver.find_element_by_id('stApp_deliveredDate')
            day = driver.find_element_by_id('stApp_deliveredDay')
            timef = driver.find_element_by_id('stApp_eodDate')

            deliverState = driver.find_element_by_id('stApp_txtAddress')
            deliverCountry = driver.find_element_by_id('stApp_txtCountry')
            leftat = driver.find_element_by_id('stApp_txtLeftAt')
            Received = driver.find_element_by_id('stApp_txtReceivedBy')

            yield {
                'Status': delivery.text,
                'Date': date.text,
                'Day': day.text,
                'Time': timef.text,
                'Delevery Location': deliverState.text + deliverCountry.text,
                'Left At': leftat.text,
                'Receiver': Received.text
            }
            driver.close()

        print("End\n\n")
