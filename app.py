from flask import Flask, render_template, jsonify, redirect, url_for, request
from flask_cors import CORS
import config
import requests
import json
from datetime import datetime
import time
import traceback
import sqlalchemy as sqla
from sqlalchemy import create_engine, DateTime, text
import functools
import pandas as pd
from flask import Flask, redirect, url_for, request
from flask import Flask, redirect, url_for,render_template, request
import pandas as pd
from sqlalchemy import create_engine
import holidays
import os, pickle
from datetime import datetime


from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
# Database connection
URI = "dbbikes.ci3iggfwlke6.eu-west-1.rds.amazonaws.com"
PORT = "3306"
DB = "dbbikes"
USER = "admin"
PASSWORD = "00000000"
global engine
engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}", echo=True, connect_args={'autocommit': True})
# API key and URL
APIKEY = "43320d58946b9083c60d5f540941c6249d9884a4"
NAME = "dublin"
URL = "https://api.jcdecaux.com/vls/v1/stations"

app = Flask(__name__)
CORS(app)



app = Flask(__name__)

@app.route("/")
def main():
    
    return render_template("index.html", apikey=config.APIKEY)



@app.route('/station/<int:station_id>')
def station(station_id):
# show the station with the given id, the id is an integer
    return f'Retrieving info for Station: {station_id}'



@app.route("/stations")
@functools.lru_cache(maxsize=128)
def get_stations():
    engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}", echo=True, connect_args={'autocommit': True})
    
    sql = "SELECT * FROM real_time ORDER BY timestamp DESC;"
    try:
        with engine.connect() as conn:
            rows = conn.execute(text(sql)).fetchall()
            print('#found {} stations', len(rows), rows)
            return jsonify([row._asdict() for row in rows]) # use this formula to turn the rows into a list of dicts
    except:
        print(traceback.format_exc())
        return "error in get_stations", 404

@app.route("/occupancy/<int:station_id>")
def get_occupancy(station_id):

    engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}", echo=True, connect_args={'autocommit': True})
    with engine.connect() as conn:
        query = text("""select * from availability where number = :number""")
        df = pd.read_sql_query(query, conn, params={"number":station_id})
        df['last_update_date'] = pd.to_datetime(df.last_update, unit='s')
        df.set_index('last_update_date', inplace=True)
        res = df['available_bike_stands'].resample('1d').mean()
        #res['dt'] = df.index
        print(res)
        
        return jsonify(data=json.dumps(list(zip(map(lambda x: x.isoformat(), res.index), res.values))))
        
# Added route to get the latest weather data
@app.route('/weather')
def get_weather():
    engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}", echo=True, connect_args={'autocommit': True})
    with engine.connect() as conn:
        sql = "SELECT * FROM weather ORDER BY timestamp DESC LIMIT 1;"
        row = conn.execute(text(sql)).fetchone()
        if row:
            return jsonify(row._asdict())
        else:
            return "No weather data available", 404

@app.route('/hour')
def get_hour():
    engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}", echo=True, connect_args={'autocommit': True})
    with engine.connect() as conn:
        sql = "SELECT DATE_FORMAT(timestamp, '%Y-%m-%d %H:00:00') AS hour, AVG(available_bikes) AS average_bikes_hour, AVG(available_bike_stands) AS average_bike_stands_hour, number FROM dbbikes.completedata GROUP BY number,hour"
        try:
            with engine.connect() as conn:
                rows = conn.execute(text(sql)).fetchall()
                print('#found {} stations', len(rows), rows)
                return jsonify([row._asdict() for row in rows]) # use this formula to turn the rows into a list of dicts
        except:
            print(traceback.format_exc())
            return "error in get_stations", 404





@app.route('/showPred/<int:pred_bikes>/<int:pred_stands>')
def showPred(pred_bikes,pred_stands):
    showString = 'The predicted number of the available bikes at starting station is '
    showString += str(pred_bikes)
    showString += '.<br>'
    showString += 'The predicted number of the available stands at ending station is '
    showString += str(pred_stands)
    showString += '.'
    return showString
    #return 'The predicted unmber of the available bikes is %d' % predNum


