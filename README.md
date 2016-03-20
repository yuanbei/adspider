### AdSpider
A spider which crawls and analyzes ads in the web page. Once we find the ads,
we can generate [ABP](https://adblockplus.org/) filters automatic.

### Ads present model
A lot of ads have the model of the below.
```html
<a href ="ads Target URL">
  <img src = "ads content URL" />
</a>
```
The host URL is the URL of page which hosts the ads.

### How to find the ads.
1. Crawl the web and record the ads profile item into database.
2. Analyze the profiles and find the items which are probably ads.
3. Generate ABP filters from ads profile item.

### Requirements
1. [tld](https://pypi.python.org/pypi/tld)
2. [scrapy](https://github.com/scrapy/scrapy)
3. [lxml](http://lxml.de/)
4. [python-gflags]()
5. [mysql-python]()


