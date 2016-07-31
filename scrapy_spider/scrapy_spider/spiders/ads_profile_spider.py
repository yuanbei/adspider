# -*- coding: utf-8 -*-
import io
import random
import scrapy
from scrapy.http import Response, TextResponse

from scrapy.linkextractors import LinkExtractor
from scrapy_spider.items import AdsProfileItem
from scrapy_splash import SlotPolicy
from scrapy_splash import SplashRequest
from scrapy_splash import SplashJsonResponse
from tld import get_tld
from urlparse import urljoin, urlparse
from scrapy_spider.utils.user_agent_generater import UserAgentGenerater

from pudb import set_trace
set_trace()


class AdsProfileSpider(scrapy.Spider):
    name = "AdsProfileSpider"
    allowed_domains = []

    def __init__(self, *args, **kwargs):
        super(AdsProfileSpider, self).__init__(*args, **kwargs)
        self.ua_generater = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(AdsProfileSpider, cls).from_crawler(crawler,
                                                           *args,
                                                           **kwargs)
        spider.ua_generater = UserAgentGenerater(crawler.settings.get(
            'USER_AGENT_LIST_FILE'))
        return spider

    def set_crawler(self, crawler):
        super(AdsProfileSpider, self).set_crawler(crawler)
        spider.ua_generater = UserAgentGenerater(crawler.settings.get(
            'USER_AGENT_LIST_FILE'))

    def _from_same_site(self, ads_host, ads_target):
        if ads_target is None:
            return True
        if not ads_target.startswith('http'):
            return True
        ads_host_domain = get_tld(ads_host, as_object=True).domain
        ads_target_domain = get_tld(ads_target, as_object=True).domain
        return True if ads_host_domain == ads_target_domain else False

    def _get_all_child_frames(self, splash_json_response):
        child_frames = splash_json_response.data['childFrames']
        frames = []
        for child_frame in child_frames:
            sub_frames = self._get_child_frames(child_frame)
            print "Get %s sub frames from %s" %(len(sub_frames), splash_json_response.url)
            frames.extend(sub_frames)
        return frames

    def _get_child_frames(self, child_frame):
        frames = []
        frame_response = TextResponse(child_frame['requestedUrl'],
                                      body=child_frame['html'].encode('utf8'))
        print "Frame %s " % frame_response
        frames.append(frame_response)
        child_frames = child_frame['childFrames']
        for the_child in child_frames:
            sub_frames = self._get_child_frames(the_child)
            print "Get %s sub frames from %s" %(len(sub_frames), frame_response.url)
            frames.extend(sub_frames)
        return frames

    def _is_valid_frame(self, url):
        if len(url) == 0 or url == "about:blank":
            return False
        return True

    def parse(self, response):
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
            ads_profile["ads_content_frame"] = ""
            ads_profile['ads_host_domain'] = urlparse(response.url).netloc
            ads_profile['ads_target_domain'] = urlparse(link_href).netloc
            yield ads_profile

        if isinstance(response, SplashJsonResponse):
            if "childFrames" in response.data:
                frames = self._get_all_child_frames(response)
                print "Get %s childFrames in %s" % (len(frames), response.url)
                for frame_response in frames:
                    if not self._is_valid_frame(frame_response.url):
                        continue
                    ads_links = frame_response.xpath('//a[img]')
                    for ads_link in ads_links:
                        link_href = ads_link.xpath('@href').extract_first()
                        if self._from_same_site(response.url, link_href):
                            continue

                        ads_profile = AdsProfileItem()
                        ads_profile["ads_host"] = response.url
                        ads_profile["ads_present_mode"] = "normal_1"
                        ads_profile["ads_target_url"] = link_href
                        img_src = frame_response.urljoin(
                            ads_link.xpath('img/@src').extract_first())
                        ads_profile["ads_content_url"] = img_src
                        ads_profile["ads_content_frame"] = frame_response.url
                        ads_profile['ads_host_domain'] = urlparse(response.url).netloc
                        ads_profile['ads_target_domain'] = urlparse(link_href).netloc
                        yield ads_profile

        link_extractor = LinkExtractor()
        all_links = link_extractor.extract_links(response)
        for link in all_links:
            request = SplashRequest(response.urljoin(link.url),
                                    self.parse,
                                    endpoint='render.json',
                                    slot_policy=SlotPolicy.PER_DOMAIN,
                                    args={'html': 1,
                                          'iframes': 1
                                          })
            request.headers.setdefault('User-Agent',
                                       self.ua_generater.get_user_agent())
            yield request
