'''
Created on Dec 1, 2013

@author: Furqan
'''
from PySide.QtCore import *
from PySide.QtGui import *
import base64
from os import getcwd ,path
import sys

class EmailPref(QDialog):
    '''
    This class i created to handle all Email configurations
    '''


    #Constructor
    def __init__(self):
        QDialog.__init__(self)
        self.EmailPrefWin = QDialog()
        self.setWindowIcon(QIcon(path.join(getcwd(), 'images\\logo_sign_small.png')))
        self.EmailPrefLayout = QVBoxLayout()
    def destroyEmailPref(self):
        del self    
    def CreateWindow(self):
        self.EmailPrefWin = QDialog()
        
    def GetWindow(self):
        return self.EmailPrefWin 
             
    def ShowDialog(self):     
        self.EmailPrefWin.show()
        self.EmailPrefWin.exec_()
        
    def SetLayout(self,layout):
        self.EmailPrefLayout = layout
        
    def SetWindowLayout(self):
        self.EmailPrefWin.setLayout(self.EmailPrefLayout)
        
    def GetLayout(self):
        return self.EmailPrefLayout
                
    def SetDesgin(self):
        self.GetLayout().addStrut(500)
        
        self.EmailAddrBar = QLineEdit("Email")
        self.Password = QLineEdit("Password")
        self.setInformation = QPushButton("Set Information")
        self.reset = QPushButton("Reset")
        self.cancel = QPushButton("Close")
        
        self.reset.setMaximumSize(100,100)
        self.cancel.setMaximumSize(100,100)
        self.setInformation.setMaximumSize(100,100)
        self.cancel.move(400,400)
        
    
        
        self.GetLayout().addWidget(self.EmailAddrBar)
        self.GetLayout().addWidget(self.Password)
        self.GetLayout().addWidget(self.setInformation)
        self.GetLayout().addWidget(self.reset)
        self.GetLayout().addWidget(self.cancel)
        
        #self.EmailAddrBar.textChanged.connect(self.EmailAddrBarClick)
        #self.EmailAddrBar.returnPressed.connect(self.EmailAddrBarClick)
        self.reset.clicked.connect(self.ResetForm)
        self.setInformation.clicked.connect(self.SetInformation)
        self.cancel.clicked.connect(self.CloseClick)
        self.SetWindowLayout()
        
    def ResetForm(self):
        self.EmailAddrBar.setText('Email')
        self.Password.setText('Password')
    #Fetch information related to email configuration    
    def getConfigInfo(self):
         
        fCheck = open(getcwd()+'\\bin\conf.txt', 'rb') 
        Text = fCheck.readlines()
        fCheck.close()
        
        information = {} 
        information['email'] = ''
        information['pass'] = ''
        information['onlyonchange'] = ''
        if len(Text) >0 :
            for SingleValue in Text:
                decodedString = self.DecodeInfo(SingleValue)
                if decodedString.find('e|') >= 0:
                    information['email'] = decodedString
                elif decodedString.find('p|') >= 0: 
                    information['pass'] = decodedString
                else:    
                    information['onlyonchange'] = decodedString
       
        return information
    #update/save information related to email configuration 
    def setConfigInfo(self,information):
        f = open(getcwd()+'\\bin\conf.txt', 'wb')
        flag = False
        for key ,Sngleitem in information.iteritems():
            if Sngleitem !='':
                f.write(self.EncodeInfo(Sngleitem) +'\n')
                flag = True
        f.close()
        return flag   
     
    def SetInformation(self):
        Email = self.EmailAddrBar.text()
        Pass = self.Password.text()
        if Email =='' or Email =='Email' or Pass =='' or Pass =='Password':
            QMessageBox.information(self, "Invalid", "Invalid information provided, please try again! ")
            return
        E_unbased = "e|"+Email
        P_unbased = "p|"+Pass
        
        information = self.getConfigInfo()
        
        information['email'] = E_unbased
        information['pass'] = P_unbased
        
        self.setConfigInfo(information)
        QMessageBox.information(self, "Success", "Information Successfully Saved! ")
        
        self.CloseClick()
        
    def PasswordClick(self):
        if self.Password.text() == 'Password':
            self.Password.setText('')
    def EncodeInfo(self,stringToBeEncoded):
        stringToBeEncoded=str(stringToBeEncoded).strip()
        return base64.b16encode(base64.b16encode(stringToBeEncoded))
    
    def DecodeInfo(self,stringToBeDecoded):
        stringToBeDecoded=str(stringToBeDecoded).strip()
        return base64.b16decode(base64.b16decode(stringToBeDecoded))
    
    def CloseClick(self):
        self.destroyEmailPref()
        self.EmailPrefWin.close()
        
                        
    def EmailAddrBarClick(self):
        
        if self.EmailAddrBar.text() == 'Email':
            self.EmailAddrBar.setText('')

# app = QApplication('asdas')
# w = EmailPref()
# w.CreateWindow()
# w.SetWindowLayout()
# w.SetDesgin()
# w.ShowDialog()
#     
# app.exec_()        

