# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 21:05:15 2023

@author: John
"""

# GUI Imports
import tkinter as tk
from tkinter import ttk

# Functional Imports
import serial.tools.list_ports
import os
import re

from file_read_backwards import FileReadBackwards
from time import sleep

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Teams Status Lamp')
        self.geometry("500x200")
        
        self.logPath_var = tk.StringVar(value="")
        self.comPort_var = tk.StringVar(value="")
        self.status_var = tk.StringVar(value="Not Running")
        self.is_running = tk.BooleanVar(value=False)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        
        self.create_widgets()
        
    # Build the widgets
    def create_widgets(self):
        padding = {'padx': 5, 'pady' : 5}
        
        # Get Teams Log
        browseButton = ttk.Button(self, text = "TEST1", command = self.selectFile)
        browseButton.grid(column=0, row=0, **padding)
        status1 = ttk.Label(self, textvariable=self.logPath_var)
        status1.grid(column=0, row=1, **padding)
        
        # Get COM Ports
        ports = self.listComPorts()
        # ttk.Label(self, text='COM Port').grid(column=0, row=1, **padding)
        comPortSelector = ttk.OptionMenu(self, self.comPort_var, *ports)        
        comPortSelector.grid(column=1, row =0, **padding)
        status2 = ttk.Label(self, textvariable=self.comPort_var)
        status2.grid(column=1, row=1, **padding)
        
        '''
        # Run and stop the Log Tracker
        runButton = ttk.Button(self, text = "Run", command=self.runApp)
        runButton.grid(column=0, row=2, **padding)
        stopButton = ttk.Button(self, text = "Stop", command=self.stopApp)
        stopButton.grid(column=1, row=2, **padding)
        
        # Log Status
        ttk.Label(self, text="HI").grid(column=0, row=3, **padding)
        '''
        # Callbacks
        def callBack(var, index, mode):
            print("Value Updated: " + index)
        
        self.logPath_var.trace_add("write", callBack)
        self.comPort_var.trace_add("write", callBack)
        self.status_var.trace_add("write", callBack)
        self.is_running.trace_add("write", callBack)
        
    def teamsStatus(self):
        logFile = self.logPath_var.get()
    
        if not os.path.isfile(logFile):
            self.status_var.set("ERROR: FILE NOT FOUND")
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
                        #print("Not in a call")
                    break
    
    def connectSerial(self):
        try:
            ser = serial.Serial(self.comPort_var.get(),9600)
            return ser
        except serial.SerialException:
            self.status_var.set("COM PORT IS BUSY OR NOT FOUND")
        
                
    #Select File Dialog Box
    def selectFile(self):
        self.logPath_var.set("Button Pushed!")
        
    #Get the list of available COM ports for selector
    def listComPorts(self):
        port_list = [""]
        ports = serial.tools.list_ports.comports()
        for port in ports:
            d = {port.device: port.description}
            port_list.append(d)
        return(port_list)
    
    def runApp(self):
        ser = self.connectSerial()
        self.is_running.set(True)
        
        while self.is_running.get():
            if self.teamsStatus():
                ser.write(b'on')
            else:
                ser.write(b'off')
    
    def stopApp(self):
        self.is_running.set(False)
        self.status_var.set("Not Running")
        
if __name__=="__main__":
    app = App()
    app.mainloop()