# Fixity command line application
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

import FixityCore
import FixityMail

import sys
from os import getcwd ,path  
import base64

def EncodeInfo(stringToBeEncoded):
	return base64.b16encode(base64.b16encode(stringToBeEncoded))
	
def DecodeInfo(stringToBeDecoded):
	return base64.b16decode(base64.b16decode(stringToBeDecoded.strip()))

project = sys.argv[1]

IsemailSet = None
try:
	if sys.argv[2]:
		IsemailSet = sys.argv[2]
except:
	pass
Text = '' 
projectConfNotAvailable = True
AutiFixPath = (getcwd()).replace('schedules','').replace('\\\\',"\\")
try:
	if path.isfile(AutiFixPath+ '\\bin\\'  + project + '-conf.txt'):
		
		
		fconf = open(AutiFixPath+ '\\bin\\'  + project + '-conf.txt', 'rb') 
		Text = fconf.readlines()
		fconf.close()
	else:
		projectConfNotAvailable = False
except:
	pass

if projectConfNotAvailable :
	TextEmail = ''
try:
	
	fconfEmail = open(AutiFixPath + '\\bin\\'  +'conf.txt', 'rb')
	TextEmail = fconfEmail.readlines()
	fconfEmail.close()
except:
	pass	
	
information = {} 
information['email'] = ''
information['pass'] = ''
information['onlyonchange'] = ''
information['filters'] = ''

for SingleValue in Text:
	decodedString = DecodeInfo(SingleValue)
	if decodedString.find('EOWSC|') >= 0:
		information['onlyonchange'] = decodedString.replace('EOWSC|', '').replace('\n', '')
	elif decodedString.find('fil|') >= 0:
		information['filters'] = decodedString  
			
for SingleValue in TextEmail:
	decodedString = DecodeInfo(SingleValue)
	if decodedString.find('e|') >= 0:
		information['email'] = decodedString.replace('e|', '').replace('\n', '')
	elif decodedString.find('p|') >= 0: 
		information['pass'] = decodedString.replace('p|', '').replace('\n', '')
			
f = open(AutiFixPath+'\\projects\\' + project + ".fxy", 'rb')
f.readline()
email = f.readline().rstrip("\r\n").split(';')

if '' in email:
	email.remove('')
results = []	

Fitlers = str(information['filters']).replace('fil|', '').replace('\n', '')
results = FixityCore.run(AutiFixPath+"\\projects\\" + project + ".fxy", Fitlers, project)

msg = "FIXITY REPORT:\n* " + str(results[0]) + " Confirmed Files\n* " + str(results[1]) + " Moved or Renamed Files\n* " + str(results[2]) + " New Files\n* " + str(results[3]) + " Changed Files\n* " + str(results[4]) + " Removed Files"

if results[1] > 0 or results[2] > 0 or results[3] > 0 or results[4] > 0 or information['onlyonchange'] == 'T' or IsemailSet =='Run':
	if (not information['email'] =='') and  (not information['pass'] ==''):
		for e in email:
			resposne = FixityMail.send(e, msg, results[5], information['email'] , information['pass'],project)
		