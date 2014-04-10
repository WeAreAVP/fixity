# Fixity Filters (File Not to Scan)
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

'''
Created on Dec 5, 2013
@version: 0.3
@author: Furqan Wasi <furqan@geekschicago.com>
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
import os
from Database import Database

#Custom Classes
from EmailPref import EmailPref
DB = Database()

class FilterFiles(QDialog):
    ''' Class to manage the Filter to be implemented for the files with specific extensions '''
    # Constructor
    def __init__(self):
        QDialog.__init__(self)
        self.EmailPref = EmailPref()
        self.FilterFilesWin = QDialog()
        self.FilterFilesWin.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.FilterFilesWin.setWindowTitle('Filter File')
        self.FilterFilesWin.setWindowIcon(QIcon(path.join(getcwd(), 'images'+str(os.sep)+'logo_sign_small.png')))
        self.FilterFilesLayout = QVBoxLayout()

    # Distructor
    def destroyFilterFiles(self):
        del self

    # Create Window For this
    def CreateWindow(self):
        self.FilterFilesWin = QDialog()
        self.FilterFilesWin.setWindowFlags(Qt.WindowStaysOnTopHint)

    # Get Window of this
    def GetWindow(self):
        return self.FilterFilesWin

    # Get Window of this
    def ShowDialog(self):
        self.FilterFilesWin.show()
        self.FilterFilesWin.exec_()

    # Set Layout
    def SetLayout(self, layout):
        self.FilterFilesLayout = layout

    # Set Window Layout
    def SetWindowLayout(self):
        self.FilterFilesWin.setLayout(self.FilterFilesLayout)

    # Get Layout
    def GetLayout(self):
        return self.FilterFilesLayout

    # Reset Form information
    def ResetForm(self):
        self.EmailAddrBar.setText('Email')
        self.Password.setText('Password')
        self.Project.setText('Project')

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
        

        ProjectListArr = DB.getProjectInfo()
        counter = 0
        ProjectList = []
        for PLA in ProjectListArr:
            counter = counter + 1
            ProjectList.append(ProjectListArr[PLA]['title'])

        self.GetLayout().addStrut(200)
        self.Porjects = QComboBox()
        self.Porjects.addItems(ProjectList)

        self.GetLayout().addWidget(self.Porjects)
        self.FilterField = QLineEdit()
        self.setInformation = QPushButton("Set Information")
        self.reset = QPushButton("Reset")
        self.cancel = QPushButton("Close")

        self.FilterField.setPlaceholderText("Add Filter")
        
        self.IgnoreHiddenFiles = QCheckBox("Ignore Hidden Files")
        
        self.FilterField.setMaximumSize(200, 100)
        self.reset.setMaximumSize(200, 100)
        self.cancel.setMaximumSize(200, 100)
        self.setInformation.setMaximumSize(200, 100)
        
        self.GetLayout().addWidget(self.IgnoreHiddenFiles)
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
        Information = DB.getProjectInfo(selectedProject)
        Information[0]['filters'] = self.FilterField.text()
        if(self.IgnoreHiddenFiles.isChecked()):
            Information[0]['ignoreHiddenFiles'] = 1
        else:
            Information[0]['ignoreHiddenFiles'] = 0

        
        if selectedProject == '':
            self.FilterFilesWin.setWindowFlags(Qt.WindowStaysOnBottomHint)
            QMessageBox.information(self, "Fixity", "No project selected - please select a project and try again.")
            self.FilterFilesWin.setWindowFlags(Qt.WindowStaysOnTopHint)
            return
        flag = DB.update(DB._tableProject, Information[0], "id = '"+str(Information[0]['id'])+"'")

        if flag != None:
            self.FilterFilesWin.setWindowFlags(Qt.WindowStaysOnBottomHint)
            QMessageBox.information(self, "Success", "Filter set successfully!")
            self.FilterFilesWin.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.Cancel()
            return
        else:
            self.FilterFilesWin.setWindowFlags(Qt.WindowStaysOnBottomHint)
            QMessageBox.information(self, "Failure", "There was a problem setting the filter - please try again.")
            self.FilterFilesWin.setWindowFlags(Qt.WindowStaysOnTopHint)

    # Reset Text of Filters
    def Reset(self):
        self.FilterField.setText('')

    # Triggers on project changed from drop down and sets related information in filters Field
    def projectChanged(self):
        
        filters = ''
        ignoreHiddenFiles = 0
        selectedProject = self.Porjects.currentText()
        try:
            Information = DB.getProjectInfo(selectedProject)
        except:
            pass

        try:
            filters = str(Information[0]['filters']).replace('\n', '')
        except:
            pass
        
        try:
            ignoreHiddenFiles = str(Information[0]['ignoreHiddenFiles']).replace('\n', '')
        except:
            pass
        
        self.FilterField.setText(filters)
        
        if(ignoreHiddenFiles == 0 or ignoreHiddenFiles == '0'):
            self.IgnoreHiddenFiles.setChecked(False)
        else:
            self.IgnoreHiddenFiles.setChecked(True)
            
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