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

def wmGetWindowPos(window):
    return map(int, getoutput(['wmiface', 'framePosition', window]).split('+')[1:])

def wmGetWindowSize(window):
    return map(int, getoutput(['wmiface', 'frameSize', window]).split('x'))

def wmSetWindowPos(window, x, y):
    call(['wmiface', 'moveFrame', window, str(x), str(y)])

def wmFindWindowAt(x, y):
    windows = []
    for window in getoutput(['wmiface', 'normalWindows', 'true']).split():
        xpos, ypos = wmGetWindowPos(window)
        width, height = wmGetWindowSize(window)
        if x > xpos + width or x < xpos or \
           y > ypos + height or y < ypos:
            continue
        xc = xpos + width / 2
        yc = ypos + height / 2
        windows.append((math.sqrt((xc - x)**2 + (yc - y)**2), window))
    if windows:
        return min(windows)[1]

def wmActivateWindow(window):
    return call(['wmiface', 'forceActiveWindow', window])

def wmGetActiveWindow():
     return getoutput(['wmiface', 'activeWindow'])

def wmMinimize(window):
    return call(['wmiface', 'minimize', window])

def wmUnminimize(window):
    return call(['wmiface', 'unminimize', window])

def wmMoveWindowRelatively(window, dx, dy):
    x, y = wmGetWindowPos(wmGetActiveWindow())
    x += dx
    y += dy
    wmSetWindowPos(window, x, y)
