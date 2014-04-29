# -- coding: utf-8 --
# Change Project Name Module
# Version 0.4, Apr 1, 2014
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

'''
Created on Dec 5, 2013
@version: 0.3
@author: Furqan Wasi <furqan@avpreserve.com>
'''
from PySide.QtCore import *
from PySide.QtGui import *
from os import getcwd , path, listdir, remove, walk
import sys

'''Custom Classes'''
from EmailPref import EmailPref
from Database import Database
import FixitySchtask

SqlLiteDataBase = Database()

''' Class to manage the the Name of the project , ChangeName class manages the action of name changing and also updating the scheduler and other information changed '''

class ChangeName(QDialog):
    
    
    '''Constructor'''
    def __init__(self,parentWin):
        QDialog.__init__(self,parentWin)
        self.parentWin = parentWin
        self.EmailPref = EmailPref(self)
        
        self.setWindowModality(Qt.WindowModal)
        
        self.setWindowTitle('Change Project Name')
        self.parentWin.setWindowTitle('Change Project Name')
        self.setWindowIcon(QIcon(path.join(getcwd(), 'images\\logo_sign_small.png')))
        self.ChangeNameLayout = QVBoxLayout()
         
       
    ''' Distructor'''        
    def destroyChangeName(self):
        del self  
        
        
    '''QDailog Reject Tigger over writen'''
    def reject(self):
        self.parentWin.setWindowTitle("Fixity "+self.parentWin.versoin)
        super(ChangeName,self).reject()
        
        
    '''Get  Window'''                
    def GetWindow(self):
        return self 
    
    
    '''Show this Dialog'''         
    def ShowDialog(self):     
        self.show()
        self.exec_()
        
        
    '''Set  Layout '''   
    def SetLayout(self, layout):
        self.ChangeNameLayout = layout
        
        
    '''Set Window Layout'''
    def SetWindowLayout(self):
        self.setLayout(self.ChangeNameLayout)
        
        
    '''Get Layout '''
    def GetLayout(self):
        return self.ChangeNameLayout


    ''' Get array of all projects currently working   '''  
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
                                
        
    ''' All design Management Done in here  got the Change Name'''
    def SetDesgin(self):
        
        
        ProjectListArr = SqlLiteDataBase.getProjectInfo()
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
    
    
    ''' Update Name Of the Project and also Updating the scheduler and other information related to the Project'''
    def SetInformation(self):
        MessageBoxForChangeName = QMessageBox 
        selectedProject = self.Porjects.currentText()
        Information = SqlLiteDataBase.getProjectInfo(selectedProject)
        FixitySchtask.deltask(str(selectedProject))
        FixitySchtask.deltask(str(self.changeNameField.text()))
        if(self.changeNameField.text() == '' and self.changeNameField.text() == None):
            
            MessageBoxForChangeName.information(self, "Fixity", "No project selected - please select a project and try again.")
            return
        else:
            Information[0]['title'] = u''+self.changeNameField.text()
        
        isThisNameAlreadyTaken = SqlLiteDataBase.getProjectInfo(Information[0]['title'])
        if len(isThisNameAlreadyTaken) > 0:
            MessageBoxForChangeName.information(self, "Fixity", "A project with this name already exists - please enter a new project name.")
            return
        flag = SqlLiteDataBase.update(SqlLiteDataBase._tableProject, Information[0], "id = '"+str(Information[0]['id'])+"'")
        if flag != None:
            self.refreshProjectSettings()
            thisItemIndex = self.parentWin.getProjectIndex(str(Information[0]['title']))

            MessageBoxForChangeName.information(self, "Success", "Project name changed successfully!")
            self.parentWin.projects.item(thisItemIndex).setSelected(True)
            self.parentWin.changedNameIndex = thisItemIndex
            self.parentWin.changedNameName = Information[0]['title']
            self.Cancel()
            return
        else:
            
            MessageBoxForChangeName.information(self, "Failure", "There was a problem changing the project name - please try again.")
            self.refreshProjectSettings()
            self.reOpenChangeName()
                
                
                
    '''Reset the Text'''
    def Reset(self):
        self.changeNameField.setText('')
    
    
    
    
    '''Re Open Change Name'''
    def reOpenChangeName(self):
        self.Cancel()
        self.EmailPref = EmailPref(self)
        self = QDialog()
        
        self.setWindowTitle('Change Project Name')
        self.setWindowIcon(QIcon(path.join(getcwd(), 'images\\logo_sign_small.png')))
        self.ChangeNameLayout = QVBoxLayout()
        
        
        
    ''' close the dailog box'''
    def Cancel(self):
        self.parentWin.setWindowTitle("Fixity "+self.parentWin.versoin)
        self.refreshProjectSettings()
        self.destroyChangeName()
        self.close()
        
        
        
    '''Refresh Project Settings on the main Window'''
    def refreshProjectSettings(self):
            allProjects = SqlLiteDataBase.getProjectInfo()
            try:
                projectLists = []
                if allProjects != None:
                    if(len(allProjects) > 0):
                        for p in allProjects:
                            projectLists.append(str(allProjects[p]['title']))
            except Exception as ex:
                print(ex[0])
            
            try:  
                self.parentWin.projects.clear()
            except Exception as ex:
                print(ex[0])
            
            try:
                if projectLists != None:
                    if(len(projectLists) > 0):
                        for p in projectLists:
                            self.parentWin.projects.addItem(p)
            except Exception as ex:
                print(ex[0])
# app = QApplication(sys.argv)
# w = FilterFiles(QDialog())
# w.SetWindowLayout()
# w.SetDesgin()
# w.ShowDialog()
# sys.exit(app.exec_())
