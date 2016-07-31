# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

from scrapy.settings.default_settings import SPIDER_MIDDLEWARES, DOWNLOADER_MIDDLEWARES
from frontera.settings.default_settings import MIDDLEWARES

FRONTERA_SETTINGS = 'frontier.settings'

BOT_NAME = 'scrapy_spider'

SPIDER_MODULES = ['scrapy_spider.spiders']
NEWSPIDER_MODULE = 'scrapy_spider.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

ITEM_PIPELINES = {
    'scrapy_spider.pipelines.MySQLStorePipeline': 300,
}

SPIDER_MIDDLEWARES.update({
    'frontera.contrib.scrapy.middlewares.schedulers.SchedulerSpiderMiddleware': 1000,
    'scrapy.spidermiddleware.depth.DepthMiddleware': None,
    'scrapy.spidermiddleware.offsite.OffsiteMiddleware': None,
    'scrapy.spidermiddleware.referer.RefererMiddleware': None,
    'scrapy.spidermiddleware.urllength.UrlLengthMiddleware': None
})

DOWNLOADER_MIDDLEWARES = {
    # Engine side
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    # Downloader side
}

DOWNLOADER_MIDDLEWARES.update({
    # Frontera
    'frontera.contrib.scrapy.middlewares.schedulers.SchedulerDownloaderMiddleware': 1000,
})

SCHEDULER = 'frontera.contrib.scrapy.schedulers.frontier.FronteraScheduler'
SPIDER_MIDDLEWARES.update({
    'scrapy_spider.spider_middlewares.file_seed_loader.SplashFileSeedLoader': 1,
})

#DOWNLOAD_HANDLERS = {
#    'http': 'scrapy_splash.HTTPDownloadHandler',
#    'https': 'scrapy_splash.HTTPDownloadHandler',
#}

# Splash Settings
SPLASH_URL = 'http://localhost:8050/'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

HTTPCACHE_ENABLED = False
REDIRECT_ENABLED = True
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 3600
RETRY_ENABLED = False
DOWNLOAD_MAXSIZE = 1 * 1024 * 1024

# auto throttling
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = False
AUTOTHROTTLE_MAX_DELAY = 3.0
AUTOTHROTTLE_START_DELAY = 0.25
RANDOMIZE_DOWNLOAD_DELAY = False

# concurrency
CONCURRENT_REQUESTS = 512
CONCURRENT_REQUESTS_PER_DOMAIN = 100

LOG_LEVEL = 'DEBUG'

REACTOR_THREADPOOL_MAXSIZE = 32
DNS_TIMEOUT = 180

MYSQL_DBSPEC = 'localhost:adspider:123456:adspider'
SEEDS_SOURCE = "seeds.txt"
USER_AGENT_LIST_FILE = 'user_agent_list.txt'
