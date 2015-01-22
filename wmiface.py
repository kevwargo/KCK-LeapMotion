from subprocess import check_output as getoutput
from subprocess import call
from subprocess import CalledProcessError
import math

def wmGetCurrentDesktop():
    try:
        return int(getoutput(['wmiface', 'currentDesktop']))
    except CalledProcessError:
        print 'error getting number of current desktop'

def wmLeftDesktop():
    return call(['wmiface', 'setCurrentDesktop', str(wmGetCurrentDesktop() - 1)])

def wmRightDesktop():
    return call(['wmiface', 'setCurrentDesktop', str(wmGetCurrentDesktop() + 1)])

def wmFindWindowAt(x, y):
    windows = []
    for window in getoutput(['wmiface', 'normalWindows', 'true']).split():
        xpos, ypos = map(int, getoutput(['wmiface', 'framePosition', window]).split('+')[1:])
        width, height = map(int, getoutput(['wmiface', 'frameSize', window]).split('x'))
        xc = xpos + width / 2
        yc = ypos + height / 2
        windows.append((math.sqrt((xc - x)**2 + (yc - y)**2), window))
    if windows:
        return min(windows)[1]

def wmActivateWindow(window):
    call(['wmiface', 'forceActiveWindow', window])
