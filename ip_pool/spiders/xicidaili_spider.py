import scrapy

from ip_pool.util import connect_redis, IsActivePorxyIP
import logging
logger = logging.getLogger("xicidaili_spider")


class Xicidaili_spider(scrapy.Spider):
    name = "xicidaili"

    def start_requests(self):
        urls = [
            "http://www.xicidaili.com/nn/1",
            "http://www.xicidaili.com/nn/2",
            "http://www.xicidaili.com/nn/3",
            "http://www.xicidaili.com/nn/4",
            "http://www.xicidaili.com/nn/5",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                dont_filter=True)

    def parse(self, response):
        logger.info("开始解析")
        redis = connect_redis()
        rows = response.xpath("//table//tr[@class]")
        ip_list=[]
        for row in rows:
            ip_path = row.xpath('.//td')[1]
            ip = ip_path.xpath('./text()').extract_first()
            port_path = row.xpath('.//td')[2]
            port = port_path.xpath('./text()').extract_first()
            protocol_path = row.xpath('.//td')[5]
            protocol = protocol_path.xpath('./text()').extract_first()

            ip_list.append(protocol.lower()+ ":" +ip+":"+port)
        logger.info(ip_list)
        active_ip = IsActivePorxyIP()
        valid_ip_list  = active_ip.validate_ip(ip_list)
        if len(valid_ip_list) > 0:
            redis.sadd("checked_ip_proxy", *valid_ip_list)
