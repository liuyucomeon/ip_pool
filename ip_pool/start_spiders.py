import os
# 必须先加载项目settings配置
# project需要改为你的工程名字（即settings.py所在的目录名字）测试了不加没问题liuyu

# os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'ip_pool.settings')
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
process = CrawlerProcess(get_project_settings())
# 指定多个spider
process.crawl("kuaidaili")
process.crawl("66ip")
process.crawl("xicidaili")

# 执行所有 spider

for spider_name in process.spider_loader.list():
    # print spider_name
    process.crawl(spider_name)
process.start()
