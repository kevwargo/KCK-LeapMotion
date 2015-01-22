import subprocess

def wmGetCurrentDesktop():
    try:
        return int(subprocess.check_output(['wmiface', 'currentDesktop']))
    except subprocess.CalledProcessError:
        print 'error getting number of current desktop'

def wmLeftDesktop():
    return subprocess.call(['wmiface', 'setCurrentDesktop', str(wmGetCurrentDesktop() - 1)])

def wmRightDesktop():
    return subprocess.call(['wmiface', 'setCurrentDesktop', str(wmGetCurrentDesktop() + 1)])

