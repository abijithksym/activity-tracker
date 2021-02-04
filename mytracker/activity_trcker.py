from pynput.keyboard import Listener  as KeyboardListener
from pynput.mouse    import Listener  as MouseListener
from pynput.keyboard import Key
import threading
import time
import logging
import pyautogui
import os
import datetime
import platform
from datetime import date
import signal
import gi
import psutil

from tkinter import *
import tkinter as tk
from pystray import MenuItem as item
import pystray
from PIL import Image

import requests
import json

import mysql.connector
import socket
import sock

####################################### LOGIN ############################################
IS_LOGIN = False
token = ""
icon_online = None

mydb = 	mysql.connector.connect(host="localhost",user="newuser1",password="1234")
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS activitytracker")


mydb = mysql.connector.connect(host="localhost",user="newuser1",password="1234",database="activitytracker")
mycursor = mydb.cursor()
# mycursor.execute("CREATE TABLE IF NOT EXISTS tb_tracker (day VARCHAR(100), activitytime VARCHAR(255),active_application VARCHAR(255),activewindow VARCHAR(255),offlinetime VARCHAR(255))")

mycursor.execute("CREATE TABLE IF NOT EXISTS tb_token (token VARCHAR(100))")

mycursor.execute("CREATE TABLE IF NOT EXISTS tb_tracker1(no varchar(10),activity JSON)")

ANG_IP = '192.168.2.8'
# TCP_PORT = 9090
ANG_PORT = "3004"
# TCP_IP = 'localhost'
# TCP_PORT = 8000

icon_online = None
def icon_show():
	global icon_online,IS_LOGIN
	image = Image.open("logon.png")
	menu = (item('About', about_action), item('Quit', quit))
	icon_online = pystray.Icon("logout", image, "Logged-in", menu)
	icon_online.run()

def about_action():
	pass

def quit():
	pystray.icon_online.stop()

def login_success():
	global IS_LOGIN,icon_online
	IS_LOGIN = True
	login_screen.withdraw()
	login_screen.quit()
	login_screen.destroy()
	image = Image.open("logon.png")
	menu = (item('About', about_action), item('Quit', quit_program))
	icon_online = pystray.Icon("logout", image, "Logged-in", menu)
	icon_online.run()

def login_verify():
	global token
	global ANG_PORT,TCP_IP
	username1 = username_verify.get()
	password1 = password_verify.get()
	username_login_entry.delete(0, END)
	password_login_entry.delete(0, END)
	url = 'http://' + ANG_IP +':'+ ANG_PORT + '/users/login'
	body = {'user_name':username1,'password':password1}
	try:
		x = requests.post(url, data = body)
		# token_json = x.text
		token_json = json.loads(x.text)
		# print(token_json)
		# print(token_json["token"])
		token = token_json["token"]
		if x.status_code == 200:
			# print("ok")
			sql = "INSERT INTO tb_token (token) VALUES (%s)"
			val = (token)
			mycursor.execute(sql, val)
			mydb.commit()
			login_success()
		else:
			Label(login_screen, text="try again").pack()
	except:
		Label(login_screen, text="server down").pack()
		# print("sorry")

def login():
	global login_screen
	
	login_screen = Tk()
	login_screen.eval('tk::PlaceWindow . center')
	login_screen.title("Login")
	login_screen.geometry("350x290")
	login_screen.resizable(0,0)

	Label(login_screen, text="Please enter details below to login" ,fg = '#06d16c').pack()
	Label(login_screen, text="").pack()

	global username_verify
	global password_verify

	username_verify = StringVar()
	password_verify = StringVar()

	global username_login_entry
	global password_login_entry

	Label(login_screen, text="Username * ",fg = '#550cf2').pack()
	username_login_entry = Entry(login_screen, textvariable=username_verify)
	username_login_entry.pack()
	Label(login_screen, text="").pack()
	Label(login_screen, text="Password * ",fg = '#550cf2').pack()
	password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
	password_login_entry.pack()
	Label(login_screen, text="").pack()
	Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()
	login_screen.mainloop()


connection = mysql.connector.connect(host='localhost',database='activitytracker',user='newuser1',password='1234')

sql_select_Query = "select * from tb_token"
cursor = connection.cursor()
cursor.execute(sql_select_Query)
records_tb_token = cursor.fetchall()
# print(type(cursor.rowcount))
row_count = cursor.rowcount
for  row in records_tb_token:
	pass