@app.route('/factors')
def factors():
    # read the real time data of stations
    table_name = 'real_time'
    real_time = pd.read_sql_table(table_name, engine)
    stationNum = real_time.number.unique()
    stationNum.sort()
    now_stations = ''
    for st in stationNum:
        now_stations += f'<option value="{st}">{st}</option>'

    # read thecurrent forecast data of weather
    table_name = 'weather_forecast'
    weather = pd.read_sql_table(table_name, engine)
    weather['dt'] = weather['dt'].apply(datetime.fromtimestamp)
    now_options = ''
    for dt in weather['dt']:
        now_options += f'<option value="{dt}">{dt}</option>'
    return render_template('/factors.html', page_options=now_options, page_stations = now_stations)


@app.route('/predFun', methods=['POST'])
def predFun():
    # read the real time data of stations
    table_name = 'real_time'
    df = pd.read_sql_table(table_name, engine)
    df = df[['banking','number','bonus' ]]
    stationInf = df.copy()

    # conver the unix time to normal time format
    from datetime import datetime
    table_name = 'weather_forecast'
    df = pd.read_sql_table(table_name, engine)
    df['dt'] = df['dt'].apply(datetime.fromtimestamp)
    # take out the date, hour, and convert to weekday and check holiday
    df['date'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df['date'].dt.day_name()
    ie_holidays = holidays.IE()
    df['holiday'] = df['date'].dt.date.apply(lambda x: x in ie_holidays)
    weatherFore = df[['weather_main', 'temp', 'wind_speed', 'weekday', 'hour', 'holiday', 'dt' ]].copy()

    # read the data submitted by web Form
    date_time = str(request.form['dt'])
    startNum = str(request.form['start'])
    endNum = str(request.form['end'])
    # Load the model already trained as well as the scaler and feature orde
    file_dir = '/home/ubuntu/Comp30830group'
    file_path = os.path.join(file_dir, 'models.pkl')
    with open(file_path, 'rb') as f:
        models = pickle.load(f)
    lr_bikes = models['lr_bikes']
    lr_stands = models['lr_stands']
    scaler = models['scaler']
    feature_order = models['feature_order']

    # take out the weather data corresponding to the selected date
    weatherFore = weatherFore[weatherFore['dt']==date_time].tail(1)
    # merge the station data and the weather data
    merged_df = pd.merge(stationInf.assign(key=1), weatherFore.assign(key=1), on='key', how='outer').drop('key', axis=1)
    merged_df = merged_df[['hour', 'number', 'weekday', 'holiday', 'weather_main', 'banking', 'bonus', 'wind_speed', 'temp']].copy()
    merged_df[['hour', 'number', 'weekday', 'holiday', 'weather_main', 'banking', 'bonus']] = merged_df[['hour', 'number', 'weekday', 'holiday', 'weather_main', 'banking', 'bonus']].astype(str)
    # take out the data corresponding to the selected starting station
    X = merged_df[merged_df['number']==startNum].copy()
    X = pd.get_dummies(X, columns=['hour', 'number','weekday', 'holiday', 'weather_main', 'banking', 'bonus'])
    X[['wind_speed', 'temp']] = scaler.transform(X[['wind_speed', 'temp']])
    X.columns = X.columns.astype(str)
    X = X.reindex(columns=feature_order, fill_value=0)

    # train the model forecasting the available bike number
    y_pred_bikes = lr_bikes.predict(X)
    # make prediction
    y_pred_bikes = y_pred_bikes[0]

    # take out the data corresponding to the selected ending station
    X = merged_df[merged_df['number']==endNum].copy()
    X = pd.get_dummies(X, columns=['hour', 'number','weekday', 'holiday', 'weather_main', 'banking', 'bonus'])
    X[['wind_speed', 'temp']] = scaler.transform(X[['wind_speed', 'temp']])
    X.columns = X.columns.astype(str)
    X = X.reindex(columns=feature_order, fill_value=0)

    # train the model forecasting the available stand number
    y_pred_stands = lr_stands.predict(X)
    # make prediction
    y_pred_stands = y_pred_stands[0]

    return redirect(url_for('showPred',pred_bikes=y_pred_bikes,pred_stands=y_pred_stands))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)