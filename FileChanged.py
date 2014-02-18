'''
Created on Feb 4, 2014
@version: 0.3
@author: Furqan Wasi
'''
# Fixity Scheduler
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0


import base64
from os import getcwd  , path
from PySide.QtCore import *
from PySide.QtGui import *
 

''' Class to manage all the the errors and warning loging'''
class FileChanged(QDialog):
    
    
    # Constuctor
    def __init__(self , orignalPathText ='', changePathText = '' ):
        self.FileChangedWin = QDialog()
        self.FileChangedWin.setWindowTitle('Change Directory Information')
        self.FileChangedWin.setWindowIcon(QIcon(path.join(getcwd(), 'images\\logo_sign_small.png')))
        self.FileChangedLayout = QVBoxLayout()
        self.version = '0.3'
        self.orignalPathText = orignalPathText
        self.changePathText = changePathText
        self.changeThePathInformation = False
        self.ReplacementArray ={} 
        
        
    # Distructor        
    def destroyFileChanged(self):
        del self
            
    def getVersion(self):
        return self.version
        
    def setVersion(self,version):
        return self.version
    
    def CreateWindow(self):
        self.FileChangedWin = QDialog()
        
    def GetWindow(self):
        return self.FileChangedWin 
             
    def ShowDialog(self):     
        self.FileChangedWin.show()
        self.FileChangedWin.exec_()
        
    def SetLayout(self, layout):
        self.FileChangedLayout = layout
        
    def GetLayout(self):
        return self.FileChangedLayout
        
    def SetWindowLayout(self):
        self.FileChangedWin.setLayout(self.FileChangedLayout)
        
    def CloseClick(self):
        self.changeThePathInformation = False
        
        self.FileChangedWin.close()
    
    def DestroyEveryThing(self):
        self.destroyFileChanged()
        self.FileChangedWin.close()        
    # All design Management Done in Here            
    def SetDesgin(self):
        
        
        
        self.GetLayout().addStrut(400)
        
        #initializing view elements
        self.orignalPathLable = QLabel()
        self.changePathToLable = QLabel()
        self.setInformation = QPushButton("&Orignal Path Information")
        self.setInformation = QPushButton("&Change Path")
        self.cancel = QPushButton("Close")
        self.orignalPath = QTextEdit()
        self.changePathTo = QTextEdit()
        
        
        #Set view text
        self.orignalPath.setText(self.orignalPathText)
        self.changePathTo.setText(self.changePathText)
        self.orignalPathLable.setText('Change Path From')
        self.changePathToLable.setText('To')
        self.orignalPath.setDisabled(True)
        self.changePathTo.setDisabled(True)
        
        #Styling
        self.orignalPath.setMaximumSize(400, 100)
        self.changePathTo.setMaximumSize(400, 100)
        self.cancel.setMaximumSize(200, 100)
        self.setInformation.setMaximumSize(200, 100)
        
        #set Widget to layouts
        self.GetLayout().addWidget(self.orignalPathLable)
        self.GetLayout().addWidget(self.orignalPath)
        self.GetLayout().addWidget(self.changePathToLable)
        self.GetLayout().addWidget(self.changePathTo)
        self.GetLayout().addWidget(self.setInformation)
        self.GetLayout().addWidget(self.cancel)
        
        #set triggers
        self.setInformation.clicked.connect(self.changeRootDirInfo)
        self.cancel.clicked.connect(self.CloseClick)
        self.SetWindowLayout()
    #Points out to change the Path of Manifest or not
    def changeRootDirInfo(self):
        if not path.exists(self.changePathText):
            msgBox = QMessageBox();
            msgBox.setText("New Directory Dose not exsit's , could not change path from "+self.orignalPathText+" To " + self.changePathText+'.please give correct path and try again')
            msgBox.exec_()
            self.changeThePathInformation = False
        else:
            if (self.orignalPathText != None and self.changePathText != None) and (self.orignalPathText != '' and self.changePathText != ''):
                self.changeThePathInformation = True
            else:
                self.changeThePathInformation = False
        self.FileChangedWin.close()
            
# Main Code
# app = QApplication('asdas')
# w = FileChanged('asdadasdasads','asdsdasdads')
# w.CreateWindow()
# w.SetWindowLayout()
# w.SetDesgin()
# w.ShowDialog()    
# app.exec_() 
