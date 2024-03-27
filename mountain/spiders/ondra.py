import scrapy


class OndraSpider(scrapy.Spider):
    """
    Spider which takes a Mountain Project link as an argument and writes that 
    page's html to file.
    """
    name = 'ondra'
    start_urls = []

    def __init__(self, link=''):
        self.start_urls = [link]

    def parse(self, response):
        content_type = response.url.split("/")[-3]
        page = response.url.split("/")[-2]
        filename = f'{content_type}-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')