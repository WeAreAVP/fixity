# -- coding: utf-8 --
# Fixity Mailing Module
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

'''
Updated on Feb 4, 2014
@author: Furqan Wasi  <furqan@geekschicago.com>
'''
from PySide.QtCore import *
from PySide.QtGui import *
from smtplib import *
import email
import datetime
from os import getcwd , path
import base64

#Custom Library
from Debuger import Debuger

DebuggerObj = Debuger()

'''
Sends Email
Note that ADDRESS and PASSWORD should be set before use

Input: root, output (boolean), hash algorithm, QApplication
Output: list of tuples of (hash, path, id)


@param recipients: All Recipients Address
@param text: Message To be sent in this Email
@param attachment: attachment To be sent in this Email
@param information: Information About Email Configuration
@param projectName: project Name
@param EmailPref: Email Preferences
  
@return:  Boolean True If Email Send other wise False 
'''
def send(recipients, text, attachment, information,projectName='', EmailPref = None):

	addr = str(information['email'])
	pas = str(information['pass'])

	msg = email.MIMEMultipart.MIMEMultipart()
	msg["From"] = addr
	msg["To"] = recipients

	if projectName == '':
		msg["Subject"] = "Fixity Report: " + str(datetime.datetime.now()).rpartition('.')[0]
	else:
		msg["Subject"] = "Fixity Report: " + str(datetime.datetime.now()).rpartition('.')[0] + ' - ' + projectName

	msg.attach(email.MIMEText.MIMEText(text, 'plain'))
	part = email.mime.base.MIMEBase('application', "octet-stream")

	if attachment:
		part.set_payload(open(attachment, 'rb').read())
		email.Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % path.basename(attachment))
		msg.attach(part)

	protocol = str(information['protocol'])
	port = int(str(information['port']).strip())


	try:
		if(protocol == 'SSL' or protocol == 'ssl'):
			server = SMTP_SSL(str(information['smtp']), port)
			server.ehlo
			server.login(addr, pas)
			server.sendmail(addr, recipients, msg.as_string())
			print('sending email')
			return True
		if(protocol == 'TLS' or protocol == 'tls'):
			server = SMTP(str(information['smtp']), port)
			server.starttls()
			server.login(addr, pas)
			server.sendmail(addr, recipients, msg.as_string())
			print('sending email')
			return True
		else:
			server = SMTP(str(information['smtp']), port)
			server.login(addr, pas)
			server.sendmail(addr, recipients, msg.as_string())
			print('sending email')
			return True


	except (SMTPException ,SMTPServerDisconnected , SMTPResponseException , SMTPSenderRefused , SMTPRecipientsRefused , SMTPDataError , SMTPConnectError , SMTPHeloError , SMTPAuthenticationError , Exception ) as Excep:
		moreInformation= {}
		try:
			moreInformation ={'SenderEmailAddress::':addr ,'RecipientsEmailAddress':recipients , '::More Detail':'' ,'ErrorCode':str(Excep[0]) , 'ErrorMsg':str(Excep[1]) }
		except:
			pass
		try:
			DebuggerObj.tureDebugerOn()
			DebuggerObj.logError('Could not send email  Line range 38 - 44 File FixityMail ', moreInformation)
		except:
			pass
		print(moreInformation)
		return False

 