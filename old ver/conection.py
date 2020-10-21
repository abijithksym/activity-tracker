import os
import time
import threading
import logging
import datetime
logging.basicConfig(level = logging.INFO, filename = 'conection.log')
total_offline_time = ""
total_offline_seconds = 0
connection_cut = ""
connection_cut_time = ""

def nw_connectivty():
	# global offline_time
	global total_offline_time

	while True:
		hostname = "google.com"
		response = os.system("ping -c 1 " + hostname)
		if response == 0:
			pingstatus = "Network Active"
			print("connected")
			logging.info("[INFO]: conected")
			print(total_offline_time)
			print("total offline time=",total_offline_time)
		else:
			pingstatus = "Network Error"
			print("no connections")
			logging.basicConfig(level = logging.WARNING, filename = 'error.log')
			logging.warning("[INFO]: no conection")
			offline()
		time.sleep(05.0)

def offline():
	global total_offline_time
	global total_offline_seconds
	global connection_cut_time
	connection_cut_time = datetime.datetime.now()
	# connection_cut = connection_cut_time.strftime("%H:%M:%S")
	while True:
		hostname = "google.com"
		response = os.system("ping -c 1 " + hostname)
		if response != 0:
			print("no connection")

		else :
			online_datetime = datetime.datetime.now()
			# online_time = online_datetime.strftime("%H:%M:%S")
			total_offline_seconds= (online_datetime-connection_cut_time).total_seconds() + total_offline_seconds
			total_offline_time = datetime.timedelta(seconds=total_offline_seconds)

			nw_connectivty()
		time.sleep(5)


if __name__ == '__main__':
	p7 = threading.Timer(01.0,nw_connectivty())
	p7.start()