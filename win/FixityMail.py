# Fixity Mailing Module
# Version 0.1, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from smtplib import SMTP
import email
import datetime
from os import path

# sends email
# note that ADDRESS and PASSWORD should be set before use
def send(recipients, text, attachment):
	
	addr = 'ADDRESS'

	msg = email.MIMEMultipart.MIMEMultipart()
	msg["From"] = addr
	msg["To"] = recipients
	msg["Subject"] = "Fixity Report: " + str(datetime.datetime.now()).rpartition('.')[0]

	msg.attach(email.MIMEText.MIMEText(text,'plain'))
	part = email.mime.base.MIMEBase('application', "octet-stream")
	part.set_payload(open(attachment, 'rb').read())
	email.encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename="%s"' % path.basename(attachment))
	msg.attach(part)

	server = SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(addr, 'PASSWORD')
	server.sendmail(addr, recipients, msg.as_string())
	return
