# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join
from scrapy.loader.processors import TakeFirst
from scrapy.loader.processors import MapCompose


def replace_s(string):
    return string.replace(' ', '')


def replace_n(string):
    return string.replace('\n', '')


def replace_N(string):
    if string:
        return string


def replace_(string):
    return string.replace('-', '')


def replace_x(string):
    return string.replace('\xa0', '')


def replace_str(string):
    return string.replace('发布于拉勾网', '')


def replace_X(string):
    return string.replace('/', '')


def replsce_f(string):
    return string.replace('\\', '')


def replace_C(string):
    return string.replace('查看地图', '')


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field(
        input_processor=MapCompose(replsce_f, replace_X, replace_N),
        output_processor=TakeFirst(),
    )
    job_name = scrapy.Field(
        input_processor=MapCompose(replace_s, replace_N),
        output_processor=TakeFirst(),
    )
    salary = scrapy.Field(
        input_processor=MapCompose(replace_s, replace_N),
        output_processor=TakeFirst(),
    )
    place = scrapy.Field(
        input_processor=MapCompose(replace_X, replace_N),
        output_processor=TakeFirst(),
    )
    experience = scrapy.Field(
        input_processor=MapCompose(replace_s, replace_X, replace_N),
        output_processor=TakeFirst(),
    )
    schooling = scrapy.Field(
        input_processor=MapCompose(replace_s, replace_X, replace_N),
        output_processor=TakeFirst(),
    )
    profession = scrapy.Field(
        input_processor=MapCompose(replace_s, replace_n, replace_N),
        output_processor=TakeFirst(),
    )
    position_label = scrapy.Field(
        input_processor=MapCompose(replace_s, replace_n, replace_N),
        output_processor=Join(),
    )
    release_time = scrapy.Field(
        input_processor=MapCompose(replace_x, replace_s, replace_str, replace_N),
        output_processor=TakeFirst(),
    )
    position_welfare = scrapy.Field(
        input_processor=MapCompose(replace_N),
        output_processor=Join(),
    )
    job_description = scrapy.Field(
        input_processor=MapCompose(replace_s, replace_n, replace_x, replace_N),
        output_processor=Join('\n'),
    )
    work_address = scrapy.Field(
        input_processor=MapCompose(replace_n, replace_s, replace_, replace_C, replace_N),
        output_processor=Join(),
    )
    company = scrapy.Field(
        input_processor=MapCompose(replace_s, replace_n, replace_N),
        output_processor=TakeFirst(),
    )
    company_area = scrapy.Field(
        input_processor=MapCompose(replace_N),
        output_processor=TakeFirst(),
    )
    company_development_stage = scrapy.Field(
        input_processor=MapCompose(replace_N),
        output_processor=TakeFirst(),
    )
    company_size = scrapy.Field(
        input_processor=MapCompose(replace_N),
        output_processor=TakeFirst(),
    )
    company_home_page = scrapy.Field(
        input_processor=MapCompose(replace_N),
        output_processor=TakeFirst(),
    )
