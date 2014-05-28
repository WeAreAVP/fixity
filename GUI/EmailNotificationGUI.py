'''
Created on May 14, 2014
@author: Furqan <furqan@geekschicago.com>
'''

from GUI import GUILibraries
from Core import SharedApp
from Core import EmailNotification
__author__ = 'Furqan'

# Class to manage the Filter to be implemented for the files with specific extensions


class EmailNotificationGUI(GUILibraries.QDialog):
    def __init__(self,parent_win):
        GUILibraries.QDialog.__init__(self,parent_win)

        self.Fixity = SharedApp.SharedApp.App
        self.parent_win = parent_win
        self.setWindowModality(GUILibraries.Qt.WindowModal)
        self.parent_win.setWindowTitle('Configure Sender Email')
        self.email_notification = EmailNotification.EmailNotification()
        self.setWindowIcon(GUILibraries.QIcon(str(self.Fixity.Configuration.getLogoSignSmall())))
        self.email_pref_layout = GUILibraries.QVBoxLayout()
        self.notification = GUILibraries.NotificationGUI.NotificationGUI()

    def reject(self):
        try:
            self.parent_win.setWindowTitle("Fixity "+self.Fixity.Configuration.getApplicationVersion())

        except:
            pass
        try:
            super(EmailNotificationGUI,self).reject()
        except:
            pass
    #Distructor

    def destroy(self):
        del self


    #
    # Show Dialog
    #
    # @return: None
    #
    def ShowDialog(self):
        self.show()
        self.exec_()

    '''
    Set Layout

    @return: None
    '''
    def SetLayout(self, layout):
        self.email_pref_layout = layout

    '''
    Set layout for windows

    @return: None
    '''
    def SetWindowLayout(self):
        self.setLayout(self.email_pref_layout)


    '''
    All design Management Done in Here

    @return: None
    '''
    def SetDesgin(self):
        self.GetLayout().addStrut(200)
        self.Fixity.Configuration.fetchEmailConfiguration()
        self.email_addr_bar = GUILibraries.QLineEdit()
        self.out_going_mail_server = GUILibraries.QLineEdit()
        self.port = GUILibraries.QLineEdit()
        self.password = GUILibraries.QLineEdit()
        self.SSL_protocol = GUILibraries.QRadioButton("SSL Protocols")
        self.TLS_protocol = GUILibraries.QRadioButton("TLS Protocols")
        self.none_protocol = GUILibraries.QRadioButton("None")

        self.password.setEchoMode(GUILibraries.QLineEdit.Password)
        self.set_information = GUILibraries.QPushButton("Save && Close")
        self.reset = GUILibraries.QPushButton("Reset")
        self.check_email = GUILibraries.QPushButton("Check Credentials")
        self.cancel = GUILibraries.QPushButton("Close Without Saving")
        self.loader = GUILibraries.QLabel("Sending Email...")

        self.email_addr_bar.setPlaceholderText("email: user@domain.com")
        self.password.setPlaceholderText("password")
        self.out_going_mail_server.setPlaceholderText("smtp.gmail.com")
        self.port.setPlaceholderText("Port")

        self.email_addr_bar.setMaximumSize(200, 100)
        self.password.setMaximumSize(200, 100)
        self.reset.setMaximumSize(200, 100)
        self.cancel.setMaximumSize(200, 100)
        self.set_information.setMaximumSize(200, 100)
        self.out_going_mail_server.setMaximumSize(200, 100)
        self.port.setMaximumSize(200, 100)
        self.check_email.setMaximumSize(200, 100)

        self.SMTP_server_lable = GUILibraries.QLabel('SMTP Server')
        self.email_address_lable = GUILibraries.QLabel('Email Address')
        self.password_lable = GUILibraries.QLabel('password')
        self.port_lable = GUILibraries.QLabel('Port')
        self.encryption_lable = GUILibraries.QLabel('Encryption Method')

        self.GetLayout().addWidget(self.loader)
        self.GetLayout().addWidget(self.SMTP_server_lable)
        self.GetLayout().addWidget(self.out_going_mail_server)

        self.GetLayout().addWidget(self.email_address_lable)
        self.GetLayout().addWidget(self.email_addr_bar)

        self.GetLayout().addWidget(self.password_lable)
        self.GetLayout().addWidget(self.password)

        self.GetLayout().addWidget(self.port_lable)
        self.GetLayout().addWidget(self.port)

        self.GetLayout().addWidget(self.encryption_lable)
        self.GetLayout().addWidget(self.SSL_protocol)
        self.GetLayout().addWidget(self.TLS_protocol)
        self.GetLayout().addWidget(self.none_protocol)
        self.GetLayout().addWidget(self.set_information)
        self.GetLayout().addWidget(self.check_email)
        self.GetLayout().addWidget(self.reset)
        self.GetLayout().addWidget(self.cancel)

        self.loader.hide()

        self.reset.clicked.connect(self.ResetForm)
        self.set_information.clicked.connect(self.Save)
        self.cancel.clicked.connect(self.CloseClick)
        self.check_email.clicked.connect(self.checkIsEmailValid)
        self.SSL_protocol.clicked.connect(self.SSL_protocolConif)
        self.TLS_protocol.clicked.connect(self.TLS_protocolConif)
        self.none_protocol.clicked.connect(self.none_protocolConif)

        self.SSL_protocol.setChecked(True)
        self.SSL_protocol.click()
        self.SetWindowLayout()
        information = self.Fixity.Configuration.getEmailConfiguration()
        self.out_going_mail_server.setText('smtp.gmail.com')
        self.setInformation(information)
        try:
                if information is not None and len(information) > 0 and information['smtp'] != None:
                    self.setInformation(information)
        except:
            pass



    def setInformation(self, information):

        email_addr = ''
        Pass = ''
        port = ''
        smtp = ''
        protocol = ''

        if information :
            if(len(information)> 0):
                email_addr = information['email']
                Pass = str(information['pass'])
                port = str(information['port'])
                smtp = str(information['smtp'])
                protocol = str(information['protocol'])
        self.email_addr_bar.setText(email_addr)
        self.password.setText(Pass)

        if smtp is not None and smtp != '':
            self.out_going_mail_server.setText(smtp)
        else:
            self.out_going_mail_server.setText('smtp.gmail.com')

        if protocol == 'SSL':
            self.SSL_protocol.setChecked(True)
            self.TLS_protocol.setChecked(False)
            self.none_protocol.setChecked(False)

            if port is not None and port != '' :
                self.port.setText(port)
            else:
                self.port.setText('465')

        elif protocol == 'TLS':
            self.TLS_protocol.setChecked(True)
            self.SSL_protocol.setChecked(False)
            self.none_protocol.setChecked(False)
            if(port is not None and port !='' ):
                self.port.setText(port)
            else:
                self.port.setText('587')
        else:
            self.none_protocol.setChecked(True)
            self.TLS_protocol.setChecked(False)
            self.SSL_protocol.setChecked(False)
            if port is not None and port != '' :
                self.port.setText(port)
            else:
                self.port.setText('25')
    '''
    Function to Reset Form information
    @return: None
    '''
    def ResetForm(self):
        self.email_addr_bar.setText('')
        self.password.setText('')
        self.out_going_mail_server.setText('')
        self.port.setText('')



    '''
    Validation Configuration provided
    @param Email: Email Address
    @param Pass: password to check

    @return: String Message of success or failure
    '''
    def validateInformation(self, Email, Pass):
        msgEmailValidation = None
        if Pass == '':
            msgEmailValidation = GUILibraries.messages['provide_valid_pass']
            return msgEmailValidation
        if not GUILibraries.re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            msgEmailValidation = GUILibraries.messages['provide_valid_email']
            return msgEmailValidation
        return True

    '''
    Manage click on close

    @return: None
    '''
    def CloseClick(self):
        try:
            self.setWindowTitle("Fixity "+self.Fixity.Configuration.getApplicationVersion())

        except:
            pass
        self.destroy()
        self.close()

    '''
    TSL configuration manager

    @return: None
    '''
    def TLS_protocolConif(self):
        information = self.getConfigInfo()
        try:
            port = str(information['port'])
        except:
            port = ''
            pass

        if(port is not None and port !='' ):
            self.port.setText(port)
        else:
            self.port.setText('587')
    '''
    SSL configuration manager

    @return: None
    '''
    def SSL_protocolConif(self):
        information = self.getConfigInfo()
        try:
            port = str(information['port'])
        except:
            port = ''
            pass

        if(port is not None and port !='' ):
            self.port.setText(port)
        else:
            self.port.setText('465')


    '''
    No Encryption Manager

    @return: None
    '''
    def none_protocolConif(self):
        information = self.getConfigInfo()
        try:
            port = str(information['port'])
        except:
            port = ''
            pass

        if port is not None and port != '' :
            self.port.setText(port)
        else:
            self.port.setText('587')

    def destroy(self):
        del self

    def checkIsEmailValid(self):

        self.loader.show()
        GUILibraries.QCoreApplication.processEvents()
        Email = self.email_addr_bar.text()
        Pass = self.password.text()
        port = self.port.text()
        out_going_mail_server = self.out_going_mail_server.text()

        if self.SSL_protocol.isChecked():
            protocol = 'SSL'
        elif self.TLS_protocol.isChecked():
            protocol = 'TLS'
        else:
            protocol = 'NONE'

        if self.out_going_mail_server.text() is None or self.out_going_mail_server.text() == '':
            self.notification.showWarning(self, 'Error', GUILibraries.messages['invalid_smtp_given'])
            self.loader.hide()
            return

        if self.port.text() is None or self.port.text() == '':
            self.notification.showWarning(self, 'Error', GUILibraries.messages['invalid_port_given'])
            self.loader.hide()
            return

        if not GUILibraries.re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            self.notification.showWarning(self, 'Error', GUILibraries.messages['invalid_email_given'])
            self.loader.hide()
            return False

        information = {}
        information['pass'] = Pass
        information['port'] = port
        information['smtp'] = out_going_mail_server
        information['email'] = Email
        information['protocol'] = protocol


        text = 'Testing email access for Fixity reporting...'

        flag = self.email_notification.TestingEmail(Email,text, information)
        if flag:
            self.notification.showInformation(self, 'check credentials ',  GUILibraries.messages['got_testing_email'])
        else:
            try:
                self.notification.showError(self, 'Error',  GUILibraries.messages['testing_email_error'])
            except:
                pass



    def GetLayout(self):
        return self.email_pref_layout

    def Save(self):

        Email = self.email_addr_bar.text()
        Pass = self.password.text()
        out_going_mail_server = self.out_going_mail_server.text()
        port = self.port.text()
        if(self.SSL_protocol.isChecked()):
            protocol = 'SSL'
        elif(self.TLS_protocol.isChecked()):
            protocol = 'TLS'
        else:
            protocol = 'NONE'

        if self.out_going_mail_server.text() is None or self.out_going_mail_server.text() == '':
            self.notification.showWarning(self, 'Error', GUILibraries.messages['invalid_smtp_given'])
            return

        if self.port.text() is None or self.port.text() == '':
            self.notification.showWarning(self, 'Error', GUILibraries.messages['invalid_port_given'])
            return
        errorMsg = self.validateInformation(Email, Pass)

        if errorMsg is not True:
            self.notification.showError(self,'Error',  errorMsg)
            return
        information = {}
        information['smtp'] = out_going_mail_server
        information['email'] = Email
        information['pass'] = Pass
        information['port'] = port
        information['protocol'] = protocol
        information['debugger'] = 0
        information['createdAt'] = self.Fixity.Configuration.getCurrentTime()
        information['updatedAt'] = self.Fixity.Configuration.getCurrentTime()
        self.Fixity.Configuration.saveEmailConfiguration(information)
        self.notification.showInformation(self, "Fixity", GUILibraries.messages['email_save_success'])
        self.Cancel()
    def getConfigInfo(self):
        print('getConfigInfo')


    '''
    Close the Dialog Box
    '''
    def Cancel(self):
        self.parent_win.setWindowTitle("Fixity "+self.Fixity.Configuration.getApplicationVersion())
        self.destroy()
        self.close()

    # Launch Dialog
    def LaunchDialog(self):
        self.SetDesgin()
        self.ShowDialog()
