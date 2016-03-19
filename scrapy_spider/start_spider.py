# coding:utf8

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    process = CrawlerProcess(get_project_settings())

    process.crawl('AdsProfileSpider')
    # the script will block here until the crawling is finished
    process.start()

if __name__ == '__main__':
    main()
