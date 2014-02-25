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

from PySide.QtCore import *
from PySide.QtGui import *
import base64
from os import getcwd , path
import FixityMail
import re


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
        information['outgoingMailServer'] = outgoingMailServer
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
        
        EmailAddr = str(information['email']).replace('e|', '').replace('\n', '')
        Pass = str(information['pass']).replace('p|', '').replace('\n', '')
        port = str(information['port']).replace('port|', '').replace('\n', '')
        smtp = str(information['outgoingMailServer']).replace('smtp|', '').replace('\n', '')
        protocol = str(information['protocol']).replace('protocol|', '').replace('\n', '')
        
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
        self.EmailAddrBar.setText('Email')
        self.Password.setText('Password')
        
        
        
    # Fetch information related to email configuration    
    def getConfigInfo(self, project=None):
        if project == None:
            information = {} 
            information['email'] = ''
            information['pass'] = ''
            information['onlyonchange'] = ''
            information['debugging'] = ''
            information['protocol'] = ''
            information['outgoingMailServer'] = ''
            information['port'] = ''
            
            
            if path.isfile(getcwd() + '\\bin\\conf.txt'): 
                fCheck = open(getcwd() + '\\bin\\conf.txt', 'rb') 
                Text = fCheck.readlines()
                fCheck.close()
                if len(Text) > 0 :
                    for SingleValue in Text:
                        decodedString = self.DecodeInfo(SingleValue)
                        if decodedString.find('smtp|') >= 0:
                            information['outgoingMailServer'] = decodedString
                        elif decodedString.find('e|') >= 0:
                            information['email'] = decodedString
                        elif decodedString.find('p|') >= 0: 
                            information['pass'] = decodedString
                        elif decodedString.find('port|') >= 0: 
                            information['port'] = decodedString
                        elif decodedString.find('protocol|') >= 0: 
                            information['protocol'] = decodedString
                        elif decodedString.find('debug|') >= 0: 
                            information['debugging'] = decodedString
                        
                        else:    
                            information['onlyonchange'] = decodedString
            return information
        else:    
            information = {} 
            information['onlyonchange'] = ''
            information['filters'] = ''
            information['RunWhenOnBatteryPower'] = ''
            information['IfMissedRunUponAvailable'] = ''
            information['RunInitialScan'] = ''
            information['filters'] = ''
            information['Algorithm'] = ''
            if path.isfile(getcwd() + '\\bin\\' + project + '-conf.txt'): 
                fCheck = open(getcwd() + '\\bin\\' + project + '-conf.txt', 'rb') 
                Text = fCheck.readlines()
                fCheck.close()
                
                if len(Text) > 0 :
                    for SingleValue in Text:
                        decodedString = self.DecodeInfo(SingleValue)
                        if decodedString.find('EOWSC|') >= 0:
                            information['onlyonchange'] = decodedString
                        elif decodedString.find('fil|') >= 0:
                            information['filters'] = decodedString
                        elif decodedString.find('RWOBP|') >= 0:
                            information['RunWhenOnBatteryPower'] = decodedString  
                        elif decodedString.find('IMRUA|') >= 0:
                            information['IfMissedRunUponAvailable'] = decodedString
                        elif decodedString.find('RIS|') >= 0:
                            information['RunInitialScan'] = decodedString
                        elif decodedString.find('algo|') >= 0:  
                            information['Algorithm'] = decodedString
                        
                                              
        return information
    
    # Update/Save Information Related To Email Configuration 
    def setConfigInfo(self, information , project=None):
        
        flag = False
        if project == None:  
            f = open(getcwd() + '\\bin\\conf.txt', 'wb')
        else:
            f = open(getcwd() + '\\bin\\' + project + '-conf.txt', 'wb')
            
        for key , Sngleitem in information.iteritems():
            if Sngleitem != '':
                f.write(self.EncodeInfo(Sngleitem) + '\n')
                flag = True
        f.close()      
        return flag   
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
        
        E_unbased = "e|" + Email
        P_unbased = "p|" + Pass
        smtp_unbased = "smtp|" + outgoingMailServer
        port_unbased = "port|" + port
        protocol_unbased = "protocol|" + protocol
        
        information = self.getConfigInfo()
        
        information['email'] = E_unbased
        information['pass'] = P_unbased
        information['port'] = port_unbased
        information['smtp'] = smtp_unbased
        information['protocol'] = protocol_unbased
        
        
        self.setConfigInfo(information)
        
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
        port = str(information['port']).replace('port|', '').replace('\n', '')
        
        if(port != None and port !='' ):
            self.port.setText(port)
        else:
            self.port.setText('587')
            
    def SSLConif(self):
        information = self.getConfigInfo()
        port = str(information['port']).replace('port|', '').replace('\n', '')
        
        if(port != None and port !='' ):
            self.port.setText(port)
        else:
            self.port.setText('465')
            
    def NoneConif(self):
        information = self.getConfigInfo()
        port = str(information['port']).replace('port|', '').replace('\n', '')
        
        if(port != None and port !='' ):
            self.port.setText(port)
        else:
            self.port.setText('587')
# Main Code
# app = QApplication('asdas')
# w = EmailPref()
# w.CreateWindow()
# w.SetWindowLayout()
# w.SetDesgin()
# w.ShowDialog()    
# app.exec_()        

