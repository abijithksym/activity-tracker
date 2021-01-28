import os
import schedule
import time
a=os.listdir()
print(a)
print(type(a))
def backup():

	hostname = "192.168.1.103" 
	response = os.system("ping -c 1 " + hostname)


	if response == 0:
	  print(hostname, 'is up!')
	  os.system("./gitbackup.sh")
	else:
	  print(hostname, 'is down!')


schedule.every().day.at("10:30").do(backup)
schedule.every().day.at("21:30").do(backup)
while 1:
    schedule.run_pending()
    time.sleep(1)


	
