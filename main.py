import time
from loguru import logger
from scrapy import cmdline
from multiprocessing import Process

confs = [{"spider_name": "lagou", "frequency": 60 * 60 * 12}]


def start_blspider(spider_name, frequency):
    args = ['scrapy', 'crawl', spider_name]
    num = 1
    while True:
        p = Process(target=cmdline.execute, args=(args,))
        p.start()
        p.join()
        logger.debug(f'运行了{num}次')
        num = num + 1
        time.sleep(frequency)


if __name__ == "__main__":
    for conf in confs:
        process = Process(target=start_blspider, args=(conf.get('spider_name'), conf.get('frequency')))
        process.start()
