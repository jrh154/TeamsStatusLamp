# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 22:12:44 2023

@author: John
"""

import os
import platform
from pathlib import Path
import re
from file_read_backwards import FileReadBackwards

'''
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
'''

def teamsStatus():
    home = str(Path.home())
    logFile = home + '/appdata/roaming/Microsoft/Teams/logs.txt'

    if not os.path.isfile(logFile):
        raise Exception("Log File Not Found")

    with FileReadBackwards(logFile, encoding="utf-8") as frb:
        for line in frb:
            event = re.search("s::;m::1;a::[0-9]", line)
            if event != None:
                #print(event.group()[-1])
                if event.group()[-1] in ["0","1"]:
                    return True
                    #print("In a call")
                else:
                    return False
                    print("Not in a call")
                break
