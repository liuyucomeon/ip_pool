import logging
import redis
from gevent.pool import Pool
import requests
from gevent import monkey
monkey.patch_socket()

logger = logging.getLogger("util")


def connect_redis():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    presenter = redis.Redis(connection_pool=pool)
    return presenter


class IsActivePorxyIP(object):
    """
    gevent 异步并发验证 代理IP是不是可以用
    """

    def __init__(self):
        self.is_active_proxy_ip = []

    def validate_ip(self, ip_list):
        """
        开启协程池批量验证
        :param ip_list:
        :return:
        """
        pool = Pool(20)
        pool.map(self._probe_proxy_ip, ip_list)
        return self.is_active_proxy_ip

    def _probe_proxy_ip(self, proxy_ip):
        """代理检测"""
        # proxy = urllib2.ProxyHandler(proxy_ip)
        # opener = urllib2.build_opener(proxy)
        # urllib2.install_opener(opener)
        # try:
        #     html = urllib2.urlopen('http://1212.ip138.com/ic.asp')
        #     # print html.read()
        #     if html:
        #         self.is_active_proxy_ip.append(proxy_ip)
        #         return True
        #     else:
        #         return False
        # except Exception as e:
        #     return False
        header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
        }
        protocol = proxy_ip[0:proxy_ip.find(':')]
        proxie = {
            protocol: proxy_ip[proxy_ip.find(':')+1:]
        }
        logger.info(proxie)
        try:
            response = requests.get('http://1212.ip138.com/ic.asp', headers=header,
                                proxies = proxie, timeout = 10)
            if response.status_code in [200,503]:
                self.is_active_proxy_ip.append(proxy_ip)
                logger.info("代理ip"+proxy_ip+"有效")
            else:
                logger.info("代理ip"+proxy_ip+"无效")
        except Exception:
            pass






