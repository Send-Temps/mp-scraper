# mp-scraper
Mountain Project scraping tool

Found out googlebot does not respect crawl delay, gives credibility to me not
respecting it lol. Will try to keep it reasonable - with 10s crawl delay,
could crawl entire site in a month.

back of envelope:
	rts = 277,724 = routes on mountain project, plus ~30k for area pages,
		so = ~300,000
	crl_dly = 60 = crawl delay on mountain project

	rts * crl_dly
		= 300,000 minutes
		= 5,000 hours
		= ~208 days ---> way too long

	if crl_dly is:
		30s ---> ~104 days
		10s ---> ~35 days
		5s  ---> ~17 days
		1s  ---> ~3.5 days

	Florida
		64 climbs total
		64 minutes with respecting 60s crawl delay
		6.4 minutes with 6 seconds crawl delay

	get all sub areas on area page:
		response.css('div.lef-nav-row a::attr(href)').getall()

	get route name from route page:
		response.css("h1::text").get().split("\n")[1].strip()