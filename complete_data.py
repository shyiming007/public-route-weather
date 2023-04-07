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

# API key and URL for weather
APIKEY_WEATHER = "61134c8141c567f71f41c90662a798cf"
URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"

engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}", echo=True, connect_args={'autocommit': True})

# Create database tables
metadata = sqla.MetaData()

completedata = sqla.Table("completedata", metadata,
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
    sqla.Column('available_bikes', sqla.Integer),
    sqla.Column('available_bike_stands', sqla.Integer),
    sqla.Column('last_update', sqla.Integer),
    # Weather data columns
    sqla.Column('weather_id', sqla.Integer),
    sqla.Column('weather_main', sqla.String(256)),
    sqla.Column('weather_description', sqla.String(256)),
    sqla.Column('weather_icon', sqla.String(256)),
    sqla.Column('temp', sqla.REAL),
    sqla.Column('pressure', sqla.Integer),
    sqla.Column('humidity', sqla.Integer),
    sqla.Column('temp_min', sqla.REAL),
    sqla.Column('temp_max', sqla.REAL),
    sqla.Column('visibility', sqla.Integer),
    sqla.Column('wind_speed', sqla.REAL),
    sqla.Column('wind_deg', sqla.Integer),
    sqla.Column('clouds_all', sqla.Integer),
    sqla.Column('dt', sqla.Integer),
    sqla.Column('sys_country', sqla.String(256)),
    sqla.Column('sys_sunrise', sqla.Integer),
    sqla.Column('sys_sunset', sqla.Integer),
    sqla.Column('timezone', sqla.Integer),
    sqla.Column('city_id', sqla.Integer),
    sqla.Column('city_name', sqla.String(256)),
    sqla.Column('cod', sqla.Integer),
    sqla.Column('timestamp', DateTime)
)

try:
    completedata.drop(engine)
except:
    pass

metadata.create_all(engine)

def station_fix_keys(station):
    station['position_lat'] = station['position']['lat']
    station['position_lng'] = station['position']['lng']
    return station


def get_weather_data():
    params = {"appid": APIKEY_WEATHER, "q": "Dublin,IE", "units": "metric"}
    response = requests.get(URL_WEATHER, params=params)
    weather_data = json.loads(response.text)
    return weather_data


def merge_data(station, weather):
    merged = station.copy()
    merged['weather_id'] = weather['weather'][0]['id']
    merged['weather_main'] = weather['weather'][0]['main']
    merged['weather_description'] = weather['weather'][0]['description']
    merged['weather_icon'] = weather['weather'][0]['icon']
    merged['temp'] = weather['main']['temp']
    merged['pressure'] = weather['main']['pressure']
    merged['humidity'] = weather['main']['humidity']
    merged['temp_min'] = weather['main']['temp_min']
    merged['temp_max'] = weather['main']['temp_max']
    merged['visibility'] = weather['visibility']
    merged['wind_speed'] = weather['wind']['speed']
    merged['wind_deg'] = weather['wind']['deg']
    merged['clouds_all'] = weather['clouds']['all']
    merged['dt'] = weather['dt']
    merged['sys_country'] = weather['sys']['country']
    merged['sys_sunrise'] = weather['sys']['sunrise']
    merged['sys_sunset'] = weather['sys']['sunset']
    merged['timezone'] = weather['timezone']
    merged['city_id'] = weather['id']
    merged['city_name'] = weather['name']
    merged['cod'] = weather['cod']

    return merged


def write_data_to_db():
    while True:
        try:
            now = datetime.now()
            r = requests.get(URL, params={"apiKey": APIKEY, "contract": NAME})
            data = json.loads(r.text)

            # Get weather data
            weather_data = get_weather_data()

            data_to_insert = []
            for item in data:
                station_item = station_fix_keys(item)
                station_item["timestamp"] = now

                # Merge weather data with station data
                merged_data = merge_data(station_item, weather_data)
                data_to_insert.append(merged_data)

            # Create a connection and execute the queries
            with engine.connect() as connection:
                for record in data_to_insert:
                    # Insert new data
                    connection.execute(completedata.insert(), record)

            print(f"Inserted data at {now}")
            time.sleep(300)
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())


if __name__ == '__main__':
    write_data_to_db()

