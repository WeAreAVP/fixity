'''
Created on Dec 1, 2013
@version: 0.3
@author: Furqan Wasi
'''
# Fixity Scheduler
# Version 0.3, Dec 1, 2013
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
#Built in Library
from PySide.QtCore import *
from PySide.QtGui import *
import base64
from os import getcwd , path
import re
# Custom Library
import FixityMail
from Database import Database

class EmailPref(QDialog):
    '''This class is created to handle all Email configurations and management'''
    # Constructor
    def __init__(self):
        QDialog.__init__(self)
        self.EmailPrefWin = QDialog()
        self.EmailPrefWin.setWindowTitle('Configure Sender Email')
        self.EmailPrefWin.setWindowIcon(QIcon(path.join(getcwd(), 'images\\logo_sign_small.png')))
        self.EmailPrefLayout = QVBoxLayout()
        self.FM = FixityMail
        self.version = '0.3'


    # Distructor
    def destroyEmailPref(self):
        del self

    def getVersion(self):
        return self.version

    def setVersion(self,version):
        return self.version

    def CreateWindow(self):
        self.EmailPrefWin = QDialog()

    def GetWindow(self):
        return self.EmailPrefWin

    def ShowDialog(self):
        self.EmailPrefWin.show()
        self.EmailPrefWin.exec_()

    def SetLayout(self, layout):
        self.EmailPrefLayout = layout

    def SetWindowLayout(self):
        self.EmailPrefWin.setLayout(self.EmailPrefLayout)


    # Check is Email address and Password is valid by sending email on its own inbox
    def checkIsEmailValid(self):
        self.loader.show()
        QCoreApplication.processEvents()
        Email = self.EmailAddrBar.text()
        Pass = self.Password.text()
        port = self.port.text()

        outgoingMailServer = self.outgoingMailServer.text()
        if(self.SSL.isChecked()):
            protocol = 'SSL'
        elif(self.TLS.isChecked()):
            protocol = 'TLS'
        else:
            protocol = 'NONE'
        information = {}

        information['email'] = Email
        information['pass'] = Pass
        information['port'] = port
        information['smtp'] = outgoingMailServer
        information['protocol'] = protocol



        if not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            msgBox = QMessageBox();
            msgBox.setText("Invalid email address provided.\nPlease provide a valid address and try again.")
            msgBox.exec_()
            self.loader.hide()
            return False
        text = 'Testing email access for Fixity reporting...'
        flag = self.FM.send(Email, text, None,information)
        if flag:
            msgBox = QMessageBox();
            msgBox.setText("Please check the provided email account's inbox.\nIf there is a message from Fixity, then reporting is enabled.")
            msgBox.exec_()

        self.loader.hide()
        return flag

    def GetLayout(self):
        return self.EmailPrefLayout

    # All design Management Done in Here
    def SetDesgin(self):
        self.GetLayout().addStrut(200)

        self.EmailAddrBar = QLineEdit()
        self.outgoingMailServer = QLineEdit()
        self.port = QLineEdit()
        self.Password = QLineEdit()
        self.SSL = QRadioButton("SSL Protocols")
        self.TLS = QRadioButton("TLS Protocols")
        self.none = QRadioButton("None")

        self.Password.setEchoMode(QLineEdit.Password)
        self.setInformation = QPushButton("Set Information")
        self.reset = QPushButton("Reset")
        self.checkEmail = QPushButton("Check Credentials")
        self.cancel = QPushButton("Close")
        self.loader = QLabel("Sending Email...")

        self.EmailAddrBar.setPlaceholderText("Email")
        self.Password.setPlaceholderText("Password")
        self.outgoingMailServer.setPlaceholderText("outgoing mail server")
        self.port.setPlaceholderText("Port ")

        self.EmailAddrBar.setMaximumSize(200, 100)
        self.Password.setMaximumSize(200, 100)
        self.reset.setMaximumSize(200, 100)
        self.cancel.setMaximumSize(200, 100)
        self.setInformation.setMaximumSize(200, 100)
        self.outgoingMailServer.setMaximumSize(200, 100)
        self.port.setMaximumSize(200, 100)
        self.checkEmail.setMaximumSize(200, 100)

        self.GetLayout().addWidget(self.loader)
        self.GetLayout().addWidget(self.outgoingMailServer)
        self.GetLayout().addWidget(self.EmailAddrBar)
        self.GetLayout().addWidget(self.Password)
        self.GetLayout().addWidget(self.port)
        self.GetLayout().addWidget(self.SSL)
        self.GetLayout().addWidget(self.TLS)
        self.GetLayout().addWidget(self.none)
        self.GetLayout().addWidget(self.setInformation)
        self.GetLayout().addWidget(self.checkEmail)
        self.GetLayout().addWidget(self.reset)
        self.GetLayout().addWidget(self.cancel)

        self.loader.hide()

        self.reset.clicked.connect(self.ResetForm)
        self.setInformation.clicked.connect(self.SetInformation)
        self.cancel.clicked.connect(self.CloseClick)
        self.checkEmail.clicked.connect(self.checkIsEmailValid)
        self.SSL.clicked.connect(self.SSLConif)
        self.TLS.clicked.connect(self.TLSConif)
        self.none.clicked.connect(self.NoneConif)


        self.SetWindowLayout()
        information = self.getConfigInfo()
        EmailAddr = ''
        Pass = ''
        port = ''
        smtp = ''
        protocol = ''

        if(len(information)> 0):
            EmailAddr = information['email']
            Pass = str(information['pass'])
            port = str(information['port'])
            smtp = str(information['smtp'])
            protocol = str(information['protocol'])

        self.EmailAddrBar.setText(EmailAddr)
        self.Password.setText(Pass)
        if(smtp != None and smtp !='' ):
            self.outgoingMailServer.setText(smtp)
        else:
            self.outgoingMailServer.setText('smtp.gmail.com')

        if protocol == 'SSL':
            self.SSL.setChecked(True)
            self.TLS.setChecked(False)
            self.none.setChecked(False)

            if(port != None and port !='' ):
                self.port.setText(port)
            else:
                self.port.setText('465')

        elif protocol == 'TLS':
            self.TLS.setChecked(True)
            self.SSL.setChecked(False)
            self.none.setChecked(False)
            if(port != None and port !='' ):
                self.port.setText(port)
            else:
                self.port.setText('587')
        else:
            self.none.setChecked(True)
            self.TLS.setChecked(False)
            self.SSL.setChecked(False)
            if(port != None and port !='' ):
                self.port.setText(port)
            else:
                self.port.setText('587')

    # Reset Form information
    def ResetForm(self):
        self.EmailAddrBar.setText('')
        self.Password.setText('')
        self.outgoingMailServer.setText('')
        self.port.setText('')




          # Fetch information related to email configuration
    def getConfigInfo(self, project=None):
        self.Database = Database()


        queryResult = self.Database.select(self.Database._tableConfiguration)

        try:
            if len(queryResult)>0 :
                information = {}
                for  result in queryResult:
                    information['id'] = queryResult[result]['id']
                    information['smtp'] = self.DecodeInfo(queryResult[result]['smtp'])
                    information['email'] = self.DecodeInfo(queryResult[result]['email'])
                    information['pass'] = self.DecodeInfo(queryResult[result]['pass'])
                    information['port'] = queryResult[result]['port']
                    information['protocol'] = queryResult[result]['protocol']
                    information['debugger'] = queryResult[result]['debugger']
                    break;
                return information
        except:
            pass
        return {}

    def ValidateEmail(self, Email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            msg = "Invalid email address provided.  Please provide a valid address and try again."
            return msg

    # Validation Configuration provided
    def validateInformation(self, Email, Pass):
        msg = None
        if Pass == '':
            msg = "Please provide a password to access the reporting email account."
            return msg
        if not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            msg = "Invalid email address provided.  Please provide a valid address and try again"
            return msg



    # Updating Configuration
    def SetInformation(self):
        self.Database = Database()

        Email = self.EmailAddrBar.text()
        Pass = self.Password.text()
        outgoingMailServer = self.outgoingMailServer.text()
        port = self.port.text()

        if(self.SSL.isChecked()):
            protocol = 'SSL'
        elif(self.TLS.isChecked()):
            protocol = 'TLS'
        else:
            protocol = 'NONE'

        errorMsg = self.validateInformation(Email, Pass)
        if not str(errorMsg).strip() == 'None':
            QB = QMessageBox()
            errorMsg = QB.information(self, "Error", errorMsg)
            return

        E_unbased = Email
        P_unbased = Pass
        smtp_unbased = outgoingMailServer
        port_unbased = port
        protocol_unbased = protocol

        information = self.getConfigInfo()

        information['email'] = self.EncodeInfo(E_unbased)
        information['pass'] = self.EncodeInfo(P_unbased)
        information['port'] = port_unbased
        information['smtp'] = self.EncodeInfo(smtp_unbased)
        information['protocol'] = protocol_unbased

        self.Database.delete(self.Database._tableConfiguration, '1=1')
        self.Database.insert(self.Database._tableConfiguration, information)

        QMessageBox.information(self, "Fixity", "Credentials successfully saved!")

        self.CloseClick()


    # Triggers
    def EncodeInfo(self, stringToBeEncoded):
        stringToBeEncoded = str(stringToBeEncoded).strip()
        return base64.b16encode(base64.b16encode(stringToBeEncoded))

    def DecodeInfo(self, stringToBeDecoded):
        stringToBeDecoded = str(stringToBeDecoded).strip()
        return base64.b16decode(base64.b16decode(stringToBeDecoded))

    def CloseClick(self):
        self.destroyEmailPref()
        self.EmailPrefWin.close()

    def TLSConif(self):
        information = self.getConfigInfo()
        try:
            port = str(information['port'])
        except:
            port = ''
            pass

        if(port != None and port !='' ):
            self.port.setText(port)
        else:
            self.port.setText('587')

    def SSLConif(self):
        information = self.getConfigInfo()
        try:
            port = str(information['port'])
        except:
            port = ''
            pass

        if(port != None and port !='' ):
            self.port.setText(port)
        else:
            self.port.setText('465')

    def NoneConif(self):
        information = self.getConfigInfo()
        try:
            port = str(information['port'])
        except:
            port = ''
            pass

        if(port != None and port !='' ):
            self.port.setText(port)
        else:
            self.port.setText('587')
# Main Code
app = QApplication('asdas')
w = EmailPref()
w.CreateWindow()
w.SetWindowLayout()
w.SetDesgin()
w.ShowDialog()
app.exec_()

