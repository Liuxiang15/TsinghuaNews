from scrapy import  cmdline
cmdline.execute("scrapy crawl THUNewsSpider -o news.csv".split())