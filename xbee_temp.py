import serial, time, datetime, sys
from xbee import ZigBee

# WINDOWS => e.g COM3
# MAC => e.g /dev/tty.usbserial-A702NXQX
SERIAL_PORT = "/dev/tty.usbserial-A702NXQX"

BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

xbee = ZigBee(ser)

print 'TEST 1-2 1-2'
while True:
	try:
		response = xbee.wait_read_frame()
		print response

		# Turn response into human readible

		# Add time stamps

		# Add the values into sqlite/csv as
		# Device ID, Time, Degree in C

	except KeyboardInterrupt:
		break

ser.close()