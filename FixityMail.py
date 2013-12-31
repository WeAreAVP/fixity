# Fixity Mailing Module
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
from PySide.QtCore import *
from PySide.QtGui import *
from smtplib import SMTP
import email
import datetime
from os import getcwd , path

# sends email
# note that ADDRESS and PASSWORD should be set before use
def send(recipients, text, attachment, emailaddr, password):
	addr = str(emailaddr)
	pas = str(password) 

	msg = email.MIMEMultipart.MIMEMultipart()
	msg["From"] = addr
	msg["To"] = recipients
	msg["Subject"] = "Fixity Report: " + str(datetime.datetime.now()).rpartition('.')[0]
	
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
	except Exception:

		msgBox = QMessageBox();
		msgBox.setText("Some Problem occurred while sending the email, please check your Internet Connection or try different Email Credentials and try again.")
		msgBox.exec_()
		return False
