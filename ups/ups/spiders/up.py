import scrapy


class UpSpider(scrapy.Spider):
    name = 'up'
    allowed_domains = ['ups.com']
    start_urls = ['http://ups.com/']

    def parse(self, response):
        pass
