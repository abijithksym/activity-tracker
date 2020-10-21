from pynput import mouse
from pynput import keyboard
import threading
import time
import logging
import pyautogui
import shutil
import os
import datetime
import platform
from datetime import date


operating_system = platform.system()

HOUR = 18
MINUTE = 0
SECOND = 0

# size for screen shot image
width = 960
height = 540

precent_time = datetime.datetime.now()
t = precent_time.strftime("%Y%m%d%H%M%S%f")

def convert(seconds): 
	return time.strftime("%H:%M:%S", time.gmtime(seconds)) 
	  
# for get_active_window_title 
restricted_windows_list = ["instagram","facebook","whatsapp","youtube"] #should be  lower case
restricted_windows_dict = {"instagram":0,"facebook":0,"whatsapp":0,"youtube":0}
restricted_windows_send_dict = {"instagram":"","facebook":"","whatsapp":"","youtube":""}
ONE_TIME_SEND = True
threads =[]
active_window_list = []
time_list = []
prev_list = []

logging.basicConfig(level = logging.INFO, filename = 'activity.log')


# 'ubuntu active window' class
class active_screen_ub(threading.Thread):

	def __init__(self, name ):
		threading.Thread.__init__(self)
		self.Thread_name = name

	def run(self):
		get_active_window_title()

# 'mouse activity' class
class mouse_activities(threading.Thread):
	def __init__(self, name ):
		threading.Thread.__init__(self)
		self.Thread_name = name

	def run(self):
		listenmouse()

# 'ubuntu screen shot' class
class screen_shot_ub(threading.Thread):
	"""docstring for ClassName"""
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.Thread_name = name
	
	def run(self):
		screenshot_ub()

# ' keyboard activity ' class
class key_board(threading.Thread):

	def __init__(self, name ):
		threading.Thread.__init__(self)
		self.Thread_name = name

	def run(self):
		keyboard_activity()

# 'connection ' class
class connection(threading.Thread):

	def __init__(self, name ):
		threading.Thread.__init__(self)
		self.Thread_name = name

	def run(self):
		nw_connectivty()

class sqldata(threading.Thread):

	def __init__(self, name ):
		threading.Thread.__init__(self)
		self.Thread_name = name

	def run(self):
		sqlupload()

#################### sql ####################
import mysql.connector

active_window_str = ""
def sqlupload():
	global active_window_list
	global total_offline_time
	global active_window_str
	while True:

		today = date.today()
		precent_time1 = datetime.datetime.now()
		t1 = precent_time.strftime("%M%S%f")
		mydb = mysql.connector.connect(host="localhost",
		user="newuser1",
		password="1234",
		database="mydatabase1"
		)

		mycursor = mydb.cursor()

		sql = "INSERT INTO activitytracker2 (date1,activitytime,activewindow,offlinetime) VALUES (%s, %s,%s,%s)"
		val = (today, t1,active_window_str,total_offline_time)

		mycursor.execute(sql, val)

		mydb.commit()

		print(mycursor.rowcount, "record inserted.")
		print("33333333333333333333333333333333333333333333333333333")
		time.sleep(10.0)
#############################################




########## function to get 'active window in ubuntu' ##############
def get_active_window_title():
	import subprocess
	import re
	global ONE_TIME_SEND
	global active_window_str
	while True:
		root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
		stdout, stderr = root.communicate()

		m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
	 
		if m != None:
			window_id = m.group(1)
			window = subprocess.Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
		   
			stdout, stderr = window.communicate()
		else:
			return None

		match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)

		if match != None:

			# return match.group("name").strip(b'"')
			active_window = match.group("name").strip(b'"')
			active_window_lower = active_window.decode("utf-8")

			active_window_str = active_window_lower.lower()
		

			if active_window_str not in active_window_list:
				active_window_list.append(active_window_str) 
				# print(active_window_str)
				logging.info("[INFO]: "+active_window_str)
			else:
				if active_window_str != active_window_list[len(active_window_list)-1]:
					active_window_list.remove(active_window_str)
					active_window_list.append(active_window_str)
					# print(active_window_str)
					logging.info("[INFO]: "+active_window_str)


			for i in restricted_windows_list:
				if active_window_list[len(active_window_list)-1].find(i) != -1:
					restricted_windows_dict[i] += 1

			if datetime.datetime.now().time() > datetime.time(HOUR,MINUTE,SECOND):
				for i,j in restricted_windows_dict.items():		
					restricted_windows_send_dict[i] = convert(j)

				if ONE_TIME_SEND:
					print("SENDING: ", restricted_windows_send_dict)

				ONE_TIME_SEND = False
		time.sleep(1)

