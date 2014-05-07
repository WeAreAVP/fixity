# -- coding: utf-8 --
# Email Preferences
# Version 0.4, Apr 1, 2014
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

'''
Created on Dec 1, 2013
@version: 0.4
@author: Furqan Wasi <furqan@geekschicago.com>
'''

# Built in Library
from PySide.QtCore import *
from PySide.QtGui import *
import base64
from os import getcwd , path
import os
import re
# Custom Library
import FixityMail
from Database import Database

'''This class is created to handle all Email configurations and management'''
class EmailPref(QDialog):
    '''
    Constructor
    '''
    def __init__(self,parentWin):        
        QDialog.__init__(self,parentWin)
        
        if parentWin:
            self.parentWin = parentWin
            self.setWindowModality(Qt.WindowModal)
            self.parentWin.setWindowTitle('Configure Sender Email')            
        else:            
            self = QDialog()
        
        
        self.setWindowIcon(QIcon(path.join(getcwd(), 'images'+str(os.sep)+'logo_sign_small.png')))
        self.EmailPrefLayout = QVBoxLayout()
        
        self.FixityMailSender = FixityMail
        self.version = '0.4'
        
    def reject(self):
        try:
            self.parentWin.setWindowTitle("Fixity "+self.parentWin.versoin)
        except:
            pass
        try:
            super(EmailPref,self).reject()
        except:
            pass
        
    '''
    Distructor
    '''
    def destroyEmailPref(self):
        del self
        
    '''
    Get Version
    
    @return: string
    '''   
    def getVersion(self):
        try:
            return self.version
        except:
            pass
    '''
    Set Version 
    @param version: current version of fixity 
    @return: string
    '''
        
    def setVersion(self,version):
        try:
            return self.version
        except:
            pass
    '''
    Create Window
    @return: None
    '''
        
    def CreateWindow(self):
        try:
            if self.parentWin:
                self = QDialog(self.parentWin)
        except:    
            self = QDialog()
        
    '''
    Get Window info
    
    @return: None
    '''
    def GetWindow(self):
        return self
    '''
    Show Dialog
    
    @return: None
    '''
    def ShowDialog(self):
        self.show()
        self.exec_()
    '''
    Set Layout
    
    @return: None
    '''
    def SetLayout(self, layout):
        self.EmailPrefLayout = layout
    '''
    Set layout for windows
    
    @return: None
    '''
    def SetWindowLayout(self):
        self.setLayout(self.EmailPrefLayout)


     
    ''' 
    Check is Email address and Password is valid by sending email on its own inbox
    
    @return: None
    '''
    def checkIsEmailValid(self):
        self.loader.show()
        QCoreApplication.processEvents()
        Email = self.EmailAddrBar.text()
        Pass = self.Password.text()
        port = self.port.text()

        outgoingMailServer = self.outgoingMailServer.text()
        if(self.SSLProtocol.isChecked()):
            protocol = 'SSL'
        elif(self.TLSProtocol.isChecked()):
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
        flag = self.FixityMailSender.send(Email, text, None,information,'',self)
        if flag:
            msgBox = QMessageBox();
            msgBox.setText("Please check the provided email account's inbox.\nIf there is a message from Fixity, then reporting is enabled.")
            msgBox.exec_()
        else:
            try:
                msgBox = QMessageBox();
                msgBox.setText("Fixity was unable to send email.\n*Please ensure that you are connected to the Internet\n*Please ensure that your email credentials are correct")
                msgBox.exec_()            
            except:
                pass
            


        self.loader.hide()
        return flag

    def GetLayout(self):
        return self.EmailPrefLayout

     
    ''' 
    All design Management Done in Here
    
    @return: None
    '''
    def SetDesgin(self):
        self.GetLayout().addStrut(200)

        self.EmailAddrBar = QLineEdit()
        self.outgoingMailServer = QLineEdit()
        self.port = QLineEdit()
        self.Password = QLineEdit()
        self.SSLProtocol = QRadioButton("SSL Protocols")
        self.TLSProtocol = QRadioButton("TLS Protocols")
        self.noneProtocol = QRadioButton("None")

        self.Password.setEchoMode(QLineEdit.Password)
        self.setInformation = QPushButton("Save && Close")
        self.reset = QPushButton("Reset")
        self.checkEmail = QPushButton("Check Credentials")
        self.cancel = QPushButton("Close Without Saving")
        self.loader = QLabel("Sending Email...")

        self.EmailAddrBar.setPlaceholderText("email: user@domain.com")
        self.Password.setPlaceholderText("Password")
        self.outgoingMailServer.setPlaceholderText("smtp.gmail.com")
        self.port.setPlaceholderText("Port")

        self.EmailAddrBar.setMaximumSize(200, 100)
        self.Password.setMaximumSize(200, 100)
        self.reset.setMaximumSize(200, 100)
        self.cancel.setMaximumSize(200, 100)
        self.setInformation.setMaximumSize(200, 100)
        self.outgoingMailServer.setMaximumSize(200, 100)
        self.port.setMaximumSize(200, 100)
        self.checkEmail.setMaximumSize(200, 100)
        
        self.SMTPServerLable = QLabel('SMTP Server')
        self.EmailAddressLable = QLabel('Email Address')
        self.PasswordLable = QLabel('Password')
        self.PortLable = QLabel('Port')
        self.EncryptionLable = QLabel('Encryption Method')
        
        self.GetLayout().addWidget(self.loader)
        self.GetLayout().addWidget(self.SMTPServerLable)
        self.GetLayout().addWidget(self.outgoingMailServer)
        
        self.GetLayout().addWidget(self.EmailAddressLable)
        self.GetLayout().addWidget(self.EmailAddrBar)
        
        self.GetLayout().addWidget(self.PasswordLable)
        self.GetLayout().addWidget(self.Password)
        
        self.GetLayout().addWidget(self.PortLable)
        self.GetLayout().addWidget(self.port)
        
        self.GetLayout().addWidget(self.EncryptionLable)
        self.GetLayout().addWidget(self.SSLProtocol)
        self.GetLayout().addWidget(self.TLSProtocol)
        self.GetLayout().addWidget(self.noneProtocol)
        self.GetLayout().addWidget(self.setInformation)
        self.GetLayout().addWidget(self.checkEmail)
        self.GetLayout().addWidget(self.reset)
        self.GetLayout().addWidget(self.cancel)

        self.loader.hide()

        self.reset.clicked.connect(self.ResetForm)
        self.setInformation.clicked.connect(self.SetInformation)
        self.cancel.clicked.connect(self.CloseClick)
        self.checkEmail.clicked.connect(self.checkIsEmailValid)
        self.SSLProtocol.clicked.connect(self.SSLProtocolConif)
        self.TLSProtocol.clicked.connect(self.TLSProtocolConif)
        self.noneProtocol.clicked.connect(self.noneProtocolConif)


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
        if(smtp is not None and smtp !='' ):
            self.outgoingMailServer.setText(smtp)
        else:
            self.outgoingMailServer.setText('smtp.gmail.com')

        if protocol == 'SSL':
            self.SSLProtocol.setChecked(True)
            self.TLSProtocol.setChecked(False)
            self.noneProtocol.setChecked(False)

            if(port is not None and port !='' ):
                self.port.setText(port)
            else:
                self.port.setText('465')

        elif protocol == 'TLS':
            self.TLSProtocol.setChecked(True)
            self.SSLProtocol.setChecked(False)
            self.noneProtocol.setChecked(False)
            if(port is not None and port !='' ):
                self.port.setText(port)
            else:
                self.port.setText('587')
        else:
            self.noneProtocol.setChecked(True)
            self.TLSProtocol.setChecked(False)
            self.SSLProtocol.setChecked(False)
            if(port is not None and port !='' ):
                self.port.setText(port)
            else:
                self.port.setText('25')

    
    ''' 
    Function to Reset Form information
    @return: None
    '''
    def ResetForm(self):
        self.EmailAddrBar.setText('')
        self.Password.setText('')
        self.outgoingMailServer.setText('')
        self.port.setText('')
        
    
    ''' 
    Function to reopen Email Pref Dialog Box
    
    @return: None
    ''' 
    def ReOpenEmailPref(self):
        self.CloseClick()
        
        self.setWindowTitle('Configure Sender Email')
        self.setWindowIcon(QIcon(path.join(getcwd(), 'images'+str(os.sep)+'logo_sign_small.png')))
        self.EmailPrefLayout = QVBoxLayout()
        self.FixityMailSender = FixityMail
        self.version = '0.4'
        self.CreateWindow()
        self.SetWindowLayout()
        self.SetDesgin()
        self.ShowDialog()
        self.show()
        
    
    ''' 
    Fetch information related to email configuration
    @param project: Project Name (Optional) 
    
    @return: Tuple Project Information in found else empty Truple
    ''' 
    def getConfigInfo(self, project=None):
        self.SqlLiteDataBase = Database()


        queryResult = self.SqlLiteDataBase.select(self.SqlLiteDataBase._tableConfiguration)

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
    
    
    ''' 
    Validate given email address
    @param Email: Email Address
   
    @return: String Message of failure
    ''' 
    def ValidateEmail(self, Email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            msgEmailValidation = "Invalid email address provided.  Please provide a valid address and try again."
            return msgEmailValidation
    
    ''' 
    Validation Configuration provided
    @param Email: Email Address
    @param Pass: Password to check
    
    @return: String Message of success or failure
    ''' 
    def validateInformation(self, Email, Pass):
        msgEmailValidation = None
        if Pass == '':
            msgEmailValidation = "Please provide a password to access the reporting email account."
            return msgEmailValidation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            msgEmailValidation = "Invalid email address provided.  Please provide a valid address and try again"
            return msgEmailValidation

     

    ''' 
    Updating Configuration
    
    @return: None  
    ''' 
    def SetInformation(self):
        self.SqlLiteDataBase = Database()
       
        
        Email = self.EmailAddrBar.text()
        Pass = self.Password.text()
        outgoingMailServer = self.outgoingMailServer.text()
        port = self.port.text()

        if(self.SSLProtocol.isChecked()):
            protocol = 'SSL'
        elif(self.TLSProtocol.isChecked()):
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

        self.SqlLiteDataBase.delete(self.SqlLiteDataBase._tableConfiguration, '1=1')
        self.SqlLiteDataBase.insert(self.SqlLiteDataBase._tableConfiguration, information)
        
        QMessageBox.information(self, "Fixity", "Credentials successfully saved!")
        
        self.CloseClick()

     
    ''' 
    Encoding Given String to base 64
    @param stringToBeEncoded string To BeEncoded.
    
    @return: string  
    ''' 
    def EncodeInfo(self, stringToBeEncoded):
        stringToBeEncoded = str(stringToBeEncoded).strip()
        return base64.b16encode(base64.b16encode(stringToBeEncoded))

    
    ''' 
    Decode Information of path
    @param stringToBeDecoded string To Be Decoded.
    
    @return: string  
    ''' 
    def DecodeInfo(self, stringToBeDecoded):
        stringToBeDecoded = str(stringToBeDecoded).strip()
        return base64.b16decode(base64.b16decode(stringToBeDecoded))

    
    ''' 
    Manage click on close
    
    @return: None  
    ''' 
    def CloseClick(self):
        try:
            self.parentWin.setWindowTitle("Fixity "+self.parentWin.versoin)
        except:
            pass
        self.destroyEmailPref()
        self.close()

    
    ''' 
    TSL configuration manager
    
    @return: None  
    ''' 
    def TLSProtocolConif(self):
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
    def SSLProtocolConif(self):
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

    #
    ''' 
    No Encryption Manager
    
    @return: None  
    ''' 
    def noneProtocolConif(self):
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
            
# app = QApplication('asdas')
# w = EmailPref(QDialog())
# w.SetWindowLayout()
# w.SetDesgin()
# w.ShowDialog()            
# app.exec_()