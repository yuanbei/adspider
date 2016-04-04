### AdSpider
A spider which crawls and analyzes ads in the web page. Our main objective is 
generating [ABP](https://adblockplus.org/) filters automatic.

### Ads present model
A lot of ads are presented with the model of below.
```html
<a href ="ads Target URL">
  <img src = "ads content URL" />
</a>
```
The host URL is the URL of page which hosts the ads.

### Core logics of AdSpider
0. Based on Ads present model, crawl the web and record the ads profile item into database.
1. Analyze the profiles and find the items which are probably ads.
2. Generate ABP filters from ads profile item.

### Common Requirements
0. [python 2.7](https://www.python.org/)
1. [tld](https://pypi.python.org/pypi/tld)
2. [lxml](http://lxml.de/)

### Requirements for MySQL tools
0. [MySQL-python]()
1. [python-gflags](https://github.com/google/python-gflags)
2. [google mysql-tools](https://github.com/google/mysql-tools)

### Requirements for Spider
1. [Scrapy](https://github.com/scrapy/scrapy)
2. [Frontera](https://github.com/scrapinghub/frontera)

### Installation Guide
0. [Python 2.7](https://www.python.org/)
1. [pip](www.pip-installer.org/en/latest/installing.html) and [setuptools](https://pypi.python.org/pypi/setuptools) Python packages. Nowadays pip requires and installs setuptools if not installed.
2. Install tld through pip
  ```
  $ pip install tld
  ```
3. Install [lxml for python](http://lxml.de/installation.html)
  ```
  $ pip install lxml
  ```
4. Install MySQL-python through yum
  ```
  $ yum install MySQL-python
  ```
5. Install python-gflags
  ```
  $ pip install python-gflags
  ```
6. Intsall Scrapy
  ```
  $ pip install scrapy
  ```
   
7. Install Frontera
  ```
  $ pip install frontera[distributed,zeromq,sql]
  ```
  
### Deployment
Thanks for [ScarpyHub](http://scrapinghub.com/), AdSpider integrate [Scrapy](https://github.com/scrapy/scrapy) with [Frontera](https://github.com/scrapinghub/frontera) to achieve a broad
distributed Spdier.
