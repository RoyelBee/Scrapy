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
        self.connection = mysql.connector.connect(host='44.236.114.81',
                                                  user='order_tracking',
                                                  passwd='ot@Ndi@OT251',
                                                  database='order_tracking')
        self.c = self.connection.cursor()
        try:
            self.c.execute(''' create table tbl_ot_tracking_detail (
                                tracking VARCHAR(30),
                                status VARCHAR(30),
                                left_at VARCHAR(30),
                                receiver VARCHAR(30),
                                day VARCHAR(30),
                                location VARCHAR(30),
                                date VARCHAR(50),
                                time VARCHAR(50)
                                )

                            ''')
            self.connection.commit()
        except:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute(""" insert into tbl_ot_tracking_detail (tracking,status,left_at, receiver,day, location, date,time)
                        values (%s,%s,%s,%s,%s,%s,%s,%s)""", (
                            item.get('tracking'),
                            item.get('status'),
                            item.get('left_at'),
                            item.get('receiver'),
                            item.get('day'),
                            item.get('location'),
                            item.get('date'),
                            item.get('time')
                            )
                       )
        self.connection.commit()
        return item
