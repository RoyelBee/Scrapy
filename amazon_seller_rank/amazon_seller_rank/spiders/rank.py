# -- coding: utf-8 --
import scrapy
import pandas as pd


# Today 02-12-2020
class Review0212Spider(scrapy.Spider):
    name = 'rank'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/']

    def parse(self, response):
        excel_data = pd.read_excel('asin2.xlsx')
        for asin in excel_data['ASIN'].tolist():
            link = '/dp/' + asin + '/?th=1'

            yield response.follow(url=link, callback=self.parse_getreview, meta={'asin': asin})

    def parse_getreview(self, response):
        review_list = []

        for rv in response.xpath("//div[@class='a-section review aok-relative']"):
            review_list.append(rv.xpath("normalize-space(.//div/div/div[4]/span/div/div/span/text())").get())
        print("Len: ", len(review_list))

        rank1 = ''
        rank2 = ''
        try:
            rank1 = response.xpath("//span/span[contains(text(), '#')]/text()").get().split()[0]
        except:
            print("rank1 not found")

        try:
            rank2 = response.xpath("//span/span[2][contains(text(), '#')]/text()").get().split()[0]
        except:
            print("rank2 not found")

        yield {
            'Date': 'ToDayDate',
            'URL': response.urljoin(('/dp/' + response.request.meta['asin'])),
            'Title': response.xpath("normalize-space(//span[@id='productTitle']/text())").get(),
            'Price': response.xpath("normalize-space(//span[@id='price_inside_buybox']/text())").get(),
            'Rank 1': rank1,
            'Rank 2': rank2,
            'Quantity of review': len(review_list),
            'Review': review_list,
            'Review Rating': response.xpath(
                "//div[@class='a-section review aok-relative']/div/div/div[2]/a[1]/i/span/text()").getall(),
            'ASIN': response.request.meta['asin']
        }