# D:\PythonProjects\DublinBike\predWeb\predApp.py

from flask import Flask, redirect, url_for,render_template, request
import pandas as pd
from sqlalchemy import create_engine
import holidays
import os, pickle
from datetime import datetime


from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

app = Flask(__name__)



# The configuration of AWS RDS MySQL
user = 'admin'
password = '00000000'
host = 'dbbikes.ci3iggfwlke6.eu-west-1.rds.amazonaws.com'
port = 3306
database = 'dbbikes'
# create the link to Database
global engine
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')



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
    file_dir = 'D:\PythonProjects\DublinBike'
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


if __name__ == '__main__':
    app.run()
