# Fixity command line application
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
'''
Created on Mar 10, 2014
@author: Furqan Wasi <furqan@geekschicago.com>
'''
#build in Library
import datetime
from os import getcwd ,path
import base64
import os
OS_Info = ''
if os.name == 'posix':
    OS_Info = 'linux'
elif os.name == 'nt':
    OS_Info = 'Windows'
elif os.name == 'os2':
    OS_Info = 'check'


#Custome Library
import FixityCore
import FixityMail
from Debuger import Debuger
from Database import Database

import datetime
from os import getcwd ,path  
import base64

class AutoRuner(object):
    #Auto Scan Runner on Given Time or on Demand
    def runAutoFix(self , project , IsemailSet):
        
        Text = '' 
        projectConfNotAvailable = True
        AutiFixPath = (getcwd()).replace('schedules','').replace('\\\\',"\\")
            
        DB = Database()
        
        Information = DB.getProjectInfo(str(project).replace('.fxy', ''))
        configuration =  DB.getConfiguration()
        
        email = {}
        emailstr = ''
        if Information != None:
            if len(Information) > 0:
                emailstr = str(Information[0]['emailAddress'])
				
        email = emailstr.split(',')        
        if len(email) > 0: 
            if '' in email:
                email.remove('')
        results = []
        Fitlers =''
        if Information != None:
            if len(Information) > 0:
                Fitlers = str(Information[0]['filters'])
        if(OS_Info == 'Windows'):
            results = FixityCore.run(AutiFixPath+"\\projects\\" + project + ".fxy", Fitlers, project)
        else:

            results = FixityCore.run(AutiFixPath+"/projects/" + project + ".fxy", Fitlers, project)
        msg = "FIXITY REPORT:\n* " + str(results[0]) + " Confirmed Files\n* " + str(results[1]) + " Moved or Renamed Files\n* " + str(results[2]) + " New Files\n* " + str(results[3]) + " Changed Files\n* " + str(results[4]) + " Removed Files"

        if(len(configuration) > 0):
            newConfiguration = configuration[0]
            newConfiguration['smtp'] = self.DecodeInfo(configuration[0]['smtp'])
            newConfiguration['email'] = self.DecodeInfo(configuration[0]['email'])
            newConfiguration['pass'] = self.DecodeInfo(configuration[0]['pass'])
        
            if results[1] > 0 or results[2] > 0 or results[3] > 0 or results[4] > 0 or Information[0]['emailOnlyUponWarning'] == 0 or IsemailSet =='Run':
                if (len(configuration) > 0):
                    if ( configuration[0]['email'] !='') and (configuration[0]['pass'] !=''):
                        for e in email:
                            
                            resposne = FixityMail.send(e, msg, results[5], newConfiguration,project)

    def EncodeInfo(self,stringToBeEncoded):
        return base64.b16encode(base64.b16encode(stringToBeEncoded))

    def DecodeInfo(self,stringToBeDecoded):
        return base64.b16decode(base64.b16decode(stringToBeDecoded.strip()))
             