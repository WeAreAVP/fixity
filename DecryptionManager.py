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
from collections import defaultdict
import shutil
import datetime
#Custom Classes
from EmailPref import EmailPref
import FixityCore
import FixitySchtask
from Debuger import Debuger
from Database import Database 

class DecryptionManager(QDialog):
    ''' Class to manage the Filter to be implemented for the files with specific extensions '''
    
    def __init__(self):
        QDialog.__init__(self)
        self.EmailPref = EmailPref()
        self.DecryptionManagerWin = QDialog()
        self.DecryptionManagerWin.setWindowTitle('Encryption Manager')
        self.DecryptionManagerWin.setWindowIcon(QIcon(path.join(getcwd(), 'images\\logo_sign_small.png')))
        self.DecryptionManagerLayout = QVBoxLayout()
        
        self.isMethodChanged = False
        self.isAllfilesConfirmed = False
    # Distructor        
    def destroyDecryptionManager(self):
        del self  
        
    def CreateWindow(self):
        self.DecryptionManagerWin = QDialog()
        
    def GetWindow(self):
        return self.DecryptionManagerWin 
             
    def ShowDialog(self):     
        self.DecryptionManagerWin.show()
        self.DecryptionManagerWin.exec_()
        
        
    def SetLayout(self, layout):
        self.DecryptionManagerLayout = layout
        
    def SetWindowLayout(self):
        self.DecryptionManagerWin.setLayout(self.DecryptionManagerLayout)
        
    def GetLayout(self):
        return self.DecryptionManagerLayout
    
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
        methods = ['sha256' , 'md5']
        self.methods = QComboBox()
        self.methods.addItems(methods)
        
        
        self.GetLayout().addWidget(self.Porjects)
        self.setInformation = QPushButton("Set Information")
        
        self.cancel = QPushButton("Close")
        
        self.methods.setMaximumSize(200, 100)
        self.cancel.setMaximumSize(200, 100)
        self.setInformation.setMaximumSize(200, 100)
        
        self.GetLayout().addWidget(self.methods)
        self.GetLayout().addWidget(self.setInformation)
        self.GetLayout().addWidget(self.cancel)
        
        self.setInformation.clicked.connect(self.SetInformation)
        
        self.cancel.clicked.connect(self.Cancel)
        self.Porjects.currentIndexChanged .connect(self.projectChanged)
        self.SetWindowLayout()
        self.projectChanged()
        
        
    # Update Filters information    
    def SetInformation(self):
        
        msgBox = QLabel('Loading')
        response = True
        hasChanged = False
        selectedProject = self.Porjects.currentText()
        
        if(selectedProject == None or selectedProject == ''):
            QMessageBox.information(self, "Warning", "Please Select a Project, and Try Again.")
            return
        
        projects_path = getcwd()+'\\projects\\'
        DB  = Database()
        info = DB.getProjectInfo(selectedProject)
        Information= {}
        
        if(len(info) > 0):
            Information = info[0]
        
        aloValueSelected = ''
        if self.methods.currentText() == None or self.methods.currentText() == '':
            aloValueSelected = 'sha256' 
        else:
            aloValueSelected = str(self.methods.currentText())
        
        sameValueFlag = False
        if aloValueSelected != Information['selectedAlgo']:
            
            sameValueFlag =True
            response = self.slotWarning(selectedProject)
            if response:
                msgBox.setWindowTitle("Processing ....")
                msgBox.setText("Reading Files, please wait ...")
                msgBox.show()
                QCoreApplication.processEvents()
                Information['selectedAlgo'] = aloValueSelected
                response = True
            else:
                response = False
        else:
            sameValueFlag = False
        if selectedProject == '':
            QMessageBox.information(self, "Failure", "No Project Selected")
            return
        DB  = Database()
        flag = DB.update(DB._tableProject, Information, "id='" + str(Information['id']) + "'")
        
        if response:
            if flag :
                    try:
                        msgBox.close()
                    except:
                        pass
                    QMessageBox.information(self, "Success", "Updated the Configuration Successfully")
                    
                    self.Cancel()
                    return
            else:
                if (not hasChanged) and (sameValueFlag):
                    QMessageBox.information(self, "Information", "Everything was not confirmed that is why algorithm change did not take place.")
        return   
        
    # Triggers on project changed from drop down and sets related information in filters Field    
    def projectChanged(self):
        Algorithm = ''
        selectedProject = self.Porjects.currentText()
        DB  = Database()
        info = DB.getProjectInfo(selectedProject)
        Information= {}
        Information['selectedAlgo'] = 'sha256'
        if(len(info) > 0):
            Information = info[0]
        
    
        Algorithm = str(Information['selectedAlgo'])
    
        if Algorithm =='md5':
            self.methods.setCurrentIndex(1)
        else:
            self.methods.setCurrentIndex(0)
        return
    
    #Close the dailog box
    def Cancel(self):
        self.destroyDecryptionManager()
        self.DecryptionManagerWin.close()
        
    #Warning to change encryption value    
    def slotWarning(self, projectName):
        reply = QMessageBox.warning(self, 'Confirmation',"Are you sure you want to change Algorithum for  ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False
    def getnumberoffiles(self,path):
        return sum([len(files) for r, d, files in walk(path)])

        
   
# Method to create (hash, path, id) tables from file root
# Input: root, output (boolean), hash algorithm, QApplication
# Output: list of tuples of (hash, path, id)
    def quietTable(self,r, a , InfReplacementArray = {} , projectName = '' , counter=0):
        
        listOfValues = []
        fls = []

        try:
            for root, subFolders, files in walk(r):
                for Singlefile in files:
                    fls.append(path.join(root, Singlefile))
                                    
        except Exception as e:
                
                moreInformation = {"moreInfo":'null'}
                try:
                    if not e[0] == None:
                        moreInformation['LogsMore'] =str(e[0])
                except:
                    pass
                try:    
                    if not e[1] == None:
                        moreInformation['LogsMore1'] =str(e[1])
                except:
                    pass    
                Debugging = Debuger();
                Debugging.tureDebugerOn()    
                Debugging.logError('Error Reporting Line 140-143 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)
                
                pass    
            
        try:
            for f in xrange(len(fls)):
                
                p = path.abspath(fls[f])
                
                EcodedBasePath = InfReplacementArray[r]['code']
                
                givenPath = str(p).replace(r, EcodedBasePath+'||')
                
                h = FixityCore.fixity(p, a , projectName)
                i = FixityCore.ntfsID(p)
                listOfValues.append((h, givenPath, i))
        
                
        except Exception as e:
                
                moreInformation = {"moreInfo":'null'}
                try:
                    if not e[0] == None:
                        moreInformation['LogsMore'] =str(e[0])
                except:
                    pass
                try:    
                    if not e[1] == None:
                        moreInformation['LogsMore1'] =str(e[1])
                except:
                    pass
                
                Debugging = Debuger();
                Debugging.tureDebugerOn()    
                Debugging.logError('Error Reporting Line 169-183 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)
                
                pass        
        
        return listOfValues
#         
# app = QApplication('asdas')
# w = DecryptionManager()
# w.CreateWindow()
# w.SetWindowLayout() 
# w.SetDesgin()
# w.ShowDialog()
# app.exec_() 
# #          
# projects_path = getcwd()+'\\projects\\'
# print(w.run(projects_path+'New_Project.fxy','','New_Project'))