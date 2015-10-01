### Requirements
1. [tld](https://pypi.python.org/pypi/tld)

### AdsCrawler
A crawler which crawls and analyzes ads in the web page. Once we find the ads,
We can generate ABP filters automatic.

### Common Ads model
A lot of ads have the model of the below.
<a href ="ads Target URL">
  <img src = "ads URL" />
</a>
The refer URL is the URL of page which hosts the ads.

### How to find the image ads in internet.
1. Crawl the web and profile the image objects into database.
2. Analyze the profiles and find the images which are probably ads.
3. Generate ABP filters  from ads image profile.

### Ads Profile Table
|----------------------------------------------------------------------------------------------------|         
|record id (primary key)| ads URL             | ads Target URL         | refer URL                   |         
|----------------------------------------------------------------------------------------------------|         
