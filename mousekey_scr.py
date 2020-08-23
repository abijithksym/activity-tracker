from pynput import mouse
from pynput import keyboard
import threading
import platform
import time
o=platform.system()




def get_active_window_title():
    import sys
    import os
    import subprocess
    import re
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
        return match.group("name").strip(b'"')

    return None
    
def printub():
  while True:
    print(get_active_window_title())
    time.sleep(1)
  


def get_active_window_title_win():
    import time
    from win32gui import GetWindowText, GetForegroundWindow
    while True:
        print(GetWindowText(GetForegroundWindow()))
        time.sleep(1)






def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    # if not pressed:
    #     # Stop listener
    #     return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))



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






def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    # if key == keyboard.Key.esc:
        # Stop listener
        # return False
def liskey():

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





if __name__ == '__main__':
  p1 = threading.Thread(target=liskey)
  p1.start()
  p2 = threading.Thread(target=listenmouse)
  p2.start()
  p3 = threading.Thread(target=printub)
  p4 = threading.Thread(target=get_active_window_title_win)
  if o=="Linux":
    p3.start()
  else:
    p4.start()

  p1.join()
  p2.join()
  

  