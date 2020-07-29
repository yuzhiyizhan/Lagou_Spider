import pymysql
from loguru import logger

db = pymysql.connect(host='localhost', user='root', password='123456', db='LAGOU')
cur = db.cursor()
sql = 'select * from LAGOU'
cur.execute(sql)
results = cur.fetchall()
for row in results:
    print(row)
logger.info(f'查询到{str(len(results))}条数据')
