# -- coding: utf-8 --
# Encryption and decryption manager of files hashes
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

'''
Created on Dec 5, 2013
@author: Furqan Wasi <furqan@geekschicago.com>
'''

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
from collections import defaultdict
import shutil
import datetime


'''Custom Classes'''
    
from EmailPref import EmailPref
import FixityCore    
import FixitySchtask
from Debuger import Debuger
from Database import Database

Debugging = Debuger()
''' Class to manage the Filter to be implemented for the files with specific extensions '''

class DecryptionManager(QDialog):
    
    '''Constructor'''
    
    def __init__(self,parentWin):
        QDialog.__init__(self,parentWin)
        self.parentWin = parentWin
        self.EmailPref = EmailPref(self)
        self.setWindowModality(Qt.WindowModal)
        
        self.setWindowTitle('Checksum Manager')
        self.parentWin.setWindowTitle('Checksum Manager')
        self.setWindowIcon(QIcon(path.join(getcwd(), 'images'+str(os.sep)+'logo_sign_small.png')))

        self.DecryptionManagerLayout = QVBoxLayout()
        
        self.isMethodChanged = False
        self.isAllfilesConfirmed = False
        
    '''
    Distructor
    '''
    def destroyDecryptionManager(self):
        del self
        
    '''Reject'''
    def reject(self):
        self.parentWin.setWindowTitle("Fixity "+self.parentWin.versoin)
        super(DecryptionManager,self).reject()
        
    '''Create Window'''
    def CreateWindow(self):
        self = QDialog()
        

    '''Create Window info'''
    def GetWindow(self):
        return self


    '''Create Show Window'''
    def ShowDialog(self):
        self.show()
        self.exec_()


    '''Create Show Window'''
    def SetLayout(self, layout):
        self.DecryptionManagerLayout = layout
        
        
    '''Set Layout for Windows'''
    def SetWindowLayout(self):
        self.setLayout(self.DecryptionManagerLayout)
        
        
    '''Get Layout'''
    def GetLayout(self):
        return self.DecryptionManagerLayout


    ''' Reset Form information'''
    def ResetForm(self):
        self.EmailAddrBar.setText('Email')
        self.Password.setText('Password')
        self.Project.setText('For the Project')

    ''' Get array of all projects currently working'''
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



    ''' All design Management Done in Here'''
    def SetDesgin(self):
        SqlLiteDataBase = Database()


        ProjectList = SqlLiteDataBase.getProjectInfo(None,False)
        isEnable = True
        AllProjectList = []
        if(len(ProjectList) > 0):
            for singleProj in ProjectList:
                AllProjectList.append(ProjectList[singleProj]['title'])
            isEnable = True
        else:
            AllProjectList.append('Create & Save Project')
            isEnable = False
            

        self.GetLayout().addStrut(200)
        self.Porjects = QComboBox()
        self.Porjects.addItems(AllProjectList)
        methods = ['sha256' , 'md5']
        self.methods = QComboBox()
        self.methods.addItems(methods)


        self.GetLayout().addWidget(self.Porjects)
        self.setInformation = QPushButton("Set Information")

        self.cancel = QPushButton("Close")


        self.GetLayout().addWidget(self.methods)
        self.GetLayout().addWidget(self.setInformation)
        self.GetLayout().addWidget(self.cancel)

        self.setInformation.clicked.connect(self.SetInformation)
        if not isEnable:
            self.methods.setDisabled(True)
            self.setInformation.setDisabled(True)
            self.Porjects.setDisabled(True)
            
        self.cancel.clicked.connect(self.Cancel)
        self.Porjects.currentIndexChanged.connect(self.projectChanged)
        self.SetWindowLayout()
        self.projectChanged()


    ''' Update Filters information'''
    def SetInformation(self):

        msgBox = QLabel('Loading')
        response = True
        hasChanged = False
        selectedProject = self.Porjects.currentText()

        if(selectedProject is None or selectedProject == ''):
            
            QMessageBox.information(self, "Warning", "No project selected.\nPlease select a project and try again.")
            return

        projects_path = getcwd()+'\\projects\\'
        SqlLiteDataBase  = Database()
        info = SqlLiteDataBase.getProjectInfo(selectedProject)
        Information= {}
        if(len(info) > 0):
            Information = info[0]
        ResponseIsAnyThingChanged = True
            
        aloValueSelected = ''
        if Information['selectedAlgo'] == str(self.methods.currentText()):
            QMessageBox.information(self, "Failure", "This Project is Already using this algorithm.")
            return
        
        if self.methods.currentText() is None or self.methods.currentText() == '':
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
                try:
                    ResponseIsAnyThingChanged = FixityCore.run(selectedProject, Information['filters'], '', True)
                except Exception as Exp:
                    print(Exp[0])
            else:
                response = False
                
        else:
            sameValueFlag = False
            
        if selectedProject == '':
            QMessageBox.information(self, "Failure", "No project selected.\nPlease select a project and try again.")
            return
        flag = False
        if not ResponseIsAnyThingChanged:
            SqlLiteDataBase  = Database()
            SqlLiteDataBase.update(SqlLiteDataBase._tableProject, Information, "id='" + str(Information['id']) + "'")
            flag = True

        if response:
            if flag:
                    try:
                        msgBox.close()
                    except:
                        pass
                    
                    QMessageBox.information(self, "Success", selectedProject+"'s algorithm has been changed successfully.")

                    self.Cancel()
                    return
            else:
                if (not hasChanged) and (sameValueFlag):
                    if ResponseIsAnyThingChanged:
                        QMessageBox.information(self, "Information", selectedProject+"'s algorithm was NOT successfully changed, because all files were not confirmed, please try again.")
                    else:
                        QMessageBox.information(self, "Information", selectedProject+"'s algorithm was NOT successfully changed - please try again.")
        return


    ''' Triggers on project changed from drop down and sets related information in filters Field'''
    def projectChanged(self):
        Algorithm = ''
        selectedProject = self.Porjects.currentText()
        SqlLiteDataBase  = Database()
        info = SqlLiteDataBase.getProjectInfo(selectedProject)
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

    '''Close the dailog box'''
    def Cancel(self):
        self.setWindowTitle("Fixity "+self.parentWin.versoin)
        self.destroyDecryptionManager()
        self.close()


    '''Warning to change encryption value'''
    def slotWarning(self, projectName):
        
        reply = QMessageBox.warning(self, 'Confirmation',"Are you sure that you want to change the checksum algorithm for " + projectName + "?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            return True
        else:
            return False
    def getnumberoffiles(self,path):
        return sum([len(files) for r, d, files in walk(path)])



    ''' 
    Method to create (hash, path, id) tables from file root
    Input: root, output (boolean), hash algorithm, QApplication
    Output: list of tuples of (hash, path, id)
    '''
    
    def quietTable(self,r, a , InfReplacementArray = {} , projectName = '' , counter=0):

        listOfValues = []
        fls = []

        try:
            for root, subFolders, files in walk(r):
                for Singlefile in files:
                    fls.append(path.join(root, Singlefile))

        except Exception as Except:

                moreInformation = {"moreInfo":'null'}
                try:
                    if  Except[0] is not None:
                        moreInformation['LogsMore'] =str(Except[0])
                except:
                    pass
                try:
                    if  Except[1] is not None:
                        moreInformation['LogsMore1'] =str(Except[1])
                except:
                    pass

                Debugging.tureDebugerOn()
                Debugging.logError('Error Reporting Line 140-143 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)

                pass

        try:
            for f in xrange(len(fls)):

                p = path.abspath(fls[f])

                EcodedBasePath = InfReplacementArray[r]['code']

                givenPath = str(p).replace(r, EcodedBasePath+'||')

                h = FixityCore.fixity(p, a , projectName)
                if(OS_Info == 'Windows'):
                    i = FixityCore.FixityCoreWin.ntfsIDForWindows(p)
                else:
                    i = FixityCore.FixityCoreMac.ntfsIDForMac(p)
                listOfValues.append((h, givenPath, i))


        except Exception as Except:

                moreInformation = {"moreInfo":'null'}
                try:
                    if  Except[0] is not None:
                        moreInformation['LogsMore'] =str(Except[0])
                except:
                    pass
                try:
                    if  Except[1] is not None:
                        moreInformation['LogsMore1'] =str(Except[1])
                except:
                    pass


                Debugging.tureDebugerOn()
                Debugging.logError('Error Reporting Line 169-183 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)

                pass

        return listOfValues

# app = QApplication('asdas')
# wDM = DecryptionManager(QDialog())
# wDM.SetWindowLayout()
# wDM.SetDesgin()
# wDM.ShowDialog()
# sys.exit(app.exec_())