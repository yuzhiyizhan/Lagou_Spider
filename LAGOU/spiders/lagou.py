# -*- coding: utf-8 -*-
import scrapy
from ..items import LagouItem
from scrapy.loader import ItemLoader


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    # allowed_domains = ['www.lagou.com']
    start_urls = 'https://www.lagou.com/'

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse, dont_filter=True)

    def parse(self, response):
        datas = response.xpath('//div[@class="mainNavs"]/div/div/dl/dd/a')
        for data in datas:
            url = data.xpath('./@href').get()
            title = data.xpath('./h3/text()').get()
            yield scrapy.Request(url=self.start_urls, callback=self.parse_cookies,
                                 meta={'title': title, 'url': url, 'function': 'parse_joblist', 'cookiejar': url},
                                 dont_filter=True)
            # break

    def parse_cookies(self, response):
        url = response.meta.get('url')
        title = response.meta.get('title')
        functions = response.meta.get('function')
        if functions == 'parse_joblist':
            yield scrapy.Request(url=url, callback=self.parse_joblist, dont_filter=True,
                                 meta={'title': title, 'cookiejar': response.meta.get('cookiejar')})
        if functions == 'parse_item':
            yield scrapy.Request(url=url, callback=self.parse_item, dont_filter=True,
                                 meta={'title': title, 'cookiejar': response.meta.get('cookiejar')})

    def parse_joblist(self, response):
        title = response.meta.get('title')
        datas = response.xpath('//ul[@class="item_con_list"]/li/div/div/div/a[@class="position_link"]')
        for data in datas:
            url = data.xpath('./@href').get()
            yield scrapy.Request(url=self.start_urls, callback=self.parse_cookies,
                                 meta={'title': title, 'url': url, 'function': 'parse_item',
                                       'cookiejar': url},
                                 dont_filter=True)
            # break
        next_url = response.xpath('//div[@class="pager_container"]/a[text()="下一页"]/@href').get()
        if next_url:
            if 'http' in next_url:
                yield scrapy.Request(url=self.start_urls, callback=self.parse_cookies,
                                     meta={'title': title, 'url': next_url, 'function': 'parse_joblist',
                                           'cookiejar': next_url},
                                     dont_filter=True)

    def parse_item(self, response):
        title = response.meta.get('title')
        item = ItemLoader(item=LagouItem(), response=response)
        # 标题/职位title
        item.add_value('title', title)
        # 工作名字job_name
        item.add_xpath('job_name', '//div[@class="position-content-l"]/div/@title')
        # 薪资salary
        item.add_xpath('salary', '//div[@class="position-content-l"]/dd/h3/span[1]/text()')
        # 地方place
        item.add_xpath('place', '//div[@class="position-content-l"]/dd/h3/span[2]/text()')
        # 经验experience
        item.add_xpath('experience', '//div[@class="position-content-l"]/dd/h3/span[3]/text()')
        # 学历schooling
        item.add_xpath('schooling', '//div[@class="position-content-l"]/dd/h3/span[4]/text()')
        # 职业性质profession
        item.add_xpath('profession', '//div[@class="position-content-l"]/dd/h3/span[5]/text()')
        # 职位标签position_label
        item.add_xpath('position_label', '//div[@class="position-content-l"]/dd/ul//text()')
        # 发布时间release_time
        item.add_xpath('release_time', '//div[@class="position-content-l"]/dd/p/text()')
        # 职位福利position_welfare
        item.add_xpath('position_welfare', '//dl[@class="job_detail"]/dd/p/text()')
        # 职位描述job_description
        item.add_xpath('job_description', '//dd[@class="job_bt"]//text()')
        # 工作地址work_address
        item.add_xpath('work_address', '//div[@class="work_addr"]//text()')
        # 公司company
        item.add_xpath('company', '//div[@class="job_company_content"]/h3/em//text()')
        # 公司领域company_area
        item.add_xpath('company_area', '//ul[@class="c_feature"]/li[1]/h4//text()')
        # 公司发展阶段company_development_stage
        item.add_xpath('company_development_stage', '//ul[@class="c_feature"]/li[2]/h4//text()')
        # 公司规模company_size
        item.add_xpath('company_size', '//ul[@class="c_feature"]/li[3]/h4//text()')
        # 公司主页company_home_page
        item.add_xpath('company_home_page', '//ul[@class="c_feature"]/li/a//text()')
        yield item.load_item()
