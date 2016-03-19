### AdSpider
A spider which crawls and analyzes ads in the web page. Once we find the ads,
we can generate [ABP](https://adblockplus.org/) filters automatic.

### Ads present model
A lot of ads have the model of the below.
```html
<a href ="ads Target URL">
  <img src = "ads URL" />
</a>
```
The refer URL is the URL of page which hosts the ads.

### How to find the image ads in internet.
1. Crawl the web and profile the image objects into database.
2. Analyze the profiles and find the images which are probably ads.
3. Generate ABP filters  from ads image profile.

### Ads Profile Table
```html
|----------------------------------------------------------------------------------------------------|         
|record id (primary key)| ads URL             | ads Target URL         | refer URL                   |         
|----------------------------------------------------------------------------------------------------|         
```

### Requirements
1. [tld](https://pypi.python.org/pypi/tld)
2. [scrapy](https://github.com/scrapy/scrapy)
3. [lxml](http://lxml.de/)
4. [python-gflags]()
5. [mysql-python]()

