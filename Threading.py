# Fixity Scan files Threads handler
# Version 0.3, 2013-12-16
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
'''
Created on Dec 11, 2013
@author: Furqan Wasi  <furqan@geekschicago.com>
'''

#Bult-in Libraries
import threading
import time
import subprocess

#Custom Libraries
from Debuger import Debuger
from AutoRuner import AutoRuner

exitFlag = 0
Debuging = Debuger()


# Custom class to run the scanning process using Multi-Threading
class Threading (threading.Thread):
    def __init__(self, threadID, name, counter,FileName,FilePath,params):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.FileName = FileName
        self.FilePath = FilePath
        self.params = params

    # Run thread to scan the given Given file path using given command
    def run(self):

        command = str(self.FilePath)
        command = command + 'fixity-'+self.name+'.vbs'

        try:
            IsemailSet = ''
            AR = AutoRuner()
            AR.runAutoFix(self.name, IsemailSet)

        except Exception as e:
            moreInformation = {"moreInfo":'null'}
            try:
                if not e[0] == None:
                    moreInformation['LogsMore'] =str(e[0])
            except:
                pass
            try:
                if not e[1] == None:
                    moreInformation['LogsMore1'] =str(e[1])
            except:
                pass

            Debuging.tureDebugerOn()
            Debuging.logError('Configuration File Dose not exist  Line range 48 - 51 File Threading ', moreInformation)
            pass
        print_time(self.name, self.counter, 5,self , command)

def print_time(threadName, delay, counter,thread,command):
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        counter -= 1
