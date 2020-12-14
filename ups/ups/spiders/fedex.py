# import scrapy
# from selenium import webdriver
# from scrapy.selector import Selector
# from shutil import which
# from selenium.webdriver.common.keys import Keys
# # for Headless
# from selenium.webdriver.chrome.options import Options
# import pandas as pd
#
#
# class UpSpider(scrapy.Spider):
#     name = 'fed'
#     allowed_domains = ['fedex.com']
#     start_urls = ['http://fedex.com/']
#
#     def parse(self, response):
#         # df = pd.read_csv('D:/Python Code/Scrapy/ups/tracking_id.csv')
#         # ids = df['id']
#         ids = ['914024657736', '914024657780']
#
#         for id in ids:
#             print('\n', id, '\n')
#
#             chrome_options = Options()
#             chrome_options.add_argument("--headless")
#             chrome_path = which("chromedriver")
#
#             # driver = webdriver.Chrome(executable_path=chrome_path)
#             driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)  # , chrome_options=chrome_options
#             driver.get("https://www.fedex.com/apps/fedextrack/?action=track")
#
#             import time
#             time.sleep(10)
#
#             search_input = driver.find_element_by_xpath('//*[@id="track_inbox_track_numbers_area"]')
#             search_input.send_keys(id)
#
#             time.sleep(2)
#             search_btn = driver.find_element_by_xpath('//*[@id="number"]/div/form/div/div/form/div[1]/div/button')
#             time.sleep(2)
#             search_btn.click()
#
#             time.sleep(15)
#
#             delevery = driver.find_element_by_xpath(
#                 '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[2]/h1/div[1]').text
#
#             if delevery == 'Delivered':
#                 status = delevery
#                 times = driver.find_element_by_xpath(
#                     '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[2]/h1/div[2]').text.split()[
#                         3:]
#                 signed_by = driver.find_element_by_xpath(
#                     '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[2]/div[5]/div/h3[3]').text.split()[
#                     3]
#                 to = driver.find_element_by_xpath(
#                     '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[6]/div[2]/div/p[6]').text
#
#                 shipmant_tab = driver.find_element_by_xpath(
#                     '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[2]/div[1]/div[5]/div/ul/li[2]/a')
#                 shipmant_tab.click()
#
#                 import time
#                 time.sleep(2)
#                 all_text = driver.find_element_by_xpath(
#                     '//div[@class="dp_facts_area wtrk_printable"]').text
#
#                 weight = driver.find_element_by_xpath(
#                     '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[2]/div[1]/div[8]/ul/li[3]/span').text
#
#                 print("End\n\n")
#                 time.sleep(2)
#                 travel_history = ''
#
#             # # Level 02
#             pending = driver.find_element_by_xpath(
#                 '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[1]/div/div[2]/h1/div[2]').text
#             if pending == 'Pending':
#                 status = pending
#                 travel_history = driver.find_element_by_xpath(
#                     '//*[@id="container"]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div/div[2]/div[1]/div[6]/div/div[3]/ul/li/div[1]').text
#                 signed_by = ''
#                 times = ''
#                 to = ''
#                 weight = ''
#             else:
#                 status = 'Something went wrong'
#             print('\n')
#
#             yield {
#                 'Tracking ID':  "'"+str(id),
#                 'Status': status,
#                 'Time': times,
#                 'Signed for By': signed_by,
#                 'To': to,
#                 'Weight': weight,
#                 'Travel History Date': travel_history
#             }
#             driver.close()
#
#         print("End\n\n")
