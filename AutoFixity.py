# Fixity command line application
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

import FixityCore
import FixityMail
from Debuger import Debuger
from Database import Database

import sys

import datetime
from os import getcwd ,path  
import base64

def EncodeInfo(stringToBeEncoded):
	return base64.b16encode(base64.b16encode(stringToBeEncoded))
	
def DecodeInfo(stringToBeDecoded):
	return base64.b16decode(base64.b16decode(stringToBeDecoded.strip()))

project = sys.argv[1]
# project = 'New_Project'
IsemailSet = None
try:
	if sys.argv[2]:
		IsemailSet = sys.argv[2]
except:
	pass
# IsemailSet = 'Run'
Text = '' 
projectConfNotAvailable = True
AutiFixPath = (getcwd()).replace('schedules','').replace('\\\\',"\\")
	
DB = Database()
Information = DB.getProjectInfo(project)
configuration =  DB.getConfiguration()


email = str(Information[0]['emailAddress']).rstrip("\r\n").split(',')

if '' in email:
	email.remove('')
results = []	

Fitlers = str(Information[0]['filters'])
results = FixityCore.run(AutiFixPath+"\\projects\\" + project + ".fxy", Fitlers, project)

msg = "FIXITY REPORT:\n* " + str(results[0]) + " Confirmed Files\n* " + str(results[1]) + " Moved or Renamed Files\n* " + str(results[2]) + " New Files\n* " + str(results[3]) + " Changed Files\n* " + str(results[4]) + " Removed Files"

if results[1] > 0 or results[2] > 0 or results[3] > 0 or results[4] > 0 or Information[0]['emailOnlyUponWarning'] == 0 or IsemailSet =='Run':
	if (not configuration[0]['email'] =='') and  (not configuration[0]['pass'] ==''):
		for e in email:
			resposne = FixityMail.send(e, msg, results[5], configuration[0],project)
		