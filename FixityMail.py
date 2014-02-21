# Fixity Mailing Module
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
from PySide.QtCore import *
from PySide.QtGui import *
from smtplib import *
import email
import datetime
from os import getcwd , path

from Debuger import Debuger

# sends email
# note that ADDRESS and PASSWORD should be set before use
def send(recipients, text, attachment, emailaddr, password,projectName=''):
	addr = str(emailaddr)
	pas = str(password) 
	
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
		
	try:	
		server = SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(addr, pas)
		server.sendmail(addr, recipients, msg.as_string())
		return True
	except (SMTPException ,SMTPServerDisconnected , SMTPResponseException , SMTPSenderRefused , SMTPRecipientsRefused , SMTPDataError , SMTPConnectError , SMTPHeloError , SMTPAuthenticationError , Exception ) as e:
		
		D = Debuger()
		D.tureDebugerOn();
		try:
			moreInformation ={'SenderEmailAddress::':addr ,'RecipientsEmailAddress':recipients , '::More Detail':'' ,'ErrorCode':str(e[0]) , 'ErrorMsg':str(e[1]) }
		except:
			pass
		D.logError('Could not send email  Line range 38 - 44 File FixityMail ', moreInformation)
		
		msgBox = QMessageBox();
		msgBox.setText("Fixity was unable to send email.\n*Please ensure that you are connected to the Internet\n*Please ensure that your email credentials are correct")
		msgBox.exec_()
		return False
