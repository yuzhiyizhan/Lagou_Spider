# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv
import redis
import pymysql
from hashlib import md5
from loguru import logger
from .items import LagouItem
from .settings import FILES_PATH
from .settings import MYSQL_HOST
from .settings import MYSQL_USER
from .settings import MYSQL_PARAMS
from .settings import MYSQL_DB


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    def __init__(self, host='localhost', password=None, port=6379, db=0, blockNum=1, key='bloomfilter'):
        """
        :param host: the host of Redis
        :param port: the port of Redis
        :param db: witch db in Redis
        :param blockNum: one blockNum for about 90,000,000; if you have more strings for filtering, increase it.
        :param key: the key's name in Redis
        """
        self.server = redis.Redis(host=host, password=password, port=port, db=db)
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def isContains(self, str_input):
        if not str_input:
            return False
        m5 = md5()
        m5.update(str(str_input).encode('utf-8'))
        str_input = m5.hexdigest()
        ret = True
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, str_input):
        m5 = md5()
        m5.update(str(str_input).encode('utf-8'))
        str_input = m5.hexdigest()
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)


bf = BloomFilter()


class LagouPipeline:
    def __init__(self):
        self.path = os.path.join(os.getcwd(), FILES_PATH)
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def process_item(self, item, spider):
        try:
            value = dict(item).values()
        except TypeError as e:
            value = None
        if not value:
            return None
        if all(value):
            title = item.get('title')
            job_name = item.get('job_name')
            salary = item.get('salary')
            place = item.get('place')
            experience = item.get('experience')
            schooling = item.get('schooling')
            profession = item.get('profession')
            position_label = item.get('position_label')
            release_time = item.get('release_time')
            position_welfare = item.get('position_welfare')
            job_description = item.get('job_description')
            work_address = item.get('work_address')
            company = item.get('company')
            company_area = item.get('company_area')
            company_development_stage = item.get('company_development_stage')
            company_size = item.get('company_size')
            company_home_page = item.get('company_home_page')
            path = os.path.join(self.path, title)
            if not os.path.exists(path):
                os.mkdir(path)
            file = os.path.join(path, title)
            if not bf.isContains(dict(item).values()):
                bf.insert(dict(item).values())
                with open(f'{file}.csv', mode='a', encoding='utf-8-sig')as f:
                    fp = csv.writer(f)
                    if os.path.getsize(f'{file}.csv') == 0:
                        fp.writerow(
                            ['职位', '工作名字', '薪资', '地方', '经验', '学历', '职业性质', '职位标签', '发布时间', '职位福利', '工作地址', '公司', '公司领域',
                             '公司发展阶段', '公司规模', '公司主页', '职位描述'])
                    fp.writerow(
                        [title, job_name, salary, place, experience, schooling, profession, position_label,
                         release_time,
                         position_welfare, work_address, company, company_area, company_development_stage, company_size,
                         company_home_page, job_description])
                    return item
        else:
            return None


class CsvPipeline:
    def __init__(self):
        self.f = open('拉勾.csv', mode='a', encoding='utf-8-sig')
        self.fp = csv.writer(self.f)

    def process_item(self, item, spider):
        try:
            value = dict(item).values()
        except TypeError as e:
            value = None
        if not value:
            return None
        if all(value):
            title = item.get('title')
            job_name = item.get('job_name')
            salary = item.get('salary')
            place = item.get('place')
            experience = item.get('experience')
            schooling = item.get('schooling')
            profession = item.get('profession')
            position_label = item.get('position_label')
            release_time = item.get('release_time')
            position_welfare = item.get('position_welfare')
            job_description = item.get('job_description')
            work_address = item.get('work_address')
            company = item.get('company')
            company_area = item.get('company_area')
            company_development_stage = item.get('company_development_stage')
            company_size = item.get('company_size')
            company_home_page = item.get('company_home_page')
            if os.path.getsize('拉勾.csv') == 0:
                self.fp.writerow(
                    [['职位', '工作名字', '薪资', '地方', '经验', '学历', '职业性质', '职位标签', '发布时间', '职位福利', '工作地址', '公司', '公司领域',
                      '公司发展阶段', '公司规模', '公司主页', '职位描述']])

            self.fp.writerow(
                [title, job_name, salary, place, experience, schooling, profession, position_label, release_time,
                 position_welfare, work_address, company, company_area, company_development_stage, company_size,
                 company_home_page, job_description])
            return item
        else:
            return None

    def close_spider(self, spider):
        self.f.close()


class MysqlPipeline:
    def __init__(self):
        self.db = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PARAMS, db=MYSQL_DB)
        self.cur = self.db.cursor()

    def process_item(self, item, spider):
        try:
            value = dict(item).values()
        except TypeError as e:
            value = None
        if not value:
            return None
        if all(value):
            title = item.get('title')
            job_name = item.get('job_name')
            salary = item.get('salary')
            place = item.get('place')
            experience = item.get('experience')
            schooling = item.get('schooling')
            profession = item.get('profession')
            position_label = item.get('position_label')
            release_time = item.get('release_time')
            position_welfare = item.get('position_welfare')
            job_description = item.get('job_description')
            work_address = item.get('work_address')
            company = item.get('company')
            company_area = item.get('company_area')
            company_development_stage = item.get('company_development_stage')
            company_size = item.get('company_size')
            company_home_page = item.get('company_home_page')
            if not bf.isContains(dict(item).values()):
                logger.info(f'重复数据{dict(item).values()}')
                bf.insert(dict(item).values())
                sql = f'insert into LAGOU(title, job_name, salary, place, experience, schooling, profession, position_label, release_time,position_welfare, work_address, company, company_area, company_development_stage, company_size,company_home_page, job_description) values(\"{title}\", \"{job_name}\", \"{salary}\", \"{place}\", \"{experience}\", \"{schooling}\", \"{profession}\",\"{position_label}\",\"{release_time}\",\"{position_welfare}\",\"{work_address}\",\"{company}\",\"{company_area}\",\"{company_development_stage}\",\"{company_size}\",\"{company_home_page}\",\"{job_description}\")'
                try:
                    self.cur.execute(sql)
                    self.db.commit()
                except Exception as e:
                    self.db.rollback()
                    logger.error(f'mysql报错信息为{e}')
                    logger.error(f'mysql报错SQL语句为{sql}')
                return item
            else:
                return None

    def close_spider(self, spider):
        self.db.close()
