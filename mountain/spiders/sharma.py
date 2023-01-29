import scrapy


class SharmaSpider(scrapy.Spider):
    """
    Retrieve a user's to-do list from mountain project.

    Parameters
    ----------
    profile_url : str
        Mountain Project username with which to retrieve to-do list.
    """
    name = 'sharma'

    def __init__(self, **kwargs): 
      super(SharmaSpider, self).__init__(**kwargs) 

      url = kwargs.get('profile_url')
      self.start_urls = [url]

    def parse(self, response):
        pass