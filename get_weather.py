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

# API key and URL for weather
APIKEY_WEATHER = "61134c8141c567f71f41c90662a798cf"
URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"

engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}", echo=True, connect_args={'autocommit': True})

# Create a database table for weather data
metadata = sqla.MetaData()

weather = sqla.Table("weather", metadata,
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
    weather.drop(engine)
except:
    pass

metadata.create_all(engine)

def write_weather_data_to_db():
    while True:
        try:
            now = datetime.now()
            r = requests.get(URL_WEATHER, params={"lat": 53.3498, "lon": -6.2603, "appid": APIKEY_WEATHER})
            data = json.loads(r.text)

            weather_item = {
                'weather_id': data['weather'][0]['id'],
                'weather_main': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'weather_icon': data['weather'][0]['icon'],
                'temp': data['main']['temp'],
                'pressure': data['main']['pressure'],
                'humidity': data['main']['humidity'],
                'temp_min': data['main']['temp_min'],
                'temp_max': data['main']['temp_max'],
                'visibility': data['visibility'],
                'wind_speed': data['wind']['speed'],
                'wind_deg': data['wind']['deg'],
                'clouds_all': data['clouds']['all'],
                'dt': data['dt'],
                'sys_country': data['sys']['country'],
                'sys_sunrise': data['sys']['sunrise'],
                'sys_sunset': data['sys']['sunset'],
                'timezone': data['timezone'],
                'city_id': data['id'],
                'city_name': data['name'],
                'cod': data['cod'],
                'timestamp': now
            }

            # Create a connection and execute the query
            with engine.connect() as connection:
                connection.execute(weather.insert(), weather_item)

            print(f"Inserted weather data at {now}")
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())


if __name__ == '__main__':
    write_weather_data_to_db()
    # print(data)

