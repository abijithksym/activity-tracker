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
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(m)
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
    






def get_active_window_title_win():
    import time
    from win32gui import GetWindowText, GetForegroundWindow
    while True:
        print(GetWindowText(GetForegroundWindow()))
        time.sleep(1)


if o=="Linux":
    while True:
        print(get_active_window_title())
        time.sleep(1)
else:
    get_active_window_title_win()
