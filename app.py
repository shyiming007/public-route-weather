from flask import Flask, render_template, jsonify
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

# engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}", echo=True, connect_args={'autocommit': True})




app = Flask(__name__)

@app.route("/")
def main():
    
    return render_template("index.html", apikey=config.APIKEY)





    
# @app.route('/contact')
# def contact():
# # get db connection
#     return app.send_static_file('contact.html')


# @app.route('/realtime')
# def realtime():
#     return app.send_static_file('realtime.html')

@app.route('/station/<int:station_id>')
def station(station_id):
# show the station with the given id, the id is an integer
    return f'Retrieving info for Station: {station_id}'



# @app.route("/stations")
# def get_stations():
#     engine = get_db()
#     sql = "select * from station;"
#     rows = engine.execute(sql).fetchall()
#     print('#found {} stations', len(rows))
#     return jsonify(...

@app.route("/stations")
@functools.lru_cache(maxsize=128)
def get_stations():
    engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}", echo=True, connect_args={'autocommit': True})
    
    sql = "SELECT * FROM station LIMIT 100;"
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
        df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')
        df.set_index('last_update_date', inplace=True)
        res = df['available_bike_stands'].resample('1d').mean()
        #res['dt'] = df.index
        print(res)
        
        return jsonify(data=json.dumps(list(zip(map(lambda x: x.isoformat(), res.index), res.values))))
    

if __name__ == "__main__":
    app.run(debug=True)