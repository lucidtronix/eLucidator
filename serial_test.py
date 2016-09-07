import serial

ser = serial.Serial('/dev/ttyACM0',9600)
while True:
	read_serial=ser.readline()
	msg = ser.readline().strip()
	print "Message is:", msg
