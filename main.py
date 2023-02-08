import os
import json
import scrapy
from util import Util
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

try:
    if os.environ.get("ENV") != "prod":
        from dotenv import load_dotenv
        load_dotenv()
        

    s3_bucket_name = os.environ.get('S3_BUCKET_NAME')
    links_filepath = os.environ.get('LINKS_FILEPATH')
    cache_filepath = os.environ.get('CACHE_FILEPATH')
    gps_filepath = os.environ.get('GPS_FILEPATH')
    dynamodb_table = os.environ.get('DYNAMODB_TABLE')
    mpIdMapper_table = os.environ.get('MPIDMAPPER_TABLE')
    machine_id = os.environ.get('MACHINE_ID')

    util = Util(s3_bucket_name, dynamodb_table, mpIdMapper_table)

except Exception as err:
    print(err)
    print("Error loading environment variables...")
    print("Exiting scraper... Clean exit")
    exit(0)


def main():
    links = util.read_from_s3(links_filepath).split("\n")

    process = CrawlerProcess(get_project_settings())

    process.crawl('megos', start_urls=links, output_file='testing.json')
    process.start()

    with open('payload.json') as payload_file:
        payload_json = payload_file.read()
        payload = json.loads(payload_json)

    # Cache Schema:
    #
    #    cache = {
    #        "id": "hash",
    #        ...
    #    }
    #
    if (util.check_for_file_s3(cache_filepath)):
        cache = util.read_from_s3(cache_filepath)
    else:
        cache = {}

    # GPS Data Schema:
    #
    #    gps_data = [
    #        {
    #           "routeName": <Route Name>,
    #           "routeId": <Send Temps ID>,
    #           "GPS": <GPS Coords>
    #        },
    #        ...
    #    ]
    #
    gps_data = []

    with util.get_batch_writer_ddb() as batch:
        for route in payload:
            st_id = util.get_id(route["mp_id"])
            st_route = {
                "routeId": st_id,
                "mpId": route["mp_id"],
                "routeName": route["route"],
                "type": route["type"],
                "coord": route["coord"],
                "grade": route["grade"],
                "parentAreaId": route["area_id"],
                "state": route["state"],
                "parentArea": route["area"]
            }

            # If the route exists in the cache already:
            if st_id in cache:
                # if hash of route data has changed,
                if cache[st_id] != util.hash_route_data(st_route):
                    # update in ddb
                    batch.put_item(Item=st_route)
                    # store updated hash in cache
                    cache[st_id] = util.hash_route_data(st_route)

            # If the route does NOT exist in the cache:
            else:
                #put in ddb
                batch.put_item(Item=st_route)
                #put in new cache file 
                cache[st_id] = util.hash_route_data(st_route)
                #put in new gps data s3 file
                gps_data.append({
                    "routeId": st_id,
                    "routeName": route["route"],
                    "GPS": route["coord"]
                })


    util.write_to_s3(cache_filepath, cache)
    util.write_to_s3(gps_filepath, gps_data)


if __name__ == '__main__':
    main()