if row_count == 1:
	token = row[0]
	IS_LOGIN = True

else:
	IS_LOGIN = False

###################################################################################################


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



######################  THREAD CLASSES   ###################################

#####--1 active application class
class class_application(threading.Thread):
	def __init__(self, name ):
		threading.Thread.__init__(self)
		self.Thread_name = name

	def run(self):
		active_app()

#####--2 sqldata class
class sqldata(threading.Thread):

	def __init__(self, name ):
		threading.Thread.__init__(self)
		self.Thread_name = name

	def run(self):
		sqldatabase()


#####--3 'ubuntu active window' class
class active_screen_ub(threading.Thread):

	def __init__(self, name ):
		threading.Thread.__init__(self)
		self.Thread_name = name

	def run(self):
		get_active_window_title()

#####--4 idle_mouse class
class class_mouse_idle(threading.Thread):
	"""docstring for class_mouse_idle"""
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.Thread_name = name
	
	def run(self):
		mouse_idle()

#####--5 'mouse activity' class
class mouse_activities(threading.Thread):
	def __init__(self, name ):
		threading.Thread.__init__(self)
		self.Thread_name = name

	def run(self):
		activity()

#####--6 'ubuntu screen shot' class
class screen_shot_ub(threading.Thread):
	"""docstring for ClassName"""
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.Thread_name = name
	
	def run(self):
		screenshot_ub()

#####--7 connection class
class connection(threading.Thread):

	def __init__(self, name ):
		threading.Thread.__init__(self)
		self.Thread_name = name

	def run(self):
		nw_connectivty()

#####--8 tcp class
class tcp_class(threading.Thread):
	def __init__(self, name ):
		threading.Thread.__init__(self)
		self.Thread_name = name

	def run(self):
		tcp_connection()

#####--9 sqldata class
class sqldata(threading.Thread):

	def __init__(self, name ):
		threading.Thread.__init__(self)
		self.Thread_name = name

	def run(self):
		sqldb()


###########################################################

#####--1################  active app  #####################
process_list = []
process_name = ""
def active_app():
	global process_name
	global IS_LOGIN
	global process_list
	while not IS_LOGIN:
		time.sleep(0.25)
		continue
	while IS_LOGIN:
		pid = int(os.popen('xdotool getactivewindow getwindowpid').read())

		process = psutil.Process(pid)

		process_name = process.name()
		if process_name not in process_list:
			process_list.append(process_name)

	
		else:
			if process_name != process_list[len(process_list)-1]:
				process_list.remove(process_name)
				process_list.append(process_name)

		time.sleep(1)
###################################################

#####--2############  sqldata  ####################
import mysql.connector

import socket
import sock

active_window_str = ""
def sqldatabase():
	global IS_LOGIN
	while not IS_LOGIN:
		time.sleep(0.25)
		continue
	while IS_LOGIN:
		mydb = mysql.connector.connect(host="localhost",
		user="newuser1",
		password="1234",
		# database="mydatabase1"
		)
		mycursor = mydb.cursor()
		mycursor.execute("CREATE DATABASE IF NOT EXISTS activitytracker")
		sqltable()

def sqltable():
	mydb = mysql.connector.connect(
	host="localhost",
	user="newuser1",
	password="1234",
	database="activitytracker"
	)

	mycursor = mydb.cursor()

	mycursor.execute("CREATE TABLE IF NOT EXISTS tracker (day VARCHAR(100), activitytime VARCHAR(255),active_application VARCHAR(255),activewindow VARCHAR(255),offlinetime VARCHAR(255))")
	sqlupload()
def sqlupload():
	global active_window_list
	global total_offline_time
	global active_window_str
	global process_name

	global token
	#-------TCP---------#
	TCP_IP = '127.0.0.1'
	# TCP_IP = '192.168.2.8'
	TCP_PORT = 9090
	# BUFFER_SIZE = 1024
	#--------------------#
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	while True:

		day = date.today()
		precent_time1 = datetime.datetime.now()
		activitytime = precent_time1.strftime("%H-%M-%S")
		mydb = mysql.connector.connect(host="localhost",user="newuser1",password="1234",database="activitytracker")

		mycursor = mydb.cursor()

		sql = "INSERT INTO tracker (day,activitytime,active_application,activewindow,offlinetime) VALUES (%s,%s, %s,%s,%s)"
		val = (day, activitytime,process_name,active_window_str,total_offline_time)
		mycursor.execute(sql, val)
		mydb.commit()

		#-----------TCP communication----------#
		data_dict = {"token":token,"day":str(day),"time":activitytime,"active_application":process_name}
		live_data = json.dumps(data_dict)
		s.send(live_data.encode())
		
		data = s.recv(1024)
		# s.close()
		print("received data:", data.decode())
		#---------------------------------------#

		print(mycursor.rowcount, "record inserted.")
		time.sleep(1.0)
