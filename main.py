import os
import json
import scrapy
from util import Util
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

try:
    if os.environ.get("ENV") == "prod":
        pass
    else:
        from dotenv import load_dotenv
        load_dotenv()
        

    s3_bucket_name = os.environ.get('S3_BUCKET_NAME')
    links_filepath = os.environ.get('LINKS_FILEPATH')
    dynamodb_table = os.environ.get('DYNAMODB_TABLE')

    util = Util(s3_bucket_name, dynamodb_table)

except Exception as err:
    print(err)
    print("Error loading environment variables...")
    print("Exiting scraper... Clean exit")
    exit(0)


def main():
    links = util.read_from_s3(links_filepath).split("\n")
    # util.write_to_s3("mp-scrape-test/test_success", links)

    process = CrawlerProcess(get_project_settings())

    process.crawl('megos', start_urls=links, output_file='testing.json')
    process.start()

    with open('payload.json') as payload_file:
        payload_json = payload_file.read()
        payload = json.loads(payload_json)

    util.write_to_s3("mp-scrape-test/payload_test", payload)

    for route in payload:
        pass


if __name__ == '__main__':
    main()
