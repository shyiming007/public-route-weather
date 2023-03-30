from flask import Flask, render_template
import config
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html", apikey=config.APIKEY)


# @app.route('/stations')
# def stations():
# # get db connection
#     # return list of stations
#     pass
# @functools.lru_cache(maxsize=128)
# def get_stations():
#     engine = get_db()
#     sql = "select * from station ;"
#     try:
#         with engine.connect() as conn:
#             rows = conn.execute(text(sql)).fetchall()
#             print('#found {} stations', len(rows), rows)
#             return jsonify([row._asdict() for row in rows]) # use this formula to turn the rows into a list of dicts
#     except:
#         print(traceback.format_exc())
#         return "error in get_stations", 404
    
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



@app.route("/stations")
def get_stations():
    engine = get_db()
    sql = "select * from station;"
    rows = engine.execute(sql).fetchall()
    print('#found {} stations', len(rows))
    return jsonify(...




if __name__ == "__main__":
    app.run(debug=True)