from scrapy import cmdline

import schedule
import time
import sys

# print('\n Every 55 Minutes your program will get execute and then take 5 minutes break')
# schedule.every(20).minutes.do(cmdline.execute("scrapy crawl allcom1".split()))
# print('Next job is set to run at: ' + str(schedule.next_run()))
#
# while True:
#     schedule.run_pending()


import time
import itertools
import os

for i in itertools.count():
    os.system("scrapy crawl allcom1")
    print('\n\n2 Min break \n\n')
    time.sleep(120)
    print('again ')
