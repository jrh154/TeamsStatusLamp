# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 21:05:15 2023

@author: John Hayes
"""

# GUI Imports
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk

# Tray Minimize Imports
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk

# Functional Imports
import serial.tools.list_ports
import os
import re
from file_read_backwards import FileReadBackwards

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Teams Status Lamp')
        self.geometry("500x200")
        
        # Set status variables
        self.logPath_var = tk.StringVar(value="")
        self.comPort_var = tk.StringVar(value="")
        self.status_var = tk.StringVar(value="Not Running")
        self.is_running = tk.BooleanVar(value=False)
        
        # Set Paths
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        
        # Define serial variable
        self.ser = None
        
        # Instantiate the widgets
        self.create_widgets()
        
        # Icon and Tray Minimize
        self.icon_image = Image.open("tray_icon.ico")
        self.iconbitmap("tray_icon.ico")
        self.tray_menu = (item('Quit', self.quit_window), item('Show', self.show_window))
        self.protocol('WM_DELETE_WINDOW', self.withdraw_window)
        
        # Run the app continuously (uses after method)
        self.runApp()
        
    # Build the widgets
    def create_widgets(self):
        '''
        Instantiate the widgets and their functions

        Returns
        -------
        None.

        '''
        padding = {'padx': 5, 'pady' : 5}
        
        # Get Teams Log
        ttk.Label(self, text='Teams Log: ').grid(column=0, row=0, **padding)
        logPath_entry= ttk.Entry(self, textvariable=self.logPath_var)
        logPath_entry.grid(column=1, row=0, **padding)
        browseButton = ttk.Button(self, text = "Browse", command = self.selectFile)
        browseButton.grid(column=2, row=0, **padding)
        
        # Get COM Ports
        ports = self.listComPorts()
        ttk.Label(self, text='COM Port').grid(column=0, row=1, **padding)
        comPortSelector = ttk.OptionMenu(self, self.comPort_var, *ports)        
        comPortSelector.grid(column=1, row =1, **padding)
        connectButton = ttk.Button(self,text="Connect", command = self.connectSerial)
        connectButton.grid(column=2, row = 1, **padding)
        
        # Run Tracker
        runButton = ttk.Button(self, text = "Run", command=lambda:self.is_running.set(True))
        runButton.grid(column=0, row=2, **padding)
        
        # Stop Tracker
        stopButton = ttk.Button(self, text = "Stop", command=self.stopApp)
        stopButton.grid(column=1, row=2, **padding)
        
        # App Status
        ttk.Label(self, textvariable=self.status_var).grid(column=0, row=3, **padding)

    def extractComPort(self):
        '''
        Extracts the COM Port from the 

        Returns
        -------
        s : String
            Selected COM Port

        '''
        s = self.comPort_var.get()
        s = s.split(" ")
        s = s[0]
        s = s[2:-2]
        return s 
    
    def selectFile(self):
        '''
        Select a file using the file browser and store the path in logPath_var

        Returns
        -------

        '''        
        file = filedialog.askopenfilename()
        self.logPath_var.set(file)
        
    #Get the list of available COM ports for selector
    def listComPorts(self):
        '''
        Generate a list of available com ports (in dictionary form)

        Returns
        -------
        List

        '''
        port_list = [""]
        ports = serial.tools.list_ports.comports()
        for port in ports:
            d = {port.device: port.description}
            port_list.append(d)
        return(port_list)
                
    def teamsStatus(self):
        '''
        Read the log file and determine the current status on Teams

        Raises
        ------
        Exception
            Sets status_var when file not found

        Returns
        -------
        bool
            Status of the Teams (on call = True)

        '''
        logFile = self.logPath_var.get()
    
        if not os.path.isfile(logFile):
            self.status_var.set("ERROR: FILE NOT FOUND")
            return
            #raise Exception("Log File Not Found")
    
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
        com = self.extractComPort()
        try:
            self.ser.close()
        except AttributeError:
            pass
        
        try:
            self.ser = serial.Serial(com,9600)
            self.status_var.set("Serial is Connected")
        except serial.SerialException:
            self.status_var.set("COM PORT NOT FOUND")
        except serial.serialutil.PortNotOpenError:
            self.status_var.set("COM PORT NOT OPEN")
            
    def runApp(self):        
        print(self.is_running.get())
        
        try:
            if self.is_running.get() and self.ser.isOpen():
                self.status_var.set("Running!")
                print("made it this far!")
                if self.teamsStatus():
                    self.ser.write(b'on')
                    print("In Meeting")
                else:
                    self.ser.write(b'off')
                    print("Not in Meeting")
            else:
                is_running.set(False)
        except:
            self.is_running.set(False)
        finally:
            self.after(1000, self.runApp)
    
    def stopApp(self):
        self.is_running.set(False)
        
        try:
            self.ser.write(b'off')
            self.ser.close()
        except AttributeError:
            pass
        except serial.serialutil.PortNotOpenError:
            pass        

        self.status_var.set("Not Running")
    
    def quit_window(self):
        self.icon.stop()
        self.stopApp()
        self.destroy()
    
    def show_window(self):
        self.icon.stop()
        self.protocol("WM_DELETE_WINDOW", self.withdraw_window)
        self.after(0, self.deiconify)
    
    def withdraw_window(self):
        self.withdraw()
        self.icon = pystray.Icon("name", self.icon_image, "Teams Status Lamp", self.tray_menu)
        self.icon.run()
    
    
    
    
if __name__=="__main__":
    app = App()
    app.mainloop()