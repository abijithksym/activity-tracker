import time
from win32gui import GetWindowText, GetForegroundWindow
while True:
    print(GetWindowText(GetForegroundWindow()))
    time.sleep(3)
