# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import mysql.connector

import logging


class upsPipeline(object):
    collection_name = 'upstbl'

    @classmethod
    def open_spider(self, spider):
        self.mydb = mysql.connector.connect(
            host="44.236.114.81",
            user="order_tracking",
            password="ot@Ndi@OT251",
            database="order_tracking"
        )
        self.mycursor = self.mydb.cursor()

    def close_spider(self, spider):
        self.mydb.close()

    def process_item(self, item, spider):
        # Fetch Data By Tracking ID
        check_sql = """SELECT * FROM tbl_ot_tracking_detail WHERE tracking = %s """
        self.mycursor.execute(check_sql, (item.get('tracking'),))
        data_by_tracking_id = self.mycursor.fetchall()

        print('Fetch data = ',data_by_tracking_id)
        print('send id = ',item['tracking'])


        if len(data_by_tracking_id) >=1 :
            print('\n Data is going to update = ',data_by_tracking_id)
            # Data Update query
            sql = """UPDATE `tbl_ot_tracking_detail`
                        SET
                        `status`= %s,
                        `left_at`= %s,
                        `receiver`= %s,
                        `day`= %s,
                        `location`= %s,
                        `date`= %s,
                        `time`= %s
                        WHERE `tracking` = %s"""

            inputData = (item['status'],
                         item['left_at'],
                         item['receiver'],
                         item['day'],
                         item['location'],
                         item['date'],
                         item['time'],
                         item['tracking'])
            self.mycursor.execute(sql, inputData)
            self.mydb.commit()

        else:
            print('\n\n Data is going to insert ', data_by_tracking_id)

            insert_sql = """ insert into tbl_ot_tracking_detail (tracking,status,left_at, receiver,day, location, date,time)
                                    values (%s,%s,%s,%s,%s,%s,%s,%s)"""
            inputData = (item['tracking'],
                        item['status'],
                         item['left_at'],
                         item['receiver'],
                         item['day'],
                         item['location'],
                         item['date'],
                         item['time']
                         )
            self.mycursor.execute(insert_sql, inputData)
            self.mydb.commit()

        return item

