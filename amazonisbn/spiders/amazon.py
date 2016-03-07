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
                      callback=self.parse_search, meta={'isbn': isbn})

    def parse_search(self, response):
        urls = response.xpath(
            '//li[contains(@id, "result")]//a[img]/@href').extract()
        if urls:
            url = urljoin(get_base_url(response), urls[0])
            yield Request(url, callback=self.parse_book,
                          meta={'isbn': response.meta['isbn']})
        else:
            yield self.book_not_found(response)

    def book_not_found(self, response):
        ld = AmazonisbnLoader(response=response)
        ld.add_value('isbn', response.meta['isbn'])
        ld.add_value('found', False)
        return ld.load_item()

    def parse_book(self, response):
        ld = AmazonisbnLoader(response=response)
        ld.add_value('found', True)
        ld.add_value('isbn', response.meta['isbn'])
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
        return ld.load_item()
