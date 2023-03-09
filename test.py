##########################################################################################################################################

import requests
import json
r = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=43320d58946b9083c60d5f540941c6249d9884a4")

json.loads(r.text)






##########################################################################################################################################

# 定时一分钟写进去一次

import requests
import traceback
import datetime
import time

APIKEY = "43320d58946b9083c60d5f540941c6249d9884a4"
NAME = "dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"


def write_to_file(text):
    now = datetime.datetime.now()
    with open("data/bikes_{}".format(now).replace(" ", "_").replace(":", "-"), "w") as f:
        f.write(text)


def write_to_db(text):
    print("Writing to database:", text)


def main():
    while True:
        try:
            now = datetime.datetime.now()
            r = requests.get(STATIONS, params={"apiKey": APIKEY, "contract": NAME})
            print(r, now)
            write_to_file(r.text)
            write_to_db(r.text)
            time.sleep(60)
        except:
            print(traceback.format_exc())


if __name__ == '__main__':
    main()


##########################################################################################################################################

# 建立连接



import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
from pprint import pprint
import simplejson as json
import requests
import time
from IPython.display import display

URI="dbbikes.ci3iggfwlke6.eu-west-1.rds.amazonaws.com"
PORT="3306"
DB = "dbbikes"
USER = "admin"
PASSWORD = "00000000"

engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

sql = """
CREATE DATABASE IF NOT EXISTS dbbikes;
"""
engine.execute(sql)

for res in engine.execute("SHOW VARIABLES;"):
    print(res)




##########################################################################################################################################

# 建表


metadata = sqla.MetaData()

station = sqla.Table("station", metadata,
    sqla.Column('address', sqla.String(256), nullable=False),
    sqla.Column('banking', sqla.Integer),
    sqla.Column('bike_stands', sqla.Integer),
    sqla.Column('bonus', sqla.Integer),
    sqla.Column('contract_name', sqla.String(256)),
    sqla.Column('name', sqla.String(256)),
    sqla.Column('number', sqla.Integer),
    sqla.Column('position_lat', sqla.REAL),
    sqla.Column('position_lng', sqla.REAL),
    sqla.Column('status', sqla.BigInteger)
)

availability = sqla.Table("availability", metadata,
    sqla.Column('available_bikes', sqla.Integer),
    sqla.Column('available_bike_stands', sqla.Integer),
    sqla.Column('number', sqla.Integer),
    sqla.Column('last_update', sqla.Integer),
)

try:
    station.drop(engine)
    availability.drop(engine)
except:
    pass

metadata.create_all(engine)


##########################################################################################################################################


import requests
import json

url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=43320d58946b9083c60d5f540941c6249d9884a4"
response = requests.get(url)

# 检查响应状态码是否为200，如果不是则说明下载失败
if response.status_code != 200:
    print(f"下载失败，错误代码：{response.status_code}")
else:
    # 将响应的JSON内容转换为Python对象
    data = json.loads(response.text)
    # 保存JSON文件到本地
    with open('stations.json', 'w') as f:
        json.dump(data, f)
    print("JSON文件已成功下载并保存到本地")


def stations_fix_keys(station):
    station['position_lat'] = station['position']['lat']
    station['position_lng'] = station['position']['lng']
    return station


stations = json.loads(open('stations.json', 'r').read())

engine.execute(station.insert(), *map(stations_fix_keys, stations))



#######################################################################################################################################


import requests
import json

url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=43320d58946b9083c60d5f540941c6249d9884a4"
response = requests.get(url)

# 检查响应状态码是否为200，如果不是则说明下载失败
if response.status_code != 200:
    print(f"下载失败，错误代码：{response.status_code}")
else:
    # 将响应的JSON内容转换为Python对象
    data = json.loads(response.text)
    # 保存JSON文件到本地
    with open('availability.json', 'w') as f:
        json.dump(data, f)
    print("JSON文件已成功下载并保存到本地")


def availability_fix_keys(availability):
    # 修改JSON文件中的key以匹配数据库表结构
    availability['number'] = availability['number']
    availability['available_bikes'] = availability['available_bikes']
    availability['available_bike_stands'] = availability['available_bike_stands']
    availability['last_update'] = availability['last_update']
    return availability


# 从JSON文件中加载数据
# availability_list = json.loads(open('availability.json', 'r').read())


# 从JSON文件中加载数据
availabilities = json.loads(open('stations.json', 'r').read())

# 将数据插入到数据库中
engine.execute(availability.insert(), *map(availability_fix_keys, availabilities))

# engine.execute(availability.insert().values(*[availability_fix_keys(avail) for avail in availability]))


#######################################################################################################################################
















