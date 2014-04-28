# -- coding: utf-8 --
# Fixity Scan files Threads handler
# Version 0.3, 2013-12-16
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
'''
Created on Dec 11, 2013
@author: Furqan Wasi  <furqan@geekschicago.com>
'''
# Fixity Scheduler
# Version 0.3, 2013-12-16
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

#Bult-in Libraries
import threading
import time
import subprocess

#Custom Libraries
from Debuger import Debuger
from AutoRuner import AutoRuner

global verifiedFiles
exitFlag = 0
Debuging = Debuger()


'''
Custom class to run the scanning process using Multi-Threading
'''
class Threading (threading.Thread):
    '''
    Constructor
    '''
    def __init__(self, threadID, name, counter,FileName,FilePath,params):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.FileName = FileName
        self.FilePath = FilePath
        self.params = params

    '''
    Run thread to scan the given Given file path using given command
    '''
    def run(self):

        command = str(self.FilePath)
        command = command + 'fixity-'+self.name+'.vbs'
        
        try:
            IsemailSet = ''
            verifiedFiles = []
            AR = AutoRuner()
            print('asdasdas')
            AR.runAutoFix(self.name, IsemailSet)

        except Exception as exep:
            moreInformation = {"moreInfo":'null'}
            try:
                if not exep[0] == None:
                    moreInformation['LogsMore'] =str(exep[0])
            except:
                pass
            try:
                if not exep[1] == None:
                    moreInformation['LogsMore1'] =str(exep[1])
            except:
                pass
            print(moreInformation)
            Debuging.tureDebugerOn()
            Debuging.logError('Configuration File Dose not exist  Line range 48 - 51 File Threading ', moreInformation)
            pass
        TriggerThread(self.name, self.counter, 5,self , command)
        
'''
Manage Thread Run Time
'''
def TriggerThread(threadName, delay, counter,thread,command):
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        counter -= 1