#!/usr/bin/env python '''This version of the readserial program demonstrates using python to write an output file'''

import os
import RPi.GPIO as GPIO
import datetime
import serial
import time
import io
from time import sleep

#configure GPIO output
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(24, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(25, GPIO.IN)
GPIO.output(22, GPIO.HIGH)
GPIO.output(17, GPIO.LOW)

#configure serial
ser = serial.Serial('/dev/ttyAMA0',9600, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1), encoding='ascii', newline='\r')

while True:
	time.sleep(0.05)
	
	#start recording GPS data
	if not GPIO.input(24):
		GPIO.output(17, GPIO.HIGH)
		GPIO.output(22, GPIO.LOW)
		print("recording")
		
		#define output file
		millis = int(round(time.time() * 1000))
		outfile='/boot/gps-recording-'+str(millis)+'.nmea'
		
		is_running = True
		
		with open(outfile,'a') as f:
			while is_running:
				time.sleep(0.05)
				datastring = sio.readline()
				f.write(datastring + '\n')       #\n is new line
				f.flush()  				         #write data to disk
				
				#end recoding
				if not GPIO.input(23):
					f.close()
					is_running = False
					
		GPIO.output(17, GPIO.LOW)
		GPIO.output(22, GPIO.HIGH)
		print("stop recording")
	
	#shutdown
	if not GPIO.input(25):
		os.system("sudo shutdown now")
