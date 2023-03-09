import requests
import json
from datetime import datetime
import time
import traceback
import sqlalchemy as sqla
from sqlalchemy import create_engine, DateTime

# Database connection
URI = "dbbikes.ci3iggfwlke6.eu-west-1.rds.amazonaws.com"
PORT = "3306"
DB = "dbbikes"
USER = "admin"
PASSWORD = "00000000"

# API key and URL
APIKEY = "43320d58946b9083c60d5f540941c6249d9884a4"
NAME = "dublin"
URL = "https://api.jcdecaux.com/vls/v1/stations"

engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}", echo=True, connect_args={'autocommit': True})

# Create database tables
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
    sqla.Column('status', sqla.BigInteger),
    sqla.Column('timestamp', DateTime)
)

availability = sqla.Table("availability", metadata,
    sqla.Column('available_bikes', sqla.Integer),
    sqla.Column('available_bike_stands', sqla.Integer),
    sqla.Column('number', sqla.Integer),
    sqla.Column('last_update', sqla.Integer),
    sqla.Column('timestamp', DateTime)
)

try:
    station.drop(engine)
    availability.drop(engine)
except:
    pass

metadata.create_all(engine)

def station_fix_keys(station):
    station['address'] = station['address']
    station['banking'] = station['banking']
    station['bike_stands'] = station['bike_stands']
    station['bonus'] = station['bonus']
    station['contract_name'] = station['contract_name']
    station['name'] = station['name']
    station['number'] = station['number']
    station['position_lat'] = station['position']['lat']
    station['position_lng'] = station['position']['lng']
    station['status'] = station['status']
    return station

def write_data_to_db():
    while True:
        try:
            now = datetime.now()
            r = requests.get(URL, params={"apiKey": APIKEY, "contract": NAME})
            data = json.loads(r.text)

            stations = []
            availabilities = []
            for item in data:
                station_item = station_fix_keys(item)
                station_item["timestamp"] = now
                stations.append(station_item)

                availability_item = {
                    'number': item['number'],
                    'available_bikes': item['available_bikes'],
                    'available_bike_stands': item['available_bike_stands'],
                    'last_update': item['last_update'],
                    'timestamp': now
                }
                availabilities.append(availability_item)

            # Create a connection and execute the queries
            with engine.connect() as connection:
                connection.execute(station.insert(), stations)
                connection.execute(availability.insert(), availabilities)

            print(f"Inserted data at {now}")
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())


if __name__ == '__main__':
    write_data_to_db()




