# -*- coding: utf-8 -*-

# Scrapy settings for LAGOU project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'LAGOU'

SPIDER_MODULES = ['LAGOU.spiders']
NEWSPIDER_MODULE = 'LAGOU.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'LAGOU (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 64

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 64
# CONCURRENT_REQUESTS_PER_IP = 64
DOWNLOAD_TIMEOUT = 10
# Disable cookies (enabled by default)
COOKIES_ENABLED = False
REDIRECT_ENABLED = False
# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'user-agent': 'Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/83.0.4103.97Safari/537.36',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'LAGOU.middlewares.LagouSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'LAGOU.middlewares.UserAgentDownloadMiddleware': 541,
    # 'LAGOU.middlewares.CookiesDownloaderMiddleware': 540,
    # 'LAGOU.middlewares.LagouDownloaderMiddleware': 542,
    'LAGOU.middlewares.IPProxyDownloadMiddleware': 543,
    'LAGOU.middlewares.RequestLOGDownloadMiddleware': 544,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'LAGOU.extensions.GeneralExtensions': 300,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'LAGOU.pipelines.LagouPipeline': 300,
    'LAGOU.pipelines.CsvPipeline': 301,
    # 'LAGOU.pipelines.MysqlPipeline': 302
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
FILES_PATH = '拉勾职位'
# redis服务配置
# redis主机名
REDIS_HOST = '127.0.0.1'
# redis端口
REDIS_PORT = '6379'
# redis密码
REDIS_PARAMS = ''
# redis db
REDIS_DB = 1
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PARAMS = '123456'
MYSQL_DB = 'LAGOU'
