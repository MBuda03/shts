import serial, time, datetime, sys, sqlite3
from xbee import ZigBee


# Convert the value to Degrees 
def reading_To_Degrees_C(reading):
	
	readings = []
	for item in reading:
		readings.append(item.get('adc-0'))

	# Averaging voltages since we are getting few samples
	voltage_average = sum(readings)/float(len(readings))

	# Converting Voltage to Temperature C. 
	# FORMULA FROM DIGI.COM/SUPPORT/KBASE
	# (((Voltage_Out / 1023) * 1200) - 500) / 10
	# This only works if the sensor is connected to 3.3V out

	temperature_C = (((voltage_average/1023) * 1200 ) - 500) / 10

	return temperature_C

# Function to get the device id as well
# When the home network consists of multiple devices
# BITIR BUNU
def get_device_id(reading):
	readings = []
	for item in reading:
		readings.append(item.get(''))

	device_id = readings[0]

	return device_id
	
# Save data into the database
# Data format is: Timestamp , Device Id (Configured below), Themperature in C
def save_Data(device_id, temp):
	cursor.execute("INSERT INTO temp_data values( (?), (?), (?) )", (int(time.time()), device_id,temp))
	connection.commit()


# WINDOWS => e.g COM3
# MAC => e.g /dev/tty.usbserial-A702NXQX
# Linux => e.g /dev/ttyUSB0
SERIAL_PORT = "/dev/tty.usbserial-A702NXQX"
BAUD_RATE = 9600

# Configuring the serial
serial_Info = serial.Serial(SERIAL_PORT, BAUD_RATE)
xbee = ZigBee(serial_Info)

# Database
connection = sqlite3.connect('temperature.db')
cursor = connection.cursor()

# Database creation (Only required for init)
# Do not run it if the database is already created!!!
#cursor.execute("CREATE TABLE temp_data(Time varchar(255), RoomID varchar(255), temp varchar(255))")
#connection.commit()

while True:
	try:
		# Get the response from xbee.
		response = xbee.wait_read_frame()
		#print response

		# Turn response into human readible
		temp_C = reading_To_Degrees_C(response['samples'])

		# Print the temp with timestamp
		print  "Time: {0}, Temperature: {1}".format(int(time.time()), temp_C)

		# Save the temp data to the database
		save_Data("Device 1", temp_C)
	except KeyboardInterrupt:
		connection.close()
		break

serial_Info.close()
