# -- coding: utf-8 --
# Fixity command line application helper
# Version 0.4, Apr 1, 2014
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
'''
Created on Mar 10, 2014
@author: Furqan Wasi <furqan@geekschicago.com>
'''

import os
OS_Info = ''
if os.name == 'posix':
    OS_Info = 'linux'
elif os.name == 'nt':
    OS_Info = 'Windows'
elif os.name == 'os2':
    OS_Info = 'check'

#build in Library
import datetime
from os import getcwd ,path  
import base64


# Custom Library
from Debuger import Debuger
from Database import Database

import FixityCore
    
    
import FixityMail
'''
Auto Scan Runner on Given Time or on Demand
'''


class AutoRuner(object):
    
    
    ''' Auto Scan Runner on Given Time or on Demand '''
    def runAutoFix(self , project , isEmailSendingSet):
        
        AutiFixPath = (getcwd()).replace('schedules','').replace('\\\\',"\\")
            
        DB = Database()
        Information = DB.getProjectInfo(str(project).replace('.fxy', ''))
        configuration =  DB.getConfiguration()
         
        emailOfReciverUsers = {}
        emailOfReciverUsersStr = ''
        if Information != None:
            if len(Information) > 0:
                emailOfReciverUsersStr = str(Information[0]['emailAddress'])

        emailOfReciverUsers = emailOfReciverUsersStr.split(',')        
        if len(emailOfReciverUsers) > 0: 
            if '' in emailOfReciverUsers:
                emailOfReciverUsers.remove('')
                
        results = []
        Fitlers =''
        print('------------- Fitlers ===================')
        if Information is not None:
            if len(Information) > 0:
                Fitlers = str(Information[0]['filters'])
        print(Fitlers)
        print('------------- Fitlers ===================')
        if(OS_Info == 'Windows'):
            results = FixityCore.run(AutiFixPath+"\\projects\\" + project + ".fxy", Fitlers, project)
        else:
            results = FixityCore.run(AutiFixPath+"/projects/" + project + ".fxy", Fitlers, project)
        
        reportGeneratedForEmail = "FIXITY REPORT:\n* " + str(results[0]) + " Confirmed Files\n* " + str(results[1]) + " Moved or Renamed Files\n* " + str(results[2]) + " New Files\n* " + str(results[3]) + " Changed Files\n* " + str(results[4]) + " Removed Files"
        

        if(len(configuration) > 0):
            newConfiguration = configuration[0]
            if configuration[0]['smtp'] !='' or configuration[0]['smtp'] is not None and configuration[0]['smtp'] !='None':
                newConfiguration['smtp'] = self.DecodeInfo(configuration[0]['smtp'])
                
            if configuration[0]['email'] !='' or configuration[0]['email'] is not None and configuration[0]['email'] !='None':
                newConfiguration['email'] = self.DecodeInfo(configuration[0]['email'])
                
            if configuration[0]['pass'] !='' or configuration[0]['pass'] is not None and configuration[0]['pass'] !='None':
                newConfiguration['pass'] = self.DecodeInfo(configuration[0]['pass'])
        
        
            if results[1] > 0 or results[2] > 0 or results[3] > 0 or results[4] > 0 or Information[0]['emailOnlyUponWarning'] == 0 or isEmailSendingSet =='Run':
                if (len(configuration) > 0):
                    if ( configuration[0]['email'] !='') and (configuration[0]['pass'] !=''):
                        for e in emailOfReciverUsers:
                            FixityMail.send(e, reportGeneratedForEmail, results[5], newConfiguration,project)



    def EncodeInfo(self,stringToBeEncoded):
        if stringToBeEncoded is not None:
            return base64.b16encode(base64.b16encode(stringToBeEncoded))

    def DecodeInfo(self,stringToBeDecoded):
        
        if stringToBeDecoded is not None:
            return base64.b16decode(base64.b16decode(stringToBeDecoded))