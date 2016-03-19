# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AdsProfileItem(scrapy.Item):
    ads_present_mode = scrapy.Field()
    ads_target_url = scrapy.Field()
    ads_host = scrapy.Field()
    ads_content_url = scrapy.Field()
    ads_target_domain = scrapy.Field()
    ads_host_domain = scrapy.Field()
