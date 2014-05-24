from Core import SharedApp

import email, datetime, os
from smtplib import *
from Core import Database
class EmailNotification(object):

    def __init__(self):

        super(EmailNotification, self).__init__()
        self.Fixity = SharedApp.SharedApp.App

        self.Database = Database.Database()

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
        port = int(str(information['port']).strip())


        try:
            if protocol == 'SSL' or protocol == 'ssl':

                server = SMTP_SSL(str(information['smtp']), port)
                server.ehlo
                server.login(addr, pas)
                server.sendmail(addr, recipients, msg.as_string())
                print('sending email')
                return True
            if protocol == 'TLS' or protocol == 'tls' :
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


        except (SMTPException, SMTPServerDisconnected,  SMTPResponseException,  SMTPSenderRefused,  SMTPRecipientsRefused,  SMTPDataError,  SMTPConnectError,  SMTPHeloError,  SMTPAuthenticationError,  Exception ):

            moreInformation= {}
            try:
                moreInformation ={'SenderEmailAddress::':addr, 'RecipientsEmailAddress':recipients,  '::More Detail':'', 'ErrorMsg':str(Exception.message)}
            except:
                pass
            self.Fixity.logger.LogException(str(moreInformation))

            return False


    def TestingEmail(self,recipients, text, information):
        print(information)
        return self.SendEmail(recipients, text, None, information)

    def ReportEmail(self, recipients, attachment, text, information):
        return self.SendEmail(recipients, text, attachment, information)

    def ErrorEmail(self, recipients, attachment, text, information):
        return self.SendEmail(recipients, text, attachment, information)
