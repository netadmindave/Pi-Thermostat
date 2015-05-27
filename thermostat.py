#!/usr/bin/python
import time
from datetime import datetime
from datetime import timedelta
import os
import MySQLdb as mdb
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO

#Global Variables
Num_AC_Units = 4
mysql_user = 'thermostat'
mysql_password = 'password'
mysql_location = 'localhost'
mysql_DB = 'thermostats'
mysql_table = 'Thermostats'
sensor = Adafruit_DHT.DHT22


#Connect to Database 
db = mdb.connect(mysql_location, mysql_user, mysql_password, mysql_DB);
cursor = db.cursor(mdb.cursors.DictCursor)


for loop in range(0, Num_AC_Units):
		#get all rows and assign them to variables
		cursor.execute("SELECT * FROM Thermostats WHERE Id = %s", loop)
		rows = cursor.fetchall()
		for row in rows:
			Fan_Pin = int(row["Fan_Pin"])
			Compressor_Pin = int(row["Compressor_Pin"])
		GPIO.setup(Fan_Pin, GPIO.OUT)
		GPIO.setup(Compressor_Pin, GPIO.OUT)
		GPIO.output(Fan_Pin, 1)
		GPIO.output(Compressor_Pin, 1)
		Fan_Status = False
		Compressor_Status = False
		cursor.execute("UPDATE Thermostats Set  Fan_Status = %s, Compressor_Status = %s WHERE Id = %s", (Fan_Status, Compressor_Status, loop))

#sleep to make sure compressor is not killed on statup
time.sleep(180)


while True:
	# Loop to get Data From DB
	for loop in range(0, Num_AC_Units):
		#get all rows and assign them to variables
		cursor.execute("SELECT * FROM Thermostats WHERE Id = %s", loop)
		rows = cursor.fetchall()
		for row in rows:
			Sensor_Pin = int(row["Sensor_Pin"])
			Fan_Pin = int(row["Fan_Pin"])
			Compressor_Pin = int(row["Compressor_Pin"])
			Temp_Target = int(row["Temp_Target"])
			Humidity_Target = int(row["Humidity_Target"])
			Fan_Status = bool(row["Fan_Status"])
			Compressor_Status = bool(row["Compressor_Status"])
			Enabled = bool(row["Enabled"])
			Enabled_Time = (row["Enabled_Time"])
			Fan_Time = (row["Fan_Time"])
			Compressor_Time = (row["Compressor_Time"])
			Fan_Change_Recent = bool(row["Fan_Change_Recent"])
			Compressor_Change_Recent = bool(row["Compressor_Change_Recent"])
		#calculate timedeltas	
		current_time = datetime.now()
		fan_time_delta = timedelta(current_time - Fan_Time)
		compressor_time_delta = timedelta(current_time - Compressor_Time)
		enabled_time_delta = timedelta(current_time - Enabled_Time)

		#get actual temperature and humidity
		humidity, temperature = Adafruit_DHT.read_retry(sensor, Sensor_Pin)
		Temp_Actual = int((temperature * 1.8) + 32)
		Humidity_Actual = int(humidity)	

		#put actual temp and humidity in DB
		cursor.execute("UPDATE Thermostats Set Temp_Actual = %s, Humidity_Actual = %s WHERE Id = %s", (Temp_Actual, Humidity_Actual, loop))	

		#if loop to check if the compressor has been turned on or off recently
		if (compressor_time_delta.total_seconds() >	180): 
			#if loop to check for enabled
			if(Enabled == 1):
				#if loop to check actual vs target temps and turn on/off AC
				if (Temp_Target < Temp_Actual):
					print "Turn on AC"
					Fan_Status = True
					Compressor_Status = True
					cursor.execute("UPDATE Thermostats Set Fan_Status = %s, Compressor_Status = %s  WHERE Id = %s", (Fan_Status, Compressor_Status, loop))
					GPIO.output(Fan_Pin, 0)
					GPIO.output(Compressor_Pin, 0)
				else:
					print "Turn off AC"
					Fan_Status = False
					Compressor_Status = False
					Compressor_Time = now()
					cursor.execute("UPDATE Thermostats Set Fan_Status = %s, Compressor_Status = %s, Compressor_Time = %s  WHERE Id = %s", (Fan_Status, Compressor_Status, Compressor_Time, loop))
					GPIO.output(Fan_Pin, 1)
					GPIO.output(Compressor_Pin, 1)	

				if (Humidity_Target < Humidity_Actual):
					print "Turn on AC"
					Fan_Status = True
					Compressor_Status = True
					cursor.execute("UPDATE Thermostats Set Fan_Status = %s, Compressor_Status = %s  WHERE Id = %s", (Fan_Status, Compressor_Status, loop))
					GPIO.output(Fan_Pin, 0)
					GPIO.output(Compressor_Pin, 0)
				else:
					print "Turn off AC"
					Fan_Status = False
					Compressor_Status = False
					cursor.execute("UPDATE Thermostats Set Fan_Status = %s, Compressor_Status = %s  WHERE Id = %s", (Fan_Status, Compressor_Status, loop))
					GPIO.output(Fan_Pin, 1)
					GPIO.output(Compressor_Pin, 1)
		db.commit()


 
db.close()
