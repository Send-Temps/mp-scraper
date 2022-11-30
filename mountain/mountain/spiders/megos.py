import scrapy
import logging

class MegosSpider(scrapy.Spider):
    name = 'megos'
    start_urls = [
        'https://www.mountainproject.com/area/111721391/florida'
    ]

    def parse(self, response):
        content_type = response.url.split("/")[-3]
        page = response.url.split("/")[-2]

        if content_type == 'area':
            links = response.css('div.lef-nav-row a::attr(href)').getall()
            for link in links:
                yield response.follow(link, self.parse)
        elif content_type == 'route':
            response = response.css("h1::text").get().split("\n")[1].strip()
            yield response
        else:
            logging.warning("Unsuported link found: " +  response.url)