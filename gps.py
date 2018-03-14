#gps.py
#A script to pull GPS data.
# Uses the pynmea2 library.
# Pynmea2 can be installed via "pip install pynmea2".
#
#import threading
import serial
import csv
import pynmea2
import sys
import threading
from datetime import datetime
import logging
import config

class gps(threading.Thread):
	global logger
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	def __init__(self):
		logger.debug('Initialized GPS\n')
		global ser, curDT
		ser = serial.Serial(
			port='/dev/ttyS0',
			baudrate=9600,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,	
			timeout=1)		
		curDT = datetime.utcnow().strftime("%Y-%m-%d %X")
		
	def run(self):
		logger.debug('Running GPS\n')
		filename = "GPS_" + curDT + ".csv"
		with open(filename, 'wb') as csvfile:
			csvWriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
			logger.debug('Opened ' + filename + '\n')
			headers = ["datetime", "num_sats", "latitude", "latitude_dir", "longitude", "longitude_dir"]
			csvWriter.writerow(headers)	
			while config.exitFlag == False:
				try: 
					line = ser.readline()
					if '$GPGGA' in line:
						msg = pynmea2.parse(line)
						#Removed the below log as it's just going to take up space. This info is available in the 'gps_*.csv' file.
						#logger.info('---Latitude: ' + msg.lat + ' ' + msg.lat_dir + '---Longitude: ' + msg.lon + ' ' + msg.lon_dir)
						curRow = [curDT, msg.num_sats, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir]
						csvWriter.writerow(curRow)
				except (RuntimeError, TypeError, NameError):
					logger.error('General exception. Closing down GPS.\n')
					raise SystemExit
		logger.debug('GPS closed nicely\n')