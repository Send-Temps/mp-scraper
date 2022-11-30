import scrapy


class OndraSpider(scrapy.Spider):
    name = 'ondra'
    #allowed_domains = ['mountainproject.com']
    start_urls = [
        'https://www.mountainproject.com/area/105708956/colorado',
        'https://www.mountainproject.com/area/108256713/officers-wall'
    ]

    def parse(self, response):
        ttl = "area-test"
        content_type = response.url.split("/")[-3]
        page = response.url.split("/")[-2]
        filename = f'{ttl}-{content_type}-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')