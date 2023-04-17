from sqlalchemy import create_engine
import numpy as np
import pandas as pd


# The configuration of AWS RDS MySQL
user = 'admin'
password = '00000000'
host = 'dbbikes.ci3iggfwlke6.eu-west-1.rds.amazonaws.com'
port = 3306
database = 'dbbikes'

# create the link to Database
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

# read the data table from database
table_name = 'completedata'
dfAll = pd.read_sql_table(table_name, engine)
# take out the needed feature
df = dfAll[['available_bikes', 'available_bike_stands', 'banking', 'number', 'bonus', 'weather_main', 'temp', 'wind_speed', 'timestamp']].copy()


# retrieve 'yyyy-mm-dd', 'hour', 'weekday'
import datetime
import holidays
df['date'] = df['timestamp'].dt.date
df['hour'] = df['timestamp'].dt.hour
df['date'] = pd.to_datetime(df['date'])
df['weekday'] = df['date'].dt.day_name()
ie_holidays = holidays.IE()
df['holiday'] = df['date'].dt.date.apply(lambda x: x in ie_holidays)

# take out the needed columns
df = df[['available_bikes', 'available_bike_stands', 'banking', 'number', 'bonus', 'weather_main', 'temp', 'wind_speed', 'hour', 'weekday', 'holiday']]

#===========The Regression Analysis Using Machine Lerning==============
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Data preparation

# take out independent features and dependent variable
X = df[['hour', 'number', 'weekday', 'holiday', 'weather_main', 'banking', 'bonus', 'wind_speed', 'temp']].copy()
y = df[['available_bikes', 'available_bike_stands']].copy()


# convert categorical variables to one-hot coded variables
X[['hour', 'number', 'weekday', 'holiday', 'weather_main', 'banking', 'bonus']] = X[['hour', 'number', 'weekday', 'holiday', 'weather_main', 'banking', 'bonus']].astype(str)

X = pd.get_dummies(X, columns=['hour', 'number','weekday', 'holiday', 'weather_main', 'banking', 'bonus'])

# divide data into training data and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=93)

# standardize continuous features
scaler = StandardScaler()
X_train[['wind_speed', 'temp']] = scaler.fit_transform(X_train[['wind_speed', 'temp']])
X_test[['wind_speed', 'temp']] = scaler.transform(X_test[['wind_speed', 'temp']])

# train the regression model
y_train_bikes = y_train['available_bikes']
y_train_stands = y_train['available_bike_stands']
lr_bikes = LinearRegression()
lr_stands = LinearRegression()
X_train.columns = X_train.columns.astype(str)
lr_bikes.fit(X_train, y_train_bikes)
lr_stands.fit(X_train, y_train_stands)


# compute prediction on the test data
X_test.columns = X_test.columns.astype(str)
y_pred_bikes = lr_bikes.predict(X_test)
y_pred_stands = lr_stands.predict(X_test)

# Evaluate the model's performance using Mean Squared Error
y_test_bikes = y_test['available_bikes']
y_test_stands = y_test['available_bike_stands']
mse_bikes = mean_squared_error(y_test_bikes, y_pred_bikes)
mse_stands = mean_squared_error(y_test_stands, y_pred_stands)

#print("Mean Squared Error for Bikes:", mse_bikes)
#print("Mean Squared Error for Stands:", mse_stands)

# save the models
import os
import pickle

feature_order = list(X_train.columns) # save the arrangement of  features
models = {'lr_bikes': lr_bikes, 'lr_stands': lr_stands,  'scaler':scaler, 'feature_order': feature_order}
file_dir = 'D:\PythonProjects\DublinBike'

file_path = os.path.join(file_dir, 'models.pkl')
with open(file_path, 'wb') as f:
    pickle.dump(models, f)
