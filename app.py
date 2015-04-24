from flask import Flask, Response, g, render_template
import sqlite3
import json
import time


app = Flask(__name__)

app.config.update(
    DEBUG=True,
    PROPAGATE_EXCEPTIONS=True
)

DATABASE = 'temperature.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


#select the last entry from the database
def get_current_temp():

    cur = get_db().cursor()
    cur.execute("SELECT * FROM temp_data ORDER BY Time DESC LIMIT 1")

    rows = cur.fetchall()

    for row in rows:
        timestamp = float(row[0]) - float((60*60*6))
        temp = float(row[2])

    return temp


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


#define the index page, which only needs the current temp to render
@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html', current_temp = get_current_temp())


#get temps is used via an ajax call with d3.js, to render the graph
@app.route('/get_temps', methods=['GET'])
def get_temp_json():

    return_array = []

    time_range = int(time.time()) - (60*60*24.0) #grab the last 24 hours
    cur = get_db().cursor()
    cur.execute("SELECT * FROM temp_data WHERE Time > ?", (time_range, ))

    rows = cur.fetchall()

    for row in rows:
    	timestamp = float(row[0]) - float((60*60*6))
    	temp = float(row[2])
    	return_array.append({'x': timestamp, 'y': temp})

    response = Response(json.dumps(return_array))
    return response


#start the app/webserver
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)