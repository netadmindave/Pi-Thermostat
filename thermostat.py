#!/usr/bin/python
import time
from datetime import datetime
from datetime import timedelta
import os
import MySQLdb as mdb
import sys
import smbus
import RPi.GPIO as GPIO

#Global Variables
Num_AC_Units = 2
mysql_user = 'thermostat'
mysql_password = 'password'
mysql_location = 'localhost'
mysql_DB = 'thermostats'
mysql_table = 'Thermostats'
GPIO.setmode(GPIO.BCM)


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
		Compressor_Time = 10
		Fan_Time = 10
		cursor.execute("UPDATE Thermostats Set  Fan_Status = %s, Compressor_Status = %s, Compressor_Time = %s, Fan_Time = %s WHERE Id = %s", (Fan_Status, Compressor_Status, Compressor_Time, Fan_Time, loop))

#sleep to make sure compressor is not killed on statup
#time.sleep(10)


while True:
	# Loop to get Data From DB
	for loop in range(0, Num_AC_Units):
		#get all rows and assign them to variables
		cursor.execute("SELECT * FROM Thermostats WHERE Id = %s", loop)
		rows = cursor.fetchall()
		for row in rows:
			Fan_Pin = int(row["Fan_Pin"])
			Compressor_Pin = int(row["Compressor_Pin"])
			Temp_Target = int(row["Temp_Target"])
			Fan_Status = bool(row["Fan_Status"])
			Compressor_Status = bool(row["Compressor_Status"])
			Enabled = bool(row["Enabled"])
			Fan_Time = (row["Fan_Time"])
			Compressor_Time = (row["Compressor_Time"])
			Fan_Change_Recent = bool(row["Fan_Change_Recent"])
			Compressor_Change_Recent = bool(row["Compressor_Change_Recent"])
		
		#get actual temperature
		bus = smbus.SMBus(1)
		tmp102 = bus.read_i2c_block_data(0x48, 0)
		tmp1020 = tmp102[0]
		tmp1021 = tmp102[1]
		Temp_Actual = int((((((tmp1020 << 8) | tmp1021) >> 4) * 0.0625) *1.8 ) + 32 )
		

		#put actual temp and humidity in DB
		cursor.execute("UPDATE Thermostats SET Temp_Actual = %s WHERE Id = %s", (Temp_Actual, loop))	

		#Loop to adjust compressor and fan time
		if (Fan_Time != 0):
			Fan_Time = (Fan_Time - 1)
			cursor.execute("UPDATE Thermostats Set Fan_Time = %s  WHERE Id = %s", (Fan_Time, loop))
		if (Compressor_Time != 0):
			Compressor_Time = (Compressor_Time - 1)
			cursor.execute("UPDATE Thermostats Set Compressor_Time = %s  WHERE Id = %s", (Compressor_Time, loop))

		
		if(Enabled == 1 and Compressor_Time == 0):
			#if loop to check actual vs target temps and turn on/off AC
			if (Temp_Target < Temp_Actual and Compressor_Status != True):
				print "Turn on AC"
				Fan_Status = True
				Compressor_Status = True
				Compressor_Time = 300
				cursor.execute("UPDATE Thermostats Set Fan_Status = %s, Compressor_Status = %s, Compressor_Time = %s  WHERE Id = %s", (Fan_Status, Compressor_Status, Compressor_Time, loop))
				GPIO.output(Fan_Pin, 0)
				GPIO.output(Compressor_Pin, 0)
			if (Temp_Target > Temp_Actual and Compressor_Status == True):
				print "Turn off AC"
				Compressor_Status = False
				Compressor_Time = 300
				Fan_Time = 300
				cursor.execute("UPDATE Thermostats Set Compressor_Status = %s, Compressor_Time = %s, Fan_Time = %s  WHERE Id = %s", (Compressor_Status, Compressor_Time, Fan_Time, loop))
				GPIO.output(Compressor_Pin, 1)	

		#Run fan to continue cooling for 5 min
		if (Compressor_Time == 1):
			Fan_Status = False
			cursor.execute("UPDATE Thermostats Set Fan_Status = %s WHERE Id = %s", (Fan_Status, loop))
			GPIO.output(Fan_Pin, 1)

		db.commit()

	time.sleep(1)

 
db.close()