############################################# 

#####--3 ##### function to get 'active window in ubuntu' ##############
restriction = False
def get_active_window_title():
	import subprocess
	import re
	global ONE_TIME_SEND
	global active_window_str
	global IS_LOGIN,restriction
	while not IS_LOGIN:
		time.sleep(0.25)
		continue
	while IS_LOGIN:
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
					restriction = True

			if datetime.datetime.now().time() > datetime.time(HOUR,MINUTE,SECOND):
				for i,j in restricted_windows_dict.items():		
					restricted_windows_send_dict[i] = convert(j)

				if ONE_TIME_SEND:
					print("SENDING: ", restricted_windows_send_dict)

				ONE_TIME_SEND = False
		time.sleep(1)

################################################################################
#####--4 ################ MOUSE and KEY-BOARD IDLE #############################
mouse_movelist_x = []
mouse_movelist_y = []
mouse_movelist_x_prev = []
mouse_movelist_y_prev = []

key_press_list = []
key_press_list_prev = []
def mouse_idle():
	global IS_LOGIN
	global mouse_movelist_x
	global mouse_movelist_y
	global mouse_movelist_x_prev
	global mouse_movelist_y_prev

	global key_press_list 
	global key_press_list_prev
	while not IS_LOGIN:
		time.sleep(0.25)
		continue
	while IS_LOGIN:
		if mouse_movelist_x == mouse_movelist_x_prev and mouse_movelist_y == mouse_movelist_y_prev and key_press_list == key_press_list_prev:
			# print("inactive")
			idle_time_counter()
		else:
			mouse_movelist_x_prev.clear()
			mouse_movelist_y_prev.clear()
			key_press_list_prev.clear()
			mouse_movelist_x_prev = list(mouse_movelist_x)
			mouse_movelist_y_prev = list(mouse_movelist_y)
			key_press_list_prev = list(key_press_list)
			# print("active")
		time.sleep(10)

		#-------Idle timer----------#
idle_houre = 0
idle_minute = 0
idle_second = 0

def idle_time_counter():
	global idle_houre,idle_minute,idle_second,idle_in_time_period,active_window_str,restricted_windows_list,restriction
	while True:
		if mouse_movelist_x == mouse_movelist_x_prev and mouse_movelist_y == mouse_movelist_y_prev and key_press_list == key_press_list_prev:
			# print(active_window_str)
			# print(restricted_windows_list)
			
			# print("Restriction == ",restriction)
			if restriction == False:
				if idle_second < 60:
					idle_second += 1
				if idle_second == 60:
					idle_second = 0
					idle_minute += 1

				# if idle_minute == 60 :
				# 	if idle_houre < 24:
				# 		idle_second = 0
				# 		idle_minute = 0
				# 		idle_houre = idle_houre + 1
				# 	if idle_houre ==24 :
				# 		idle_second = 0
				# 		idle_minute = 0
				# 		idle_houre = 0
				
			else:
				pass
		else:
			# print(f"inactive time ={idle_houre}:{idle_minute}:{idle_second}")
			mouse_idle()
		# print(f"TIME = {idle_houre}:{idle_minute}:{idle_second}")
		time.sleep(1)
		#--------------------------------#

####################################################################

#####--5 ################### MOUSE and KEY-BOARD ####################
key_press = 0
def on_move(x, y):
	global mouse_movelist_x
	global mouse_movelist_y

	logging.info("Mouse moved to ({0}, {1})".format(x, y))
	if len(mouse_movelist_x)<10 and len(mouse_movelist_y)<10:
		mouse_movelist_x.append(x)
		mouse_movelist_y.append(y)

	else:
		mouse_movelist_x.pop(0)
		mouse_movelist_x.append(x)
		mouse_movelist_y.pop(0)
		mouse_movelist_y.append(y)

def on_press(key):

	global key_press_list,key_press
	key_press = key_press + 1
	key_pressed = str(key)
	logging.info(str(key))
	if len(key_press_list)<10:
		key_press_list.append(str(key))
	else:
		key_press_list.pop(0)
		key_press_list.append(str(key))

def on_click(x, y, button, pressed):
	global key_press
	if pressed:
		key_press = key_press + 1
		logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
		# print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
		# print(f"{key_press} no.of keys pressed")

def on_scroll(x, y, dx, dy):
	logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
	# print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

def activity():
	global IS_LOGIN

	while not IS_LOGIN:
		time.sleep(0.25)
		continue

	while IS_LOGIN:
		with MouseListener( on_click=on_click, on_scroll=on_scroll, on_move=on_move) as listener:
			with KeyboardListener(on_press=on_press) as listener:
				listener.join()
############################################################################

#####--6 ############ ubuntu screen shot function ################
def screenshot_ub():
	global IS_LOGIN

	while not IS_LOGIN:
		time.sleep(0.25)
		continue

	while IS_LOGIN:
		if not os.path.exists("Images"):
			directory = "Images"
			parent_dir = ""
			path = os.path.join(parent_dir, directory)
			os.mkdir(path)

		precent_time = datetime.datetime.now()
		myScreenshot = pyautogui.screenshot() 
		image = myScreenshot.resize((width, height))
		img_name = 'Images/' + str(precent_time)+".png"
		image.save(img_name)
		

		logging.info("[INFO]: "+str(img_name)+ " saved ")
		#----------- checks no.of items in image folde ----------#
		directory = 'Images'
		number_of_files = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])
		# print(number_of_files)
		#---------------------------------------------------------#

		time.sleep(5)

############################################################################

#####--7################### function for notwork connectivity #####################

total_offline_time = ""
total_offline_seconds = 0
connection_cut = ""
connection_cut_time = ""
network_connection = True

def nw_connectivty():
	global IS_LOGIN
	# global offline_time
	global total_offline_time
	while not IS_LOGIN:
		time.sleep(0.25)
		continue
	while IS_LOGIN:
		hostname = "google.com"
		response = os.system("ping -c 1 " + hostname)
		if response == 0:
			pingstatus = "Network Active"
			# print("connected")
			logging.info("[INFO]: conected")
			network_connection = True
			print("network_connection=",network_connection)
		else:
			pingstatus = "Network Error"
			# print("no connections")
			logging.basicConfig(level = logging.WARNING, filename = 'error.log')
			logging.warning("[INFO]: no conection")
			offline()
		time.sleep(05.0)

def offline():
	global total_offline_time
	global total_offline_seconds
	global connection_cut_time,network_connection
	connection_cut_time = datetime.datetime.now()
	# connection_cut = connection_cut_time.strftime("%H:%M:%S")
	while True:
		hostname = "google.com"
		response = os.system("ping -c 1 " + hostname)
		if response != 0:
			print("no connection")
			network_connection = False
			total_offline_seconds = (datetime.datetime.now()-connection_cut_time)
			print("network_connection=",network_connection)
		else :
			print(total_offline_seconds)
			# print(connection_cut_time)
			network_connection = True
			nw_connectivty()
		time.sleep(5)


##############################################################
#####--8################ TCP-connection #######################
live_data = ""
# TCP_PORT = 9090
TCP_PORT = 9090
# IP = '192.168.2.8'
IP = '127.0.0.1'
tcp_send_flag = None
def tcp_connection():
	global restricted_windows_list,restricted_windows_dict,restricted_windows_send_dict,idle_in_time_period,idle_second,idle_minute,network_connection,activity_number
	global IS_LOGIN,restriction,tcp_send_flag
	global total_offline_time
	global live_data
	global TCP_PORT,IP
	while not IS_LOGIN:
		time.sleep(0.25)
		continue

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IP, TCP_PORT))

	while IS_LOGIN:
		time.sleep(50)
		live_data_setup()

		if network_connection and s:
			try:
				tcp_send_flag = True
				s.send(live_data.encode())
				data = s.recv(1024)
				print("received data:", data.decode())
				if activity_number != 0:
					print("activity_number=",activity_number)
					print("sql table contains data!")
					sql_select_Query = "select * from tb_tracker1"
					mycursor = mydb.cursor()
					mycursor.execute(sql_select_Query)
					records = mycursor.fetchall()
					for row in records:
						s.send(row[1].encode())
						data = s.recv(1024)
						print(data)
						print(row[1])
						time.sleep(0.03)
						if not data:
							s.send(row[1].encode())
							data = s.recv(1024)
				delete_sql()
			except:
				tcp_send_flag = False
				tcp_reconnect()
					
			print("completed")
			print("network_connection=",network_connection)
			clear_dic_items()

def tcp_reconnect():
	global TCP_PORT,IP
	global tcp_send_flag
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((IP, TCP_PORT))
		tcp_send_flag = True
	except:
		tcp_send_flag = False
		pass
def live_data_setup():
	global idle_in_time_period,idle_minute,idle_second,live_data
	idle_in_time_period = str(f"{idle_minute}:{idle_second}")
	new_dict = {**restricted_windows_dict, **{'idle_time': idle_in_time_period}} 
	live_data = json.dumps(new_dict)

def clear_dic_items():
	global restriction,restricted_windows_dict,idle_minute,idle_second,idle_in_time_period

	restriction = False
	restricted_windows_dict = {"instagram":0,"facebook":0,"whatsapp":0,"youtube":0}
	idle_minute=0
	idle_second=0
	idle_in_time_period = str(f"{idle_minute}:{idle_second}")

def delete_sql():
	sql_select_Query = "select * from tb_tracker1"
	mycursor = mydb.cursor()
	mycursor.execute(sql_select_Query)
	records = mycursor.fetchall()
	mycursor.execute("DELETE FROM tb_tracker1")
	mydb.commit()
	print("deletin...")	


########################################################
#####--9############### sql bd ####################
activity_number = 0
def sqldb():
	global IS_LOGIN,network_connection,tcp_send_flag
	global live_data,mydb,mycursor,activity_number,records
	while not IS_LOGIN:
		time.sleep(0.25)
	while IS_LOGIN:
		time.sleep(50)
		sql_select_Query = "select * from tb_tracker1"
		mycursor = mydb.cursor()
		mycursor.execute(sql_select_Query)
		records = mycursor.fetchall()
		activity_number = mycursor.rowcount
		print("Total number of rows in tb_tracker1 is: ", activity_number)
		if not network_connection or not tcp_send_flag :
			live_data_setup()
			sql = "INSERT INTO tb_tracker1 (no,activity) VALUES (%s,%s)"
			val = (activity_number+1,live_data)
			print("data inserted successfully")
			mycursor.execute(sql, val)
			mydb.commit()
			clear_dic_items()

		else:
			pass



###################################################

if __name__ == '__main__':
	
# for Linux
	if operating_system =="Linux":

		######--1   thread active applicatin
		thread_active_application = class_application('application')
		thread_active_application.start()
		threads.append(thread_active_application)

		# ######--2   thread sql
		# thread_sql = sqldata('sql')
		# thread_sql.start()
		# threads.append(thread_sql)

		#####--3 'Thread' To find active window
		thread_active_screen_ub = active_screen_ub('active_window_ub')
		thread_active_screen_ub.start()
		threads.append(thread_active_screen_ub)

		#####--4 Thread to mouse_idle
		thread_mouse_idle = class_mouse_idle('idle_mouse')
		thread_mouse_idle.start()
		threads.append(thread_mouse_idle)

		#####--5 Thread to find mouse activity
		thread_mouse = mouse_activities('mouse_activity')
		thread_mouse.start()
		threads.append(thread_mouse)

		#####--6 thread to screen shot
		thread_screen_shot_ub = screen_shot_ub('screen_shot')
		thread_screen_shot_ub.start()
		threads.append(thread_screen_shot_ub)

		#####--7 thread to conectivity
		thread_connection = connection('conectivity')
		thread_connection.start()
		threads.append(thread_connection)

		#####--8 thread to tcp
		thread_tcp = tcp_class('tcpclass')
		thread_tcp.start()
		threads.append(thread_tcp)

		#####--9 thread to sql
		thread_sql = sqldata('sql')
		thread_sql.start()
		threads.append(thread_sql)


		if not IS_LOGIN:
			login()
		else:
			icon_show()


