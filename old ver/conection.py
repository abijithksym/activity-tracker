import os
import time
import threading
import logging
logging.basicConfig(level = logging.INFO, filename = 'conection.log')

def connect():
	while True:
		hostname = "google.com"
		response = os.system("ping -c 1 " + hostname)
		if response == 0:
		    pingstatus = "Network Active"
		    print("connected")
		    logging.info("[INFO]: conected")
		else:
		    pingstatus = "Network Error"
		    print("no connection")
		    logging.basicConfig(level = logging.WARNING, filename = 'error.log')
		    logging.warning("[INFO]: no conection")
		time.sleep(05.0)

if __name__ == '__main__':
	p7 = threading.Timer(01.0,connect())
	p7.start()