import scrapy


class MultypageSpider(scrapy.Spider):
    name = 'multypage'
    allowed_domains = ['www.clickbd.com']
    start_urls = ['https://www.clickbd.com/search?category=mobile-phones']

    def parse(self, response):

        for model in response.xpath("//div[@class='row']/div/div[3]/div/div"):

            name = model.xpath('.//div/h3/a[1]/text()').get()
            price = model.xpath('.//div[2]/b/b/text()').get()
            url = response.urljoin(model.xpath('.//div/h3/a[1]/@href').get())


            yield {
                'Phone Model' : name,
                'BD Price'    : price,
                'Phone URL' : url
                # 'User Agent': response.request.headers['User-Agent']

            }

        next_page = response.urljoin(response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get())

        if next_page:
            yield scrapy.Request(url= next_page, callback=self.parse)