# Manage Debugging of Fixity
# Version 0.4, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
'''
Created on Feb 4, 2014
@author: Furqan Wasi  <furqan@geekschicago.com>
'''
# Fixity Scheduler
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

import logging
import datetime
import base64
from os import getcwd  , path

import os
OS_Info = ''
if os.name == 'posix':
    OS_Info = 'linux'
elif os.name == 'nt':
    OS_Info = 'Windows'
elif os.name == 'os2':
    OS_Info = 'check'

''' Class to manage all the the errors and warning loging'''
class Debuger(object):


    # Constuctor
    def __init__(self):

        self.configFilePath= getcwd()+ str(os.sep)+'bin' +str(os.sep)+'conf.txt'
        self.loger = logging
        if not path.isfile(self.configFilePath):
           file =  open(self.configFilePath,'w+')
           file.write('debugger:0')
           file.close()

        if(OS_Info == 'Windows'):
            self.loger.basicConfig(filename=getcwd() +str(os.sep)+'debug'+str(os.sep)+'debug.log',level=logging.DEBUG)
        else:
            self.loger.basicConfig(filename=getcwd() +str(os.sep)+'debug'+str(os.sep)+'debug.log',level=logging.DEBUG)

        self.isdebugerOn = False

        self.Information ={}

        self.Information = self.getDebugConfiguration()


    # Function to Log Errors
    # @param msg Message to log
    def logError(self,msg,moreInformation = None):
        if(self.isdebugerOn):
            self.loger.debug(msg)
            if(moreInformation):
                for key in moreInformation:
                    self.loger.debug(key + '::' + moreInformation[key]+"\n")



    # Function to Log Information
    # @param msg Message to log
    def logInfo(self,msg,moreInformation = None):
        if(self.isdebugerOn):
            self.loger.info(msg)
            if(moreInformation):
                for key in moreInformation:
                    self.loger.info(key + '::' + moreInformation[key]+"\n")

    # Function to Log Warning
    # @param msg Message to log
    def logWarning(self,msg,moreInformation = None):
        if(self.isdebugerOn):
            self.loger.warning(msg)
            if(moreInformation):
                for key in moreInformation:
                    self.loger.warning(key + '::' + moreInformation[key]+"\n")


    # Function to turn debugging On
    def tureDebugerOn(self):
        self.loger.info('Logging for Date '+ str(datetime.datetime.now()).rpartition('.')[0] +"\n")
        if self.Information['debugger'] == 1:
            self.isdebugerOn = True
        else:
            self.isdebugerOn = False

    # Function to turn debugging of
    def tureDebugerOff(self):
        self.isdebugerOn = False

    # Function to Get Current Time
    def getCurrentTime(self):
        if(self.isdebugerOn):
            return str(datetime.datetime.now()).rpartition('.')[0]
    #Set Debug On or Off information
    def setDebugConfiguration(self,flagOfDebug):
        try:
            ConfigFile = open(self.configFilePath, 'w+')
            ConfigFile.write('debugger:'+str(flagOfDebug))
            ConfigFile.close()
        except Exception as ex :
            moreInformation = {"moreInfo":'null'}
            try:
                if not ex[0] == None:
                    moreInformation['LogsMore'] =str(ex[0])
            except:
                pass

            try:
                if not ex[1] == None:
                    moreInformation['LogsMore1'] =str(ex[1])
            except:
                pass

            self.tureDebugerOn()
            self.logError('Error Reporting 36 - 42 File Database While Connecting for database information'+"\n", moreInformation)
    #Get Debug On or Off information
    def getDebugConfiguration(self):
        Information = {}
        Information['debugger'] = 0
        try:
            ConfigFile = open(self.configFilePath, 'r+')
            debugline  = ConfigFile.readline()
            ConfigFile.close()

            debugInfo = str(debugline).split(':')
            Information[str(debugInfo[0])] = int(debugInfo[1])

        except Exception as ex :
            moreInformation = {"moreInfo":'null'}
            try:
                if not ex[0] == None:
                    moreInformation['LogsMore'] =str(ex[0])
            except:
                pass
            try:
                if not ex[1] == None:
                    moreInformation['LogsMore1'] =str(ex[1])
            except:
                pass

            self.tureDebugerOn()
            self.logError('Error Reporting 36 - 42 File Database While Connecting for database information'+"\n", moreInformation)

        return Information
