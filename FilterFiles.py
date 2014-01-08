'''
Created on Dec 5, 2013
@version: 0.3
@author: Furqan Wasi
'''
# Fixity Scheduler
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
from PySide.QtCore import *
from PySide.QtGui import *
from os import getcwd , path, listdir, remove, walk
import sys
from EmailPref import EmailPref
class FilterFiles(QDialog):
    ''' Class to manage the Filter to be implemented for the files with specific extensions '''
    
    def __init__(self):
        QDialog.__init__(self)
        self.EmailPref = EmailPref()
        self.FilterFilesWin = QDialog()
        self.FilterFilesWin.setWindowTitle('Filter File')
        self.FilterFilesWin.setWindowIcon(QIcon(path.join(getcwd(), 'images\\logo_sign_small.png')))
        self.FilterFilesLayout = QVBoxLayout()
        
    # Distructor        
    def destroyFilterFiles(self):
        del self  
        
    def CreateWindow(self):
        self.FilterFilesWin = QDialog()
        
    def GetWindow(self):
        return self.FilterFilesWin 
             
    def ShowDialog(self):     
        self.FilterFilesWin.show()
        self.FilterFilesWin.exec_()
        
        
    def SetLayout(self, layout):
        self.FilterFilesLayout = layout
        
    def SetWindowLayout(self):
        self.FilterFilesWin.setLayout(self.FilterFilesLayout)
        
    def GetLayout(self):
        return self.FilterFilesLayout
    
    # Reset Form information    
    def ResetForm(self):
        self.EmailAddrBar.setText('Email')
        self.Password.setText('Password')
        self.Project.setText('For the Project')
        
    # Get array of all projects currently working     
    def getProjects(self , src):
        ProjectsList = []
        for root, subFolders, files in walk(src):
            for file in files:
                    projectFile = open(src + "\\" + file, 'rb')
                    projectFileLines = projectFile.readlines()
                    projectFile.close()
                    if (projectFileLines):
                        ProjectsList.append(str(file).replace('.fxy', ''))
        return ProjectsList        
                                

                                    
    # All design Management Done in Here            
    def SetDesgin(self):
        
        ProjectList = self.getProjects(getcwd() + '\\projects')
        
        self.GetLayout().addStrut(200)
        self.Porjects = QComboBox()
        self.Porjects.addItems(ProjectList)
        
        
        self.GetLayout().addWidget(self.Porjects)
        self.FilterField = QLineEdit()
        self.setInformation = QPushButton("Set Information")
        self.reset = QPushButton("Reset")
        self.cancel = QPushButton("Close")
        
        self.FilterField.setPlaceholderText("Add Filter")
        
        self.FilterField.setMaximumSize(200, 100)
        self.reset.setMaximumSize(200, 100)
        self.cancel.setMaximumSize(200, 100)
        self.setInformation.setMaximumSize(200, 100)
        
        self.GetLayout().addWidget(self.FilterField)
        self.GetLayout().addWidget(self.setInformation)
        self.GetLayout().addWidget(self.reset)
        self.GetLayout().addWidget(self.cancel)
        
        self.setInformation.clicked.connect(self.SetInformation)
        self.reset.clicked.connect(self.Reset)
        self.cancel.clicked.connect(self.Cancel)
        self.Porjects.currentIndexChanged .connect(self.projectChanged)
        self.SetWindowLayout()
        self.projectChanged()
        
    # Update Filters information    
    def SetInformation(self):
        selectedProject = self.Porjects.currentText()
        Information = self.EmailPref.getConfigInfo(selectedProject)
        Information['filters'] = 'fil|' + self.FilterField.text()
        if selectedProject == '':
            QMessageBox.information(self, "Failure", "No Project Selected")
            return
        flag = self.EmailPref.setConfigInfo(Information, selectedProject)
        if flag:
            QMessageBox.information(self, "Success", "Updated the Configuration Successfully")
            self.Cancel()
            return
        else:
            QMessageBox.information(self, "Failure", "Some Problem Occurred While Update the Configurations,Please Try Again")
                
        
    def Reset(self):
        self.FilterField.setText('')
        
    # Triggers on project changed from drop down and sets related information in filters Field    
    def projectChanged(self):
        
        filters = ''
        selectedProject = self.Porjects.currentText()
        Information = self.EmailPref.getConfigInfo(selectedProject)
        filters = str(Information['filters']).replace('fil|', '').replace('\n', '')
        self.FilterField.setText(filters)
        return
    # close the dailog box
    def Cancel(self):
        self.destroyFilterFiles()
        self.FilterFilesWin.close()

# app = QApplication('asdas')
# w = FilterFiles()
# w.CreateWindow()
# w.SetWindowLayout()
# w.SetDesgin()
# w.ShowDialog()
#     
# app.exec_() 
         
