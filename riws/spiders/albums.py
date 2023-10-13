import scrapy


class AlbumsSpider(scrapy.Spider):
    name = "albums"
    allowed_domains = ["albumoftheyear.org"]
    start_urls = ["https://albumoftheyear.org/"]

    def parse(self, response):
        print(response.body.decode('utf-8'))
