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
        Email = self.EmailAddrBar.text()
        Pass = self.Password.text()
    
        if not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            msgBox = QMessageBox();
            msgBox.setText("Invalid Email Address")
            msgBox.exec_()
            self.loader.hide()
            return False
        text = 'Testing email credentials for Fixity'
        flag = self.FM.send(Email, text, None, Email, Pass)
        if flag:
            msgBox = QMessageBox();
            msgBox.setText("Please Check , if you recieve email from your email address then provided credentails are correct ")
            msgBox.exec_()
            
        self.loader.hide()
        return flag
        
    def GetLayout(self):
        return self.EmailPrefLayout

    # All design Management Done in Here            
    def SetDesgin(self):
        self.GetLayout().addStrut(200)
        
        self.EmailAddrBar = QLineEdit()
        self.Password = QLineEdit()
        self.Project = QLineEdit()
        self.Password.setEchoMode(QLineEdit.Password)
        self.setInformation = QPushButton("Set Information")
        self.reset = QPushButton("Reset")
        self.checkEmail = QPushButton("Check Credentials")
        self.cancel = QPushButton("Close")
        self.loader = QLabel("Sending Email ....")
        
        self.EmailAddrBar.setPlaceholderText("Email")
        self.Password.setPlaceholderText("Password")
        self.Project.setPlaceholderText("For the Project")
        
        self.EmailAddrBar.setMaximumSize(200, 100)
        self.Password.setMaximumSize(200, 100)
        self.reset.setMaximumSize(200, 100)
        self.cancel.setMaximumSize(200, 100)
        self.setInformation.setMaximumSize(200, 100)
        self.checkEmail.setMaximumSize(200, 100)
        self.Project.setMaximumSize(200, 100)
        
        information = self.getConfigInfo()
        
        self.GetLayout().addWidget(self.loader)
        self.GetLayout().addWidget(self.EmailAddrBar)
        self.GetLayout().addWidget(self.Password)
        self.GetLayout().addWidget(self.setInformation)
        self.GetLayout().addWidget(self.checkEmail)
        self.GetLayout().addWidget(self.reset)
        self.GetLayout().addWidget(self.cancel)
        self.loader.hide()
        
        self.reset.clicked.connect(self.ResetForm)
        self.setInformation.clicked.connect(self.SetInformation)
        self.cancel.clicked.connect(self.CloseClick)
        self.checkEmail.clicked.connect(self.checkIsEmailValid)

        
        self.SetWindowLayout()
        EmailAddr = str(information['email']).replace('e|', '').replace('\n', '')
        Pass = str(information['pass']).replace('p|', '').replace('\n', '')
        self.EmailAddrBar.setText(EmailAddr)
        self.Password.setText(Pass)
        
        
        
    # Reset Form information    
    def ResetForm(self):
        self.EmailAddrBar.setText('Email')
        self.Password.setText('Password')
        self.Project.setText('For the Project')
        
        
    # Fetch information related to email configuration    
    def getConfigInfo(self, project=None):
        if project == None:
            information = {} 
            information['email'] = ''
            information['pass'] = ''
            information['onlyonchange'] = ''
            if path.isfile(getcwd() + '\\bin\\conf.txt'): 
                fCheck = open(getcwd() + '\\bin\\conf.txt', 'rb') 
                Text = fCheck.readlines()
                fCheck.close()
                if len(Text) > 0 :
                    for SingleValue in Text:
                        decodedString = self.DecodeInfo(SingleValue)
                        if decodedString.find('e|') >= 0:
                            information['email'] = decodedString
                        elif decodedString.find('p|') >= 0: 
                            information['pass'] = decodedString
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
            msg = "Invalid Invalid Email Address provided, please try again! "
            return msg
    # Validation Configuration provided
    def validateInformation(self, Email, Pass , Project):
        msg = None
        if Pass == '':
            msg = "Invalid information provided, please try again! "
            return msg
        if not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            msg = "Invalid Invalid Email Address provided, please try again! "
            return msg
        
        
        
    # Updating Configuration     
    def SetInformation(self):
        Email = self.EmailAddrBar.text()
        Pass = self.Password.text()
        Project = self.Project.text()
        errorMsg = self.validateInformation(Email, Pass, Project)
        if not str(errorMsg).strip() == 'None':
            QB = QMessageBox()
            errorMsg = QB.information(self, "Error", errorMsg)
            return
        
        E_unbased = "e|" + Email
        P_unbased = "p|" + Pass
        
        information = self.getConfigInfo()
        
        information['email'] = E_unbased
        information['pass'] = P_unbased
        
        self.setConfigInfo(information)
        QMessageBox.information(self, "Success", "Information Successfully Saved! ")
        
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
# Main Code
# app = QApplication('asdas')
# w = EmailPref()
# w.CreateWindow()
# w.SetWindowLayout()
# w.SetDesgin()
# w.ShowDialog()    
# app.exec_()        

