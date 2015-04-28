from flask import Flask, Response, g, render_template
import sqlite3
import json
import time


app = Flask(__name__)

app.config.update(
    DEBUG=True,
    PROPAGATE_EXCEPTIONS=True
)

database = 'temperature.db'


# Function to check if a database exists
# If so, return it.
def get_database():
    data_b = getattr(g, '_database', None)
    if data_b is None:
        data_b = g._database = sqlite3.connect(database)
    return data_b


# Returns the latest entry in the database
def get_latest_temperature():

    cur = get_database().cursor()
    # Get the entries in the database.
    # Order them by time.
    cur.execute("SELECT * FROM temp_data ORDER BY Time DESC LIMIT 1")

    rows = cur.fetchall()

    for row in rows:
        timestamp = (float(row[0]) - float((60*60*6))) + (7.0 * 60.0 * 60.0)
        temp = float(row[2])

    return temp

# Returns the latest intry for the device x
def get_latest_temp_by_device_id(device_id):
    cur = get_database().cursor()
    # Get the entries in the database.
    # Order them by time.
    cur.execute("SELECT * FROM temp_data WHERE RoomID=device_id ORDER BY Time DESC LIMIT 1")

    rows = cur.fetchall()

    for row in rows:
        timestamp = (float(row[0]) - float((60*60*6))) + (7.0 * 60.0 * 60.0)
        temp = float(row[2])

    return temp

# Close the db connection.
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Creates the index page by using the template.
@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html', current_temp = get_latest_temperature())


# Creates a sample page for rendering the graph, device 2
@app.route('/render_graph_device_1', methods=['GET'])
def get_temp_json():

    data_array = []

    # Defines the time range for the graph.
    # Change this to display last X hours
    time_range_in_hrs = 224.0

    # Defines the x-axis of the graph
    x_axis_range = int(time.time()) - (60*60*time_range_in_hrs) 
    cur = get_database().cursor()
    cur.execute("SELECT * FROM temp_data WHERE Time > ? AND RoomID='Device 1'", (x_axis_range, ))

    # Get the rows from the database using the 
    # range defined above.
    rows = cur.fetchall()

    # For each row of data, get timestamp and temperature
    # Convert timestamp into a proper format
    # Assign x and y values of the graph.
    # Return the graph to be rendered
    for row in rows:
        timestamp = (float(row[0]) - float((60*60*6))) + (7.0 * 60.0 * 60.0)
        temp = float(row[2])
        data_array.append({'x': timestamp, 'y': temp})

    res = Response(json.dumps(data_array))
    return res

# Creates a sample page for rendering the graph, device 2
@app.route('/render_graph_device_2', methods=['GET'])
def get_temp_json_2():

    data_array = []

    # Defines the time range for the graph.
    # Change this to display last X hours
    time_range_in_hrs = 224.0

    # Defines the x-axis of the graph
    x_axis_range = int(time.time()) - (60*60*time_range_in_hrs) 
    cur = get_database().cursor()
    cur.execute("SELECT * FROM temp_data WHERE Time > ? AND RoomID='Device 1'", (x_axis_range, ))

    # Get the rows from the database using the 
    # range defined above.
    rows = cur.fetchall()

    # For each row of data, get timestamp and temperature
    # Convert timestamp into a proper format
    # Assign x and y values of the graph.
    # Return the graph to be rendered
    for row in rows:
        timestamp = (float(row[0]) - float((60*60*6))) + (7.0 * 60.0 * 60.0)
        temp = float(row[2])
        data_array.append({'x': timestamp, 'y': temp})

    res = Response(json.dumps(data_array))
    return res


# Run the webserver
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)