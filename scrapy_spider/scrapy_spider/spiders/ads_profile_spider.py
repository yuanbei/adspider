# -*- coding: utf-8 -*-
import io
import random
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy_spider.items import AdsProfileItem
from tld import get_tld
from urlparse import urljoin, urlparse


class AdsProfileSpider(scrapy.Spider):
    name = "AdsProfileSpider"
    allowed_domains = []

    def __init__(self, *args, **kwargs):
        super(AdsProfileSpider, self).__init__(*args, **kwargs)
        self.user_agents = None

    def _read_user_agents(self):
        if self.user_agents is None:
            with io.open(self.user_agent_list_file) as file_handle:
                self.user_agents = file_handle.readlines()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(AdsProfileSpider, cls).from_crawler(crawler,
                                                           *args,
                                                           **kwargs)
        spider.user_agent_list_file = crawler.settings.get(
            'USER_AGENT_LIST_FILE')
        return spider

    def set_crawler(self, crawler):
        super(AdsProfileSpider, self).set_crawler(crawler)
        spider.user_agent_list_file = crawler.settings.get(
            'USER_AGENT_LIST_FILE')

    def _from_same_site(self, ads_host, ads_target):
        if ads_target is None:
            return True
        if not ads_target.startswith('http'):
            return True
        ads_host_domain = get_tld(ads_host, as_object=True).domain
        ads_target_domain = get_tld(ads_target, as_object=True).domain
        return True if ads_host_domain == ads_target_domain else False

    def parse(self, response):
        self._read_user_agents()
        if response.status != 200 or response.body == '':
            return
        ads_links = response.xpath('//a[img]')
        for ads_link in ads_links:
            link_href = ads_link.xpath('@href').extract_first()
            if self._from_same_site(response.url, link_href):
                continue

            ads_profile = AdsProfileItem()
            ads_profile["ads_host"] = response.url
            ads_profile["ads_present_mode"] = "normal_1"
            ads_profile["ads_target_url"] = link_href
            img_src = response.urljoin(
                ads_link.xpath('img/@src').extract_first())
            ads_profile["ads_content_url"] = img_src
            ads_profile['ads_host_domain'] = urlparse(response.url).netloc
            ads_profile['ads_target_domain'] = urlparse(link_href).netloc
            yield ads_profile

        link_extractor = LinkExtractor()
        all_links = link_extractor.extract_links(response)
        for link in all_links:
            request = scrapy.Request(response.urljoin(link.url),
                                     callback=self.parse)
            request.headers.setdefault('User-Agent',
                                       random.choice(self.user_agents))
            yield request
