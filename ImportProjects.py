# -*- coding: utf-8 -*-
# Import old Projects modules 
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
'''
Created on Dec 5, 2013
@author: Furqan Wasi  <furqan@geekschicago.com>
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
import time
import re
import hashlib
import datetime
import time



#Custom Classes
from Database import Database
from EmailPref import EmailPref


DB = Database()
''' Class to manage the Filter to be implemented for the files with specific extensions '''
class ImportProjects(QDialog):
    
    '''
    Constuctor
    @param parentWin: Parent Window of Import Ppojects
    '''
    def __init__(self ,parentWin):
        QDialog.__init__(self,parentWin)
        self.parentWin = parentWin
        self.setWindowModality(Qt.WindowModal)
        self.parentWin.setWindowTitle('Import Project')
        self.setWindowTitle('Import Project')
        self.setWindowIcon(QIcon(path.join(getcwd(), 'images'+str(os.sep)+'logo_sign_small.png')))
        self.ImportProjectsLayout = QVBoxLayout()
        self.projectListWidget = None
    '''
    Distructor
    '''
    def destroyImportProjects(self):
        del self
  
        
    '''
    Get Window
    '''
    def GetWindow(self):
        return self
    '''
    Show Dialog
    '''
    def ShowDialog(self):
        self.show()
        self.exec_()

    '''
    Set Layout
    '''
    def SetLayout(self, layout):
        self.ImportProjectsLayout = layout
        
    '''
    Set Window Layout
    '''
    def SetWindowLayout(self):
        self.setLayout(self.ImportProjectsLayout)
    
    '''
    Get Layout
    '''
    def GetLayout(self):
        return self.ImportProjectsLayout

    '''
    All design Management Done in Here
    '''
    def SetDesgin(self):
        

        ProjectListArr = DB.getProjectInfo()
        counter = 0
        ProjectList = []
        for PLA in ProjectListArr:
            counter = counter + 1
            ProjectList.append(ProjectListArr[PLA]['title'])


        self.GetLayout().addStrut(200)
        self.Projects = QPushButton('Select Project')
        self.projectSelected = QTextEdit()

        self.Projects.clicked.connect(self.pickdir)

        self.GetLayout().addWidget(self.Projects)
        self.projectSelected = QLineEdit()
        self.setInformation = QPushButton("Import")
        self.cancel = QPushButton("Close Without Saving")

        self.projectSelected.setPlaceholderText("Project Path")

        self.GetLayout().addWidget(self.projectSelected)
        self.GetLayout().addWidget(self.setInformation)

        self.GetLayout().addWidget(self.cancel)

        self.setInformation.clicked.connect(self.ImportProjectInformation)

        self.cancel.clicked.connect(self.Cancel)
        self.projectSelected.setDisabled(True)
        self.SetWindowLayout()
        
    '''
    Over ride reject QDialog Trigger
    '''
    def reject(self):
        self.parentWin.setWindowTitle("Fixity "+self.parentWin.versoin)
        super(ImportProjects,self).reject()
        
    '''
    Import Project Information
    '''
    def ImportProjectInformation(self):
        

        filePath = self.projectSelected.text()

        if(filePath is None or filePath == ''):
            
            QMessageBox.information(self, "Error", "Please select valid Project/Manifest file path")
            
            return
        fileName = str(path.basename(filePath))
        fileName = fileName.replace('.fxy','')
        fileName = fileName.replace('.tsv','')
        
        if '_-_-_' in fileName:
            NameOfFile =  fileName.split('_-_-_')
            if '__' in fileName:
                NameOfFileArr =  str(NameOfFile[0]).split('__')
                fileName = NameOfFileArr[0]
            else:
                fileName = NameOfFile[0]
                
        
        Project = DB.getProjectInfo(fileName)

        if(len(Project)>0):
            
            QMessageBox.information(self, "Error", "A Project with this name already exists!")
            
            return
       
        
        fileToImportInfoOf =  open(filePath,'rb')

        pathInformation = str(fileToImportInfoOf.readline())
        emailAddress =  str(fileToImportInfoOf.readline())
        projectConfiguration = str(fileToImportInfoOf.readline())
        lastRan  = str(fileToImportInfoOf.readline())
        filters  = str(self.CleanStringForDictionary(fileToImportInfoOf.readline()))
        AlgorithmSelected  = str(self.CleanStringForDictionary(fileToImportInfoOf.readline()))
        allContent = fileToImportInfoOf.readlines()
        filters = filters.split('||-||')
        if(pathInformation and  projectConfiguration):
            versionInformation ={}
            versionInformation['versionType'] = ''
            EP = EmailPref(self)
            self.setWindowTitle('Importing Project....')
            self.parentWin.setWindowTitle('Importing Project....')
            CurrentDate = time.strftime("%Y-%m-%d")
            versionInformation['name'] = EP.EncodeInfo(str(CurrentDate))
            VersionID = DB.insert(DB._tableVersions, versionInformation)
            
            if(VersionID is not None and VersionID !=''):
                Config = {}
                runDayOrMonth = ''
                durationType = 0
                runTime = '00:00'

                Config['title'] = str(fileName)
                Config['versionCurrentID'] = VersionID['id']

                information = projectConfiguration.split(' ')
                dmonth, dweek = 99, 99
                runTime = str(information[1])
                dweek = information[2]
                dmonth = str(information[3]).replace('\\r\n','')
                
                if(int(dmonth) == 99 and int(dweek) == 99):
                    durationType = 3
                    runDayOrMonth = '-'
                elif (int(dmonth) == 99 and int(dweek) != 99):

                    durationType = 2
                    runDayOrMonth = dweek
                elif(int(dmonth) != 99 and int(dweek) == 99):
                    durationType = 1
                    runDayOrMonth = dmonth
                if AlgorithmSelected == '' or AlgorithmSelected is None:
                    AlgorithmSelected = self.checkForAlgoUsed(allContent)
                # 0 = Monthly, 1 = Weekly, 2 = Daily
                
                Config['lastRan'] = str(lastRan)
                Config['filters'] = str(filters[0])
                Config['runTime'] = runTime
                Config['durationType'] = durationType
                Config['ignoreHiddenFiles'] = str(filters[1])
                Config['runDayOrMonth']  = runDayOrMonth
                Config['emailOnlyUponWarning'] = 0
                Config['ifMissedRunUponRestart'] = 0
                Config['emailOnlyUponWarning'] = 0
                Config['runWhenOnBattery'] = 1
                Config['extraConf'] = ''
                Config['selectedAlgo'] = AlgorithmSelected
                Config['emailAddress'] = self.CleanStringForDictionary(str(emailAddress).replace(';',''))

                projectID = DB.insert(DB._tableProject, Config)
                AllProjectPaths = []
                pathInfo = pathInformation.split(';')

                if '|-|-|' in pathInformation:
                    for  SinglePath in pathInfo:
                        singlePathDetail = SinglePath.split('|-|-|')
                        if(len(singlePathDetail) > 1):
                            listing = []
                            listing.append(str(singlePathDetail[0]))
                            listing.append(str(singlePathDetail[1]))
                            AllProjectPaths.append(listing)
                else:
                    counter = 1
                    for  SinglePath in pathInfo:
                        if(SinglePath != '' and SinglePath is not None):
                            listing = []
                            listing.append(str(SinglePath))
                            listing.append('Fixity-'+str(counter))
                            AllProjectPaths.append(listing)
                            counter = counter + 1
                if projectID:
                    
                    for informPath in AllProjectPaths:
                        inforProjectPath = {}
                        inforProjectPath['projectID'] = projectID['id']
                        inforProjectPath['versionID'] = VersionID['id']
                        inforProjectPath['path'] = informPath[0]
                        inforProjectPath['pathID'] = informPath[1]
                        DB.insert(DB._tableProjectPath, inforProjectPath)

                if projectID and len(allContent) > 0:

                    for singleContent in allContent:

                        FixInfo = re.split(r'\t+', singleContent)

                        if FixInfo is not None:
                            if(len(FixInfo) > 2):
                                md5_hash = ''
                                ssh256_hash = ''
                                if(len(str(FixInfo[0])) == 32):
                                    md5_hash = FixInfo[0]
                                else:
                                    ssh256_hash = FixInfo[0]
                                InforOfPathID = {}
                                if '||' in str(FixInfo[1]):
                                    InforOfPathID = str(FixInfo[1]).split('||')
                                else:
                                    for informPath in AllProjectPaths:
                                        if str(informPath[0]) in str(FixInfo[1]):
                                            InforOfPathID[0] =informPath[1]
                                            FixInfo[1] = str(FixInfo[1]).replace( str(informPath[0]), str(informPath[1]) + '||')

                                inforVersionDetail = {}
                                inforVersionDetail['projectID'] = projectID['id']
                                inforVersionDetail['versionID'] = VersionID['id']
                                inforVersionDetail['projectPathID'] = InforOfPathID[0]
                                inforVersionDetail['md5_hash'] = self.CleanStringForDictionary(md5_hash)
                                inforVersionDetail['ssh256_hash'] = self.CleanStringForDictionary(ssh256_hash)
                                inforVersionDetail['path'] = self.CleanStringForDictionary(FixInfo[1])
                                inforVersionDetail['inode'] = self.CleanStringForDictionary(FixInfo[2])
                                DB.insert(DB._tableVersionDetail, inforVersionDetail)
        
        QMessageBox.information(self, "Success", "Project importing completed ")
        self.refreshProjectSettings()
        self.parentWin.toggler(False)
        self.setWindowTitle('Import Project')
        self.parentWin.setWindowTitle('Import Project')
        try:
                    self.parentWin.old = self.projects.itemAt(0, 0)
                    self.parentWin.update(self.old)
                    self.parentWin.old.setSelected(True)
        except:
            pass
        
        try:
            fileToImportInfoOf.close()
        except:
            pass
        self.Cancel()
        return
    
    
    
    '''
    Check For Algorithm Used
    @param content: Content line containing Algorithm
    
    @return: Algorithm Used
    '''
    def checkForAlgoUsed(self,content):
        algo = 'sha256'
        for singleContent in content:
            FixInfo = re.split(r'\t+', singleContent)
            if FixInfo is not None:
                if(len(FixInfo) > 2):
                    if(len(str(FixInfo[0])) == 32):
                        algo = 'md5'
                    else:
                        algo = 'sha256'
                    return algo
        return algo 
    
    
    
    '''
    Pick Directory
    
    @return: None
    '''
    def pickdir(self):
        if OS_Info =='Windows':
            path = self.getFixityHomePath()
        else:
            path = str(self.getFixityHomePath())
            path = str(path).replace(' ', '\\ ')
            
        fileInformation  = list(QFileDialog.getOpenFileName(self,"Select File",str(path)))
        self.projectSelected.setText(str(fileInformation[0]))
        
        
        
    '''
    Reset form
    @return: None
    '''
    def Reset(self):
        self.projectSelected.setText('')


    '''
    Close the dailog box
    
    @return: None
    '''
    def Cancel(self):
        self.parentWin.setWindowTitle("Fixity "+self.parentWin.versoin)
        self.destroyImportProjects()
        self.close()



    '''
    Refresh Project Settings
    
    @return: None
    '''
    def refreshProjectSettings(self):
            allProjects = DB.getProjectInfo()
            try:
                projectLists = []
                if allProjects is not None:
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
                if projectLists is not None:
                    if(len(projectLists) > 0):
                        for p in projectLists:
                            self.projectListWidget.addItem(p)
            except:
                pass




             
    '''
    Get Fixity Home Path
    
    @return: BasePathForMacAndWindows
    '''
    def getFixityHomePath(self):
        pathInfo = str(getcwd()).replace(str(os.sep)+'Contents'+str(os.sep)+'Resources','')
        pathInfo = str(pathInfo).replace('Fixity.app'+str(os.sep), '')
        pathInfo = str(pathInfo).replace('Fixity.app', '')
        
        return str(pathInfo)
    ''' 
    CleanStringForDictionary
    @param StringToBeCleaned: String To Be Cleaned
    
    @return: CleanString  
    '''
    def CleanStringForDictionary(self,StringToBeCleaned):
        CleanString = str(StringToBeCleaned).strip()
        try:
            CleanString = CleanString.replace('\r\n', '')
            CleanString = CleanString.replace('\n', '')
            CleanString = CleanString.replace('\r', '')
        except:
            pass
        
        return CleanString
     
# app = QApplication(sys.argv)
# w = ImportProjects(QDialog())
# w.SetWindowLayout()
# w.SetDesgin()
# w.ShowDialog()
# sys.exit(app.exec_())