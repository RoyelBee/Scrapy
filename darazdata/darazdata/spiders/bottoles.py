import scrapy

class darazBotols(scrapy.spiders):
    name = 'botol'

    start_urls = ['https://www.daraz.com.bd/water-bottle/?q=water+bottle&from=suggest_normal']

    def parse(self, response):
        title = response.xpath('//title').extract()

        yield{
            'title' : title
        }

