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
# URL_WEATHER = f"http://api.openweathermap.org/data/2.5/forecast?appid={APIKEY_WEATHER}"

URL_WEATHER = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?appid={APIKEY_WEATHER}"

engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}", echo=True, connect_args={'autocommit': True})

# Create a database table for weather data
metadata = sqla.MetaData()

weather = sqla.Table("weather_forecast", metadata,
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
    sqla.Column('timezone', sqla.Integer),
    sqla.Column('city_id', sqla.Integer),
    sqla.Column('city_name', sqla.String(256)),
    sqla.Column('rain_1h', sqla.REAL, nullable=True),
    sqla.Column('timestamp', DateTime)
)

# try:
#     weather.drop(engine)
# except:
#     pass
#
# metadata.create_all(engine)

def write_weather_data_to_db():
    while True:
        try:
            now = datetime.now()
            r = requests.get(URL_WEATHER, params={"lat": 53.344, "lon": -6.2672})
            data = json.loads(r.text)

            for forecast in data['list']:
                weather_item = {
                    'weather_id': forecast['weather'][0]['id'],
                    'weather_main': forecast['weather'][0]['main'],
                    'weather_description': forecast['weather'][0]['description'],
                    'weather_icon': forecast['weather'][0]['icon'],
                    'temp': forecast['main']['temp'],
                    'pressure': forecast['main']['pressure'],
                    'humidity': forecast['main']['humidity'],
                    'temp_min': forecast['main']['temp_min'],
                    'temp_max': forecast['main']['temp_max'],
                    'visibility': forecast['visibility'],
                    'wind_speed': forecast['wind']['speed'],
                    'wind_deg': forecast['wind']['deg'],
                    'clouds_all': forecast['clouds']['all'],
                    'dt': forecast['dt'],
                    'sys_country': data['city']['country'],
                    'timezone': data['city']['timezone'],
                    'city_id': data['city']['id'],
                    'city_name': data['city']['name'],
                    'rain_1h': forecast['rain']['1h'] if 'rain' in forecast and '1h' in forecast['rain'] else None,
                    'timestamp': now
                }

                # Create a connection and execute the query
                with engine.connect() as connection:
                    # Check if the record already exists for the specific timestamp
                    select_query = weather.select().where(weather.c.dt == weather_item['dt'])
                    result = connection.execute(select_query).fetchone()

                    # If the record exists, update it, otherwise insert a new record
                    if result:
                        update_query = weather.update().where(weather.c.dt == weather_item['dt']).values(weather_item)
                        connection.execute(update_query)
                    else:
                        connection.execute(weather.insert(), weather_item)

            print(f"Updated weather data at {now}")
            time.sleep(60*60)
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())

if __name__ == '__main__':
    write_weather_data_to_db()


