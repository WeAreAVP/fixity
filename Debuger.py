'''
Created on Feb 4, 2014
@version: 0.3
@author: Furqan Wasi
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

 

''' Class to manage all the the errors and warning loging'''
class Debuger():
    
    
    # Constuctor
    def __init__(self):
        self.loger = logging
        self.loger.basicConfig(filename=getcwd() + '\\debug\\debug.log',level=logging.DEBUG)
        self.loger.info('Logging for Date '+ str(datetime.datetime.now()).rpartition('.')[0] +"\n")
        self.isdebugerOn = False

        self.Information = self.getConfigInfo()
        
        
        
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
        
        if self.Information['debugging'] == 'debug|on':
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

 # Fetch information related to email configuration    
    def getConfigInfo(self,project=None):
        if project == None:
            information = {} 
            information['email'] = ''
            information['pass'] = ''
            information['onlyonchange'] = ''
            information['debugging'] = ''
            if path.isfile(getcwd() + '\\bin\\conf.txt'): 
                fCheck = open(getcwd() + '\\bin\\conf.txt', 'rb') 
                Text = fCheck.readlines()
                fCheck.close()
                if len(Text) > 0 :
                    for SingleValue in Text:
                        decodedString = self.DecodeInfo(SingleValue)
                        if decodedString.find('e|') >= 0:
                            information['email'] = decodedString
                        elif decodedString.find('p|') >= 0: 
                            information['pass'] = decodedString
                        elif decodedString.find('debug|') >= 0: 
                            information['debugging'] = decodedString
                        else:    
                            information['onlyonchange'] = decodedString
             
            return information
        else:    
            information = {} 
            information['onlyonchange'] = ''
            information['filters'] = ''
            information['RunWhenOnBatteryPower'] = ''
            information['IfMissedRunUponAvailable'] = ''
            information['RunInitialScan'] = ''
            information['filters'] = ''
            if path.isfile(getcwd() + '\\bin\\' + project + '-conf.txt'): 
                fCheck = open(getcwd() + '\\bin\\' + project + '-conf.txt', 'rb') 
                Text = fCheck.readlines()
                fCheck.close()
                
                if len(Text) > 0 :
                    for SingleValue in Text:
                        decodedString = self.DecodeInfo(SingleValue)
                        if decodedString.find('EOWSC|') >= 0:
                            information['onlyonchange'] = decodedString
                        elif decodedString.find('fil|') >= 0:
                            information['filters'] = decodedString
                        elif decodedString.find('RWOBP|') >= 0:
                            information['RunWhenOnBatteryPower'] = decodedString  
                        elif decodedString.find('IMRUA|') >= 0:
                            information['IfMissedRunUponAvailable'] = decodedString
                        elif decodedString.find('RIS|') >= 0:
                            information['RunInitialScan'] = decodedString
                        
                                              
        return information
    
    
    # Triggers     
    def EncodeInfo(self, stringToBeEncoded):
        stringToBeEncoded = str(stringToBeEncoded).strip()
        return base64.b16encode(base64.b16encode(stringToBeEncoded))
    
    def DecodeInfo(self, stringToBeDecoded):
        stringToBeDecoded = str(stringToBeDecoded).strip()
        return base64.b16decode(base64.b16decode(stringToBeDecoded))
    
# app = QApplication('asdas')
# w = FilterFiles()
# w.CreateWindow()
# w.SetWindowLayout()
# w.SetDesgin()
# w.ShowDialog()
#       
# app.exec_() 

            