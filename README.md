# mp-scraper
Mountain Project scraping tool

This tool is a web scraper run in ECS containers dispatched by an AWS Batch job within the route-data-etl step function. Below you will find an explanation of every directory and file contained in this repository.

## Folders
### /links/
The links folder contains `links-1` to `links-9`, text files containing all of the seed links for the scraper to access every route and sub area on Mountain Project's site. They are split into these files to create managable chunks for each parallel ECS container to handle independantly. Each instance of the scraper will read one of these files and use the seed links to scrape a chunk of the site.

### /mountain/
The crawler code lives in this directory. The crawler was made using the python crawling framework [Scrapy](https://docs.scrapy.org/en/latest/). Along with some configuration items used by the scraper to handle and process data, the `/mouintain/spiders/` folder contains the "spiders", which are ["the classes which define how a certain site (or a group of sites) will be scraped, including how to perform the crawl (i.e. follow links) and how to extract structured data from their pages (i.e. scraping items)"](https://docs.scrapy.org/en/latest/topics/spiders.html). Basically, the logic for the entire scrape lives here. I have decided to name the spiders after famous rock climbers (just seemed right to me).

`Megos`, the main spider of the project, is responsible for the recursive scrape of an area and all its sub areas. `Megos` is capable of accepting links to both areas and routes. If it receives an area link, it decides whether the page is a parent node (the area contains sub areas and not individual routes, i.e. the page for an entire state), or a leaf node (the page contains individual routes), and processes accordingly. Once it gets a route page, it scrapes all relevant data and returns it as a JSON object.

`Ondra` is a testing utility spider which will scrape exactly one mountain project page and write the scraped html to a file named according to the content type and mountain project id. To use this spider, simply

`Sharma` is a to-be-written spider that will scrape a user's to-do list and return each route as a JSON object, in the same format as the `Megos` crawler. This data will be used to populate a user's to-do list on the SendTemps app.

### /main.py
This is the main function and entry point for the scraper. After setting environment variables based on dev/prod status, the function reads the seed links file designated for it from S3 and kicks off a crawl. Once the crawler is done with the link queue and writes all data to file, the program updates the cache/writes the data to the route data DynamoDB table.

### /scrapy.cfg
This file contains some configuration items for the Scrapy framework.

### /util.py
The utility file contains some common functions for accessing our AWS cloud framework. Notably, it provides an interface to:
- Access S3 (used for the route cache as well as the seed links)
- Access DynamoDB (used to write new route data as well as update existing routes that have changed)
- Create a hash of route data (for checking if route data has changed in the cache/DDB)
- Get/Create a route's Send Temps ID - a uuid used for identifying a route on the Send Temps platform

## Running the Project
First navigate to the root directory and run the following commands (this assumes that you have [pip](https://pypi.org/project/pip/) installed):
```
python3 -m venv env
source env/bin/activate
pip install requirements.txt
```
This will create a new virtual Python environment and install the required dependancies for the project (ie Scrapy).
To run a single spider, the syntax is as follows:
```
scrapy crawl <spider name>
```
For example, if running `ondra` to download a single MP page, the syntax for providing the link as an arg is as follows:
```
scrapy crawl ondra -a link=<insert mountain project link here>
```

## Back of Envelope:

Found out googlebot does not respect crawl delay, gives credibility to me not
respecting it lol. Will try to keep it reasonable - with 10s crawl delay,
could crawl entire site in a month.

	rts = 277,724 = routes on mountain project, plus ~30k for area pages,
		so = ~300,000
	crl_dly = 60 = crawl delay on mountain project (from robots.txt)

	rts * crl_dly
		= 300,000 minutes
		= 5,000 hours
		= ~208 days ---> way too long

	if crl_dly is:
		30s ---> ~104 days
		10s ---> ~35 days
		5s  ---> ~17 days
		1s  ---> ~3.5 days
		500ms -> ~1.8 days
		100ms -> ~0.36 days -> 9 hours

	Florida
		64 climbs total
		64 minutes with respecting 60s crawl delay
		6.4 minutes with 6 seconds crawl delay

## Useful Commands
Below are some commands for manipulating html returned from a spider. Useful for analyzing scraped data for quality, as well as formatting the parser that scrapes the data we then store in DDB.

	get all sub areas on parent area page:
		response.css('div.lef-nav-row a::attr(href)').getall()

	get all route links from leaf node area
		response.css("table#left-nav-route-table a::attr(href)").getall()

	get route name from route page:
		response.css("h1::text").get().split("\n")[1].strip()

	get route type from route page:
		response.css("table.description-details tr:nth-child(1) td:nth-child(2)::text")[0].get().strip('\n').strip().split(',')[0]

	get route grade from route page (works at least for boulder/sport):
		response.css('h2.inline-block span.rateYDS::text').get().strip()

	get route's parent area id:
		response.css('div.mb-half a::attr(href)').getall()[-5].split('/')[-2]

	get coords from area page:
		response.css("table.description-details tr:nth-child(2) td:nth-child(2)::text").get().strip(" \n")

	check if leaf node area page or parent area
		response.css("table#left-nav-route-table").get()