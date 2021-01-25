from tkinter import *
import tkinter as tk

from functools import partial
import tkinter.font as font
import os


def login_verify():
	username1 = username_verify.get()
	password1 = password_verify.get()
	username_login_entry.delete(0, END)
	password_login_entry.delete(0, END)

	list_of_files = os.listdir()
	if username1 in list_of_files:
		file1 = open(username1, "r")
		verify = file1.read().splitlines()
		if password1 in verify:
			run()
			

		else:
			# password_not_recognised()
			Label(login_screen, text="wrong password").pack()

	else:
		# user_not_found()
		Label(login_screen, text="user not found").pack()


# Designing popup for login success
def user_not_found():
	global user_not_found_screen
	# user_not_found_screen = Toplevel(login_screen)
	user_not_found_screen = Tk()
	user_not_found_screen.eval('tk::PlaceWindow . center')
	user_not_found_screen.title("Success")
	user_not_found_screen.geometry("150x100")
	Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

# def user_not_found():
# 	Label(login_screen, text="User Not Found").pack()
# 	# login_screen.destroy()
# 	label.destroy()
# 	# login()
def run():
	login_screen.withdraw()
	os.system('python3 activitytracker.py')
	# login_screen.destroy()



# def login_success():
# 	Label(login_screen, text="login success").pack()
# 	# login_screen.destroy()

def login():
	global login_screen
	login_screen = Tk()
	# login_screen = Toplevel(main_screen)
	login_screen.eval('tk::PlaceWindow . center')
	login_screen.title("Login")
	login_screen.geometry("300x250")
	# remove maximize button
	login_screen.resizable(0,0)


	Label(login_screen, text="Please enter details below to login").pack()
	Label(login_screen, text="").pack()

	global username_verify
	global password_verify

	username_verify = StringVar()
	password_verify = StringVar()

	global username_login_entry
	global password_login_entry

	Label(login_screen, text="Username * ").pack()
	username_login_entry = Entry(login_screen, textvariable=username_verify)
	username_login_entry.pack()
	Label(login_screen, text="").pack()
	Label(login_screen, text="Password * ").pack()
	password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
	password_login_entry.pack()
	Label(login_screen, text="").pack()
	Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()
	login_screen.mainloop()
login()