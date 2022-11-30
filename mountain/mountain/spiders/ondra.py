import scrapy


class OndraSpider(scrapy.Spider):
    name = 'ondra'
    #allowed_domains = ['mountainproject.com']
    start_urls = [
        'https://www.mountainproject.com/area/111721391/florida'
    ]

    def parse(self, response):
        content_type = response.url.split("/")[-3]
        page = response.url.split("/")[-2]
        filename = f'{content_type}-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')