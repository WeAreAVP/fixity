'''
Created on Dec 11, 2013
@version: 0.3
@author: Furqan Wasi
'''
# Fixity Scheduler
# Version 0.3, 2013-12-16
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0




import threading
import time
import subprocess
import tkMessageBox
exitFlag = 0


# Custom class to run the scanning process using multithreading  


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
        command= '"'+command+ self.FileName +'"'
                
        command = command +" "+self.params
        

        popen = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = popen.communicate()
        errcode = popen.returncode
        print_time(self.name, self.counter, 5,self , command)
        

def print_time(threadName, delay, counter,thread,command):
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        counter -= 1
        
