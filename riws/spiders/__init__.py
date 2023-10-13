# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from scrapy import Spider , Request


class AOTYSpider(Spider):
    name = 'aoty'
    
    def start_requests(self):
        urls = ['https://www.albumoftheyear.org/']

        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        page = response.url
        print(page)