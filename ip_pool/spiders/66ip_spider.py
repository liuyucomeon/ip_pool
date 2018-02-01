import scrapy

from ip_pool.util import connect_redis, IsActivePorxyIP
import logging
logger = logging.getLogger("66ip_spider")


class Ip66_spider(scrapy.Spider):
    name = "66ip"

    def start_requests(self):
        urls = [
            'http://www.66ip.cn/mo.php?sxb=&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                dont_filter=True)

    def parse(self, response):
        redis = connect_redis()
        ip_list = response.xpath('//body').re(r'\d+\.\d+\.\d+\.\d+:\d+')
        ip_list = ["http:"+ip for ip in ip_list]
        active_ip = IsActivePorxyIP()
        valid_ip_list  = active_ip.validate_ip(ip_list)
        if len(valid_ip_list) > 0:
            redis.sadd("checked_ip_proxy", *valid_ip_list)
