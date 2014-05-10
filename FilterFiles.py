# -- coding: utf-8 --
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
"""
    Builtin library
"""
import os
OS_Info = ''
if os.name == 'posix':
    OS_Info = 'linux'
elif os.name == 'nt':
    OS_Info = 'Windows'
elif os.name == 'os2':
    OS_Info = 'check'

from PySide.QtCore import *
from PySide.QtGui import *
from os import getcwd , path, listdir, remove, walk
import sys

"""
    Custom Library
"""
from Database import Database



SqlLiteDataBase = Database()


'''
Class to manage the Filter to be implemented for the files with specific extensions
'''
class FilterFiles(QDialog):

    '''
            Constructor
    '''
    def __init__(self,parentWin):

        QDialog.__init__(self,parentWin)
        self.parentWin = parentWin
        self.setWindowModality(Qt.WindowModal)
        self.parentWin.setWindowTitle('Filter File')
        self.setWindowTitle('Filter File')
        self.setWindowIcon(QIcon(path.join(getcwd(), 'images'+str(os.sep)+'logo_sign_small.png')))
        self.FilterFilesLayout = QVBoxLayout()

    '''
        Grab Key Press Events
    '''
    def keyPressEvent(self, event):

        if type(event) == QKeyEvent:
            print event.key()
        super(FilterFiles,self).keyPressEvent(event)

    '''
        catch Reject even of the Dialog box
    '''
    def reject(self):

        self.parentWin.setWindowTitle("Fixity "+self.parentWin.versoin)
        super(FilterFiles,self).reject()


    '''
        Distructor
    '''
    def destroyFilterFiles(self):

        del self


    '''
    Get Window of this
    '''
    def GetWindow(self):
        return self.FilterFilesWin

    '''
    Get Window of this
    '''
    def ShowDialog(self):
        self.show()
        self.exec_()

    '''
    Set Layout
    '''
    def SetLayout(self, layout):
        self.FilterFilesLayout = layout

    '''
    Set Window Layout
    '''
    def SetWindowLayout(self):
        self.setLayout(self.FilterFilesLayout)

    '''
    Get Layout
    '''
    def GetLayout(self):
        return self.FilterFilesLayout

    '''
    Reset Form information
    '''
    def ResetForm(self):
        self.EmailAddrBar.setText('Email')
        self.Password.setText('Password')
        self.Project.setText('Project')

    '''
    Get array of all projects currently working
    '''
    def getProjects(self , src):
        ProjectsList = []
        for root, subFolders, files in walk(src):
            for filePathFix in files:
                    projectFile = open(src + "\\" + filePathFix, 'rb')
                    projectFileLines = projectFile.readlines()
                    projectFile.close()
                    if (projectFileLines):
                        ProjectsList.append(str(filePathFix).replace('.fxy', ''))
        return ProjectsList

    '''
     All design Management Done in Here
    '''
    def SetDesgin(self):
        ProjectListArr = SqlLiteDataBase.getProjectInfo()
        counter = 0
        isEnable = True
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
        self.FilterField = QLineEdit()
        self.setInformation = QPushButton("Save && Close")
        self.reset = QPushButton("Reset")
        self.cancel = QPushButton("Close Without Saving")

        self.FilterField.setPlaceholderText("Add Filter")

        self.IgnoreHiddenFiles = QCheckBox("Ignore Hidden Files")


#         if OS_Info == 'linux':
        self.GetLayout().addWidget(self.IgnoreHiddenFiles)
        self.GetLayout().addWidget(self.FilterField)
        self.GetLayout().addWidget(self.setInformation)
        self.GetLayout().addWidget(self.reset)
        self.GetLayout().addWidget(self.cancel)

        if not isEnable:
            self.setInformation.setDisabled(True)
            self.reset.setDisabled(True)
            self.Porjects.setDisabled(True)
            self.FilterField.setDisabled(True)
            self.IgnoreHiddenFiles.setDisabled(True)

        self.setInformation.clicked.connect(self.SetInformation)
        self.reset.clicked.connect(self.Reset)
        self.cancel.clicked.connect(self.Cancel)

        self.Porjects.currentIndexChanged .connect(self.projectChanged)
        self.SetWindowLayout()
        self.projectChanged()


    '''
    Update Filters information
    '''
    def SetInformation(self):


        selectedProject = self.Porjects.currentText()
        Information = SqlLiteDataBase.getProjectInfo(selectedProject)
        Information[0]['filters'] = self.FilterField.text()
        if(self.IgnoreHiddenFiles.isChecked()):
            Information[0]['ignoreHiddenFiles'] = 1
        else:
            Information[0]['ignoreHiddenFiles'] = 0


        if selectedProject == '':

            QMessageBox.information(self, "Fixity", "No project selected - please select a project and try again.")

            return
        flag = SqlLiteDataBase.update(SqlLiteDataBase._tableProject, Information[0], "id = '"+str(Information[0]['id'])+"'")

        if flag is not None:

            QMessageBox.information(self, "Success", "Filter set successfully!")

            self.Cancel()
            return
        else:

            QMessageBox.information(self, "Failure", "There was a problem setting the filter - please try again.")


    ''' Reset Text of Filters '''
    def Reset(self):
        self.FilterField.setText('')
        self.IgnoreHiddenFiles.setChecked(False)


    '''
    Triggers on project changed from drop down and sets related information in filters Field
    '''
    def projectChanged(self):

        filters = ''
        ignoreHiddenFiles = 0
        selectedProject = self.Porjects.currentText()
        try:
            Information = SqlLiteDataBase.getProjectInfo(selectedProject)
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

        if(ignoreHiddenFiles == 1 or ignoreHiddenFiles == '1'):
            self.IgnoreHiddenFiles.setChecked(True)
        else:
            self.IgnoreHiddenFiles.setChecked(False)

        return


    '''
    Close the Dialog Box
    '''
    def Cancel(self):
        self.parentWin.setWindowTitle("Fixity "+self.parentWin.versoin)
        self.close()
        self.destroyFilterFiles()
# app = QApplication(sys.argv)
# w = FilterFiles(QDialog())
# w.SetWindowLayout()
# w.SetDesgin()
# w.ShowDialog()
# sys.exit(app.exec_())