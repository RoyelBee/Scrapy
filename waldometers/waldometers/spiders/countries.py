import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath('//td/a')

        for country in countries:
            country_name = country.xpath('.//text()').get()
            country_url = country.xpath('.//@href').get()

            # absoulate_url = f"https://www.worldometers.info{country_url}"
            # absoulate_url = response.urljoin(country_url)
            # yield scrapy.Request(url=absoulate_url)

            # Another way
            yield response.follow(url=country_url, callback=self.parse_countries, meta={'country_name': country_name})

    def parse_countries(self, response):
        name = response.request.meta['country_name']
        urls = response.xpath(
            '(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        for url in urls:
            year = url.xpath(".//td[1]/text()").get()
            population = url.xpath(".//td[2]/strong/text()").get()

            yield {
                'Country': name,
                'Year': year,
                'Population': population
            }
