from scrapy import Spider, Request
from urlparse import urljoin
from scrapy.utils.response import get_base_url
from amazonisbn.loaders import AmazonisbnLoader


class AmazonISBNSpider(Spider):
    name = 'amazonisbn'

    amazon_search_url = ('http://www.amazon.com/s/ref=nb_sb_noss'
                         '?url=search-alias%3Daps&field-keywords={}')

    def start_requests(self):
        isbn = getattr(self, 'isbn')
        yield Request(self.amazon_search_url.format(isbn),
                      callback=self.parse_search)

    def parse_search(self, response):
        urls = response.xpath(
            '//li[contains(@id, "result")]//a[img]/@href').extract()
        url = urljoin(get_base_url(response), urls[0])
        yield Request(url, callback=self.parse_book)

    def parse_book(self, response):
        ld = AmazonisbnLoader(response=response)
        ld.add_xpath(
            'title',
            'id("ebooksProductTitle")/text()')
        ld.add_xpath(
            'no_reviews',
            'id("acrCustomerReviewText")', re='\d+')
        ld.add_xpath(
            'price',
            '//tr[@class="kindle-price"]'
            '//td[contains(@class, "a-color-price")]/text()')
        yield ld.load_item()
