from scrapy import cmdline


# name = 'kuaidaili'
# name = '66ip'
name = 'xicidaili'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())