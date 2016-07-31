# -*- coding: utf-8 -*-

from frontera.contrib.scrapy.middlewares.seeds.file import FileSeedLoader
from scrapy_splash import SlotPolicy
from scrapy_splash import SplashRequest
from scrapy_spider.utils.user_agent_generater import UserAgentGenerater


class SplashFileSeedLoader(FileSeedLoader):

    def configure(self, settings):
        super(SplashFileSeedLoader, self).configure(settings)
        self.ua_generater = UserAgentGenerater(settings.get(
            'USER_AGENT_LIST_FILE'))

    def process_start_requests(self, start_requests, spider):
        urls = [url for url in self.load_seeds() if not url.startswith('#')]
        return [self._make_splash_requests_from_url(url) for url in urls]

    def _make_splash_requests_from_url(self, url):
        request = SplashRequest(url,
                                endpoint='render.json',
                                slot_policy=SlotPolicy.PER_DOMAIN,
                                args={'html': 1,
                                      'iframes': 1
                                      })
        request.headers.setdefault('User-Agent',
                                   self.ua_generater.get_user_agent())
        return request
