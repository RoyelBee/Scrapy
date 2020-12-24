import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from shutil import which
from selenium.webdriver.common.keys import Keys
# for Headless
from selenium.webdriver.chrome.options import Options
import pandas as pd
from time import sleep
import requests
import pyautogui as pag

class UpSpider(scrapy.Spider):
    name = 'snow'
    allowed_domains = ['app.snowflake.com']
    start_urls = ['https://app.snowflake.com/']

    def parse(self, response):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_path = which("chromedriver")

        # driver = webdriver.Chrome(executable_path=chrome_path)
        driver = webdriver.Chrome(executable_path=chrome_path)
        # # Login url
        main_page = driver.current_window_handle[0]
        driver.get("https://app.snowflake.com/us-west-2/itstrategists/data/marketplace/listings?category=All&search=")
        sleep(15)
        # Click continue button
        con = driver.find_element_by_xpath('//*[@id="reactRoot"]/div/div[1]/div[2]/div/div/div/div/div[2]/div')
        con.click()

        sleep(20)

        # # login bot --------------------
        pag.click(x=429, y=514)
        pag.typewrite('JOHNCOLLECT')
        sleep(2)
        pag.click(x=452, y=596)
        pag.typewrite('Jeez321333')
        
        sleep(5)
        pag.click(x=595, y=666)
        pag.click()
        # # ------------------------------
        sleep(20)

        # categories = []
        # for cat in response.xpath('//*[@id="reactRoot"]/div/div[2]/div/div[2]/div[1]/div[1]/div'):
        #     categories.append(cat)
        #
        # print(categories)


        yield {
            'text' : driver.find_element_by_xpath('//*[@id="reactRoot"]/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/div').text
        }
