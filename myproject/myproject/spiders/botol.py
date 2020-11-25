import scrapy


class BotolSpider(scrapy.Spider):
    name = 'botol'
    allowed_domains = ['www.daraz.com.bd']
    start_urls = ['https://www.daraz.com.bd/water-bottle/?q=water+bottle&from=suggest_normal']

    def parse(self, response):
        title = response.xpath('//title/text()').get()
        price = response.xpath("//div[@class='c3gUW0']/span/text()").getall()

        yield {
            'title': title,
            'price' : price
        }
