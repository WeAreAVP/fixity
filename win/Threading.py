'''
Created on Dec 11, 2013

@author: Furqan Wasi
'''
# Fixity Scheduler
# Version 0.1, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

import threading
import time
import subprocess

exitFlag = 0

class Threading (threading.Thread):
    def __init__(self, threadID, name, counter,FileName,FilePath,params):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.FileName = FileName
        self.FilePath = FilePath
        self.params = params
        
    def run(self):
        shell = True 
        command = str(self.FilePath+self.FileName +" "+self.params)
        command= command.replace('  ', ' ')
        popen = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE)
        print_time(self.name, self.counter, 5,self , command)
        

def print_time(threadName, delay, counter,thread,command):
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, str(command))
        counter -= 1