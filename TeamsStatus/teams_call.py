import os
import platform
from pathlib import Path
import re

def getLogFile():
    uname = platform.uname()
    home = str(Path.home())

    if uname.system == 'Linux':
        return home + '/.config/Microsoft/Microsoft Teams/logs.txt'
    elif uname.system == 'Windows':
        return (home + '/appdata\roaming\Microsoft\Teams\logs.txt')
    else:
        raise Exception('OS not supported!')

def isInCall():
    logFile = getLogFile()
    print(logFile)
    if not os.path.isfile(logFile):
        raise Exception('Log file not found: ' + logFile)

    output = os.popen('tac "' + logFile +  '" | grep -oh "eventData: s::;m::1;a::[0-9]" | head -n1').read().split('\n')

    if output[0][-1] in ['0', '1']:
        #print("In Call")
        return True
    else:
        #print("Not In Call")
        return False

if __name__ == '__main__':
    isInCall()
