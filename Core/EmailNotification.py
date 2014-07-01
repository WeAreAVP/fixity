    # -*- coding: UTF-8 -*-
#
#@author: Furqan Wasi <furqan@avpreserve.com>

from Core import SharedApp

import email, datetime, os
from smtplib import *

class EmailNotification(object):

    def __init__(self):
        super(EmailNotification, self).__init__()
        self.Fixity = SharedApp.SharedApp.App

    #Sends Email
    #Note that ADDRESS and PASSWORD should be set before use
    #
    #Input: root, output (boolean), hash algorithm, QApplication
    #Output: list of tuples of (hash, path, id)
    #
    #
    #@param recipients: All Recipients Address
    #@param text: Message To be sent in this Email
    #@param attachment: attachment To be sent in this Email
    #@param information: Information About Email Configuration
    #@param projectName: project Name
    #@param EmailPref: Email Preferences
    #
    #@return:  Boolean True If Email Send other wise False

    def SendEmail(self, recipients, text, attachment, information, project_name=''):

        try:self.Fixity = SharedApp.SharedApp.App
        except:pass
        addr = str(information['email'])
        pas = str(information['pass'])

        msg = email.MIMEMultipart.MIMEMultipart()
        msg["From"] = addr
        msg["To"] = recipients

        if project_name == '' or project_name is None or project_name is 'None':
            msg["Subject"] = "Fixity Report: " + str(datetime.datetime.now()).rpartition('.')[0]

        else:
            msg["Subject"] = "Fixity Report: " + str(datetime.datetime.now()).rpartition('.')[0] + ' - ' + project_name

        msg.attach(email.MIMEText.MIMEText(text, 'plain'))
        part = email.mime.base.MIMEBase('application', "octet-stream")

        if attachment:
            part.set_payload(open(attachment, 'rb').read())
            email.Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
            msg.attach(part)

        protocol = str(information['protocol'])
        try:
            port = int(str(information['port']).strip())
        except:
            return False

        try:
            if protocol == 'SSL' or protocol == 'ssl':

                server = SMTP_SSL(str(information['smtp']), port)
                server.ehlo
                server.login(addr, pas)
                server.sendmail(addr, recipients, msg.as_string())
                print('sending Email....')
                return True
            if protocol == 'TLS' or protocol == 'tls':
                server = SMTP(str(information['smtp']), port)
                server.starttls()
                server.login(addr, pas)
                server.sendmail(addr, recipients, msg.as_string())
                print('sending Email....')
                return True
            else:
                server = SMTP(str(information['smtp']), port)
                server.login(addr, pas)
                server.sendmail(addr, recipients, msg.as_string())
                print('sending Email....')
                return True

        except (SMTPException, SMTPServerDisconnected,  SMTPResponseException,  SMTPSenderRefused,  SMTPRecipientsRefused,  SMTPDataError,  SMTPConnectError,  SMTPHeloError,  SMTPAuthenticationError,  Exception ):

            moreInformation= {}
            try:
                moreInformation ={'SenderEmailAddress::':addr, 'RecipientsEmailAddress':recipients,  '::More Detail':'', 'ErrorMsg':str(Exception.message)}
            except:
                pass
            self.Fixity.logger.LogException(str(moreInformation))

            return False


    def TestingEmail(self,recipients, text, information):
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        return self.SendEmail(recipients, text, None, information)

    def ReportEmail(self, recipients, attachment, text, information,project_name):
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        all_recipients = str(recipients).split(',')
        flag = True
        for single_recipients in all_recipients:

            if single_recipients.strip() != '' and single_recipients is not None:
                if self.SendEmail(single_recipients, text, attachment, information, project_name) and flag is True:
                    flag = True
                else:
                    flag = False
        return flag

    def ErrorEmail(self, recipients, attachment, text, information, project_name):
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass
        flag = True
        all_recipients = str(recipients).split(',')
        for single_recipients in all_recipients:
            if single_recipients.strip() != '' and single_recipients is not None:
                if self.SendEmail(single_recipients, text, attachment, information, project_name) and flag is True:
                    flag = True
                else:
                    flag = False
        return flag
