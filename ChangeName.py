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
from Database import Database

#Custom Classes
from EmailPref import EmailPref
DBObj = Database()

class ChangeName(QDialog):
    ''' Class to manage the Filter to be implemented for the files with specific extensions '''
    
    def __init__(self):
        QDialog.__init__(self)
        self.EmailPref = EmailPref()
        self.ChangeNameWin = QDialog()
#         flags =  Qt.Window
        flags =  Qt.WindowTitleHint
#         flags =  Qt.CustomizeWindowHint  
        self.ChangeNameWin.setWindowFlags(flags)
        
        self.ChangeNameWin.setWindowTitle('Change Project Name')
        self.ChangeNameWin.setWindowIcon(QIcon(path.join(getcwd(), 'images\\logo_sign_small.png')))
        self.ChangeNameLayout = QVBoxLayout()
         
        self.projectListWidget = None
        
    # Distructor        
    def destroyChangeName(self):
        del self  
        
    def CreateWindow(self):
        self.ChangeNameWin = QDialog()
        
        
    def GetWindow(self):
        return self.ChangeNameWin 
             
    def ShowDialog(self):     
        self.ChangeNameWin.show()
        self.ChangeNameWin.exec_()
        
        
        
    def SetLayout(self, layout):
        self.ChangeNameLayout = layout
        
    def SetWindowLayout(self):
        self.ChangeNameWin.setLayout(self.ChangeNameLayout)
        
    def GetLayout(self):
        return self.ChangeNameLayout
    

        
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
        
        
        ProjectListArr = DBObj.getProjectInfo()
        isEnable = True
        counter = 0 
        ProjectList = []
        if(len(ProjectListArr) > 0):
            for PLA in ProjectListArr:
                counter = counter + 1
                ProjectList.append(ProjectListArr[PLA]['title'])
            isEnable = True
        else:
            ProjectList.append('Create & Save Project')
            isEnable = False
        
        self.GetLayout().addStrut(200)
        self.Porjects = QComboBox()
        self.Porjects.addItems(ProjectList)
        
        
        self.GetLayout().addWidget(self.Porjects)
        self.changeNameField = QLineEdit()
        self.setInformation = QPushButton("Set Information")
        
        self.cancel = QPushButton("Close")
        
        self.changeNameField.setPlaceholderText("Add New Name")
        
        self.changeNameField.setMaximumSize(200, 100)
        
        self.cancel.setMaximumSize(200, 100)
        self.setInformation.setMaximumSize(200, 100)
        
        self.GetLayout().addWidget(self.changeNameField)
        self.GetLayout().addWidget(self.setInformation)
        
        self.GetLayout().addWidget(self.cancel)
        
        self.setInformation.clicked.connect(self.SetInformation)
        
        self.cancel.clicked.connect(self.Cancel)
        self.Porjects.currentIndexChanged .connect(self.projectChanged)
        if not isEnable:
            self.setInformation.setDisabled(True)
            self.changeNameField.setDisabled(True)
            self.Porjects.setDisabled(True)
            
        self.SetWindowLayout()
        self.projectChanged()
        
    def projectChanged(self):
        return
    # Update Filters information    
    def SetInformation(self):
        
        QMB = QMessageBox 
        selectedProject = self.Porjects.currentText()
        Information = DBObj.getProjectInfo(selectedProject)
        if(self.changeNameField.text() == '' and self.changeNameField.text() == None):
            
            QMB.information(self, "Fixity", "No project selected - please select a project and try again.")
            
            return
        else:
            Information[0]['title'] = u''+self.changeNameField.text()
        
       
        flag = DBObj.update(DBObj._tableProject, Information[0], "id = '"+str(Information[0]['id'])+"'")
        if flag != None:
            self.refreshProjectSettings()
            
            QMB.information(self, "Success", "Name have changed successfully!")
            
            self.Cancel()
            
            return
        else:
            
            QMB.information(self, "Failure", "There was a problem setting the filter - please try again.")
            self.refreshProjectSettings()
            self.reOpenChangeName()
                
        
    def Reset(self):
        self.changeNameField.setText('')
        
    def reOpenChangeName(self):
        self.Cancel()
        self.EmailPref = EmailPref()
        self.ChangeNameWin = QDialog()
        
        self.ChangeNameWin.setWindowTitle('Change Project Name')
        self.ChangeNameWin.setWindowIcon(QIcon(path.join(getcwd(), 'images\\logo_sign_small.png')))
        self.ChangeNameLayout = QVBoxLayout()
        self.projectListWidget = None
        
    # close the dailog box
    def Cancel(self):
        self.refreshProjectSettings()
        self.destroyChangeName()
        self.ChangeNameWin.close()
        
    def refreshProjectSettings(self):
            allProjects = DBObj.getProjectInfo()
            try:
                projectLists = []
                if allProjects != None:
                    if(len(allProjects) > 0):
                        for p in allProjects:
                            projectLists.append(str(allProjects[p]['title']))
            except:
                pass
            
            try:  
                self.projectListWidget.clear()
            except:
                pass
            
            try:
                if projectLists != None:
                    if(len(projectLists) > 0):
                        for p in projectLists:
                            self.projectListWidget.addItem(p)
            except:
                pass
            
# app = QApplication('asdas')
# w = ChangeName()
# w.CreateWindow()
# w.SetWindowLayout()
# w.SetDesgin()
# w.ShowDialog()
#          
# app.exec_() 
         
