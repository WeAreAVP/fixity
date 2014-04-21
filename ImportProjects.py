# Email Preferences Setting to send eamil
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
'''
Created on Dec 5, 2013
@author: Furqan Wasi  <furqan@geekschicago.com>
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
import time
import re
import hashlib
import os

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
        self.Projects = QPushButton('Select Path')
        self.projectSelected = QTextEdit()

        self.Projects.clicked.connect(self.pickdir)

        self.GetLayout().addWidget(self.Projects)
        self.projectSelected = QLineEdit()
        self.setInformation = QPushButton("Start Importing")
        self.cancel = QPushButton("Close")

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

        if(filePath == None or filePath == ''):
            
            QMessageBox.information(self, "Error", "Please select valid Project/Manifest file path")
            
            return
        fileName = str(path.basename(filePath))
        fileName = fileName.replace('.fxy','')

        Project = DB.getProjectInfo(fileName)

        if(len(Project)>0):
            
            QMessageBox.information(self, "Error", "A Project with this name already exists!")
            
            return
       
        
        fileToImportInfoOf =  open(filePath,'rb')

        pathInformation = str(fileToImportInfoOf.readline())
        emailAddress =  str(fileToImportInfoOf.readline())
        projectConfiguration = str(fileToImportInfoOf.readline())
        lastRan  = str(fileToImportInfoOf.readline())
        allContent = fileToImportInfoOf.readlines()

        if(pathInformation and  projectConfiguration):
            versionInformation ={}
            versionInformation['versionType'] = ''
            EP = EmailPref(self)
            self.setWindowTitle('Importing Project....')
            self.parentWin.setWindowTitle('Importing Project....')
            CurrentDate = time.strftime("%Y-%m-%d")
            versionInformation['name'] = EP.EncodeInfo(str(CurrentDate))
            VersionID = DB.insert(DB._tableVersions, versionInformation)
            if(VersionID != None and VersionID !=''):
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

                # 0 = Monthly, 1 = Weekly, 2 = Daily

                Config['lastRan'] = str(lastRan)
                Config['filters'] = ''
                Config['runTime'] = runTime
                Config['durationType'] = durationType
                Config['runDayOrMonth']  = runDayOrMonth
                Config['emailOnlyUponWarning'] = 0
                Config['ifMissedRunUponRestart'] = 0
                Config['emailOnlyUponWarning'] = 0
                Config['runWhenOnBattery'] = 1
                Config['extraConf'] = ''
                Config['selectedAlgo'] = 'sha256'
                Config['emailAddress'] = str(emailAddress).replace(';','')

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
                        if(SinglePath != '' and SinglePath != None):
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

                        if FixInfo != None:
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
                                inforVersionDetail['md5_hash'] = md5_hash
                                inforVersionDetail['ssh256_hash'] = ssh256_hash
                                inforVersionDetail['path'] = FixInfo[1]
                                inforVersionDetail['inode'] = FixInfo[2]
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
        return
        self.Cancel()
        
    '''
    Pick Directory
    '''
    def pickdir(self):
        fileInformation  = list(QFileDialog.getOpenFileName())
        self.projectSelected.setText(str(fileInformation[0]))
        
    '''
    reset form
    '''
    def Reset(self):
        self.projectSelected.setText('')

    '''
    close the dailog box
    '''
    def Cancel(self):
        self.parentWin.setWindowTitle("Fixity "+self.parentWin.versoin)
        self.destroyImportProjects()
        self.close()

    '''
    Refresh Project Settings
    '''
    def refreshProjectSettings(self):
            allProjects = DB.getProjectInfo()
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
         