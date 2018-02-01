import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, \
    TCPTimedOutError, TimeoutError
from ip_pool.util import connect_redis, IsActivePorxyIP
import logging
logger = logging.getLogger("kuaidaili_spider")


class Kuaidaili_spider(scrapy.Spider):
    name = "kuaidaili"

    def start_requests(self):
        urls = [
            'https://www.kuaidaili.com/free',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                 errback=self.err_handler, dont_filter=True)

    def parse(self, response):
        redis = connect_redis()
        ip_list = []
        for row in response.xpath("//tbody/tr"):
            ip = row.xpath("./td[contains(@data-title,'IP')]/text()").extract_first()
            port = row.xpath("./td[contains(@data-title,'PORT')]/text()").extract_first()
            protocol = row.xpath("./td[contains(@data-title,'类型')]/text()").extract_first()
            ip_list.append(protocol.lower()+ ":" +ip+":"+port)

        active_ip = IsActivePorxyIP()
        valid_ip_list  = active_ip.validate_ip(ip_list)
        if len(valid_ip_list) > 0:
            redis.sadd("checked_ip_proxy", *valid_ip_list)

        current_page = response.xpath("//a[contains(@href,'/free/inha') and "
                                   "contains(@class,'active')]")
        next_page = current_page.xpath("../following-sibling::li")[0]
        next_url = next_page.xpath(".//a/@href").extract_first()
        if next_url is not None:
            logger.info("暂停一秒")
            yield response.follow(next_url, callback=self.parse, dont_filter=True)

    def err_handler(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)