#####################################################

####################  MOUSE #########################

def on_move(x, y):
    # print('Pointer moved to {0}'.format((x, y)))
    logging.info("[INFO]: Pointer moved to {0} ".format((x, y)))
    


def on_click(x, y, button, pressed):
    # print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
    logging.info("[INFO]: {0} at {1}".format(" Pressed" if pressed else " Released",(x, y)))
    # if not pressed:
    #     # Stop listener
    #     return False

def on_scroll(x, y, dx, dy):
    # print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y)))
    logging.info("[INFO]: {0} at {1}".format('down' if dy < 0 else 'up',(x, y)))



def listenmouse():

# Collect events until released
	with mouse.Listener(
	        on_move=on_move,
	        on_click=on_click,
	        on_scroll=on_scroll) as listener:
	    listener.join()

	# ...or, in a non-blocking fashion:
	listener = mouse.Listener(
	    on_move=on_move,
	    on_click=on_click,
	    on_scroll=on_scroll)
	listener.start()
 ###########################################################

############### keyboard activity function #################
def on_press(key):
	try:
		# print('alphanumeric key {0}  pressed'.format(key.char))
		logging.info("[INFO]: alphanumeric key {0} pressed".format(key.char))

	except AttributeError:
		# print('special key {0} pressed'.format(key))
		logging.info("[INFO]: special key {0} pressed".format(key))


def on_release(key):
	# print('{0} released'.format(key))
	logging.info("{0} released".format(key))

	# if key == keyboard.Key.esc:
	#     listener.stop
	#     return False
def keyboard_activity():

# Collect events until released
	with keyboard.Listener(
		   on_press=on_press,
		   on_release=on_release) as listener:
		listener.join()
  
	# ...or, in a non-blocking fashion:
	listener = keyboard.Listener(
		on_press=on_press,
		on_release=on_release)
	listener.start()

############################################################





################ ubuntu screen shot function ################
def screenshot_ub():
	while True:
		if not os.path.exists("Images"):
			directory = "Images"
			parent_dir = ""
			path = os.path.join(parent_dir, directory)
			os.mkdir(path)

		

		precent_time = datetime.datetime.now()
		myScreenshot = pyautogui.screenshot() 
		print("===================")
		print(type(myScreenshot))
		print(datetime.datetime.now())
		print(precent_time)
		print("===================")
		image = myScreenshot.resize((width, height))
		#   path = 'Images/'
		img_name = str(precent_time)+".png"
		image.save(img_name)
		
		original = img_name
		target = ('Images/')
		shutil.move(original,target)
		logging.info("[INFO]: "+str(img_name)+ " saved ")
		######## checks no.of items in image folde ######
		directory = 'Images'
		number_of_files = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])
		print(number_of_files)
		##################################################

		time.sleep(5)

######################################################################

######################### function for notwork connectivity #####################

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


#################################################################################




if __name__ == '__main__':

# for Linux
	if operating_system =="Linux":

		# 'Thread' To find active window
		thread_active_screen_ub = active_screen_ub('active_window_ub')
		thread_active_screen_ub.start()
		threads.append(thread_active_screen_ub)

		# Thread to find mouse activity
		thread_mouse = mouse_activities('mouse_activity')
		thread_mouse.start()
		threads.append(listenmouse)


		# thread to screen shot
		thread_screen_shot_ub = screen_shot_ub('screen_shot')
		thread_screen_shot_ub.start()
		threads.append(thread_screen_shot_ub)

		# thread keyboard 
		thread_keyboard = key_board('key__board')
		thread_keyboard.start()
		threads.append(thread_keyboard)

		# thread connection
		thread_connection = connection('conectivity')
		thread_connection.start()
		threads.append(thread_connection)

		thread_sql = sqldata('sql')
		thread_sql.start()
		threads.append(thread_sql)

