import scrapy
import logging

class MegosSpider(scrapy.Spider):
    name = 'megos'
    start_urls = [
        'https://www.mountainproject.com/area/111721391/florida'
    ]

    def parse(self, response, coord=None):

        content_type = response.url.split("/")[-3]

        #for areas, crawl sub-areas if parent node and routes if leaf node
        if content_type == 'area':

            #if leaf area, add route urls to queue to be crawled:
            if (response.css("table#left-nav-route-table").get() != None):

                coord = response \
                    .css("table.description-details tr:nth-child(2) td:nth-child(2)::text") \
                    .get() \
                    .strip(" \n")

                links = response \
                    .css("table#left-nav-route-table a::attr(href)") \
                    .getall()

                for link in links:
                    yield response.follow(link, self.parse)

            #else, parent area, so add sub-areas to queue:
            links = response.css('div.lef-nav-row a::attr(href)').getall()
            for link in links:
                yield response.follow(link, self.parse)

        #for route pages, scrape relevant data
        elif content_type == 'route':
            yield self.parse_route(response, coord)

        #in case other links are visited in error:
        else:
            logging.warning(":::Unsuported link found: " +  response.url)


    #parse route into relevant info and return JSON
    def parse_route(self, route, coord):
        route_name = route.css("h1::text").get().split("\n")[1].strip()
        route_id = route.url.split("/")[-2]
        route_type = route \
                .css("table.description-details tr:nth-child(1) " + \
                    "td:nth-child(2)::text")[0] \
                .get() \
                .strip('\n') \
                .strip() \
                .split(',')[0]
        grade = route.css('h2.inline-block span.rateYDS::text').get().strip()
        area_id = route \
            .css('div.mb-half a::attr(href)') \
            .getall()[-5] \
            .split('/')[-2]

        return {
            'route': route_name,
            'id': route_id,
            'type': route_type,
            'coord': coord,
            'grade': grade,
            'area_id': area_id
        }

