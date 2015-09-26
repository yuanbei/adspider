### Requirements
1. [tld](https://pypi.python.org/pypi/tld)

### AdsCrawler
A crawler which crawls and analyzes ads in the web page. Once we find the ads,
We can generate ABP filters automatic.

### How to find the image ads in internet.
1. Crawl the web and profile the image objects into database.
2. Analyze the profiles and find the images which are probably ads.
3. Generate ABP filters  from ads image profile.

###Ads Profile Table
|----------------------------------------------------------------------------------------------------|         
|record id (primary key)| ads URL             | ads Target URL         | refer URL                   |         
|----------------------------------------------------------------------------------------------------|         
