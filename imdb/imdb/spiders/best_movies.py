import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv_250']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield {
            'title' : response.xpath("//div[@class='title_wrapper']/h1[1]/text()").get(),
            'Year'  : response.xpath("//span[@id='titleYear']/a/text()").get(),
            'Duration' : response.xpath("normalize-space((//time[@datetime='PT142M'])[1]/text())").get(),
            'Genere': response.xpath("//div[@class='subtext']/a[1]/text()").get(),
            'Rating' : response.xpath("//div[@class='ratingValue']/strong/span/text()").get(),
            'Release Date': response.xpath("//div[@class='subtext']/a[2]/text()").get()
        }

