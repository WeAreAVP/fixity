# -*- coding: utf-8 -*-
# Fixity GUI
# Version 0.4, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0


import os
OS_Info = ''
if os.name == 'posix':
    OS_Info = 'linux'
elif os.name == 'nt':
    OS_Info = 'Windows'
elif os.name == 'os2':
    OS_Info = 'check'

''' Built-in Libraries ''' 
from PySide.QtCore import *
from PySide.QtGui import *

if OS_Info == 'linux':
    from os import path, listdir, remove, walk, getcwd, spawnl, system
else:
    from os import path, listdir, remove, walk, getcwd, P_DETACH, spawnl, system

from collections import deque
from genericpath import exists
import re
import datetime
import shutil
import sys
import argparse
import platform
import os



''' Custom Libraries '''
import FixityCore
import FixitySchtask
from Threading import Threading
from EmailPref import EmailPref
from Debuger import Debuger
from FilterFiles import FilterFiles
from FileChanged import FileChanged
from DecryptionManager import DecryptionManager
from Database import Database
from ImportProjects import ImportProjects
from AboutFixity import AboutFixity
from ChangeName import ChangeName
from AutoRuner import AutoRuner

Debuging = Debuger()

'''Main Class to handle all menu and options of Fixity'''


class ProjectWin(QMainWindow):


        ''' Constructor '''
        def __init__(self, EmailPref, FilterFiles):

                if(OS_Info == 'Windows'):
                    self.CreateAllRequiredFileAndDirectoriesForWindows()
                else:
                    self.CreateAllRequiredFileAndDirectoriesForMac()

                self.Database = Database()
                self.createDatabaseTables()

                pathInfo = str(getcwd()).replace('\\schedules', '')
                pathInfo = pathInfo.replace('schedules', '')


                if(OS_Info == 'Windows'):
                    databasePath = pathInfo+"\\bin\\Fixity.db-journal"
                else:
                    databasePath = pathInfo+"/bin/Fixity.db-journal"

                if path.isfile(databasePath):
                    remove(databasePath)

                QMainWindow.__init__(self)
                Debuging.tureDebugerOn()
                Debuging.logInfo('Logger started!::::::::::::::::::' + "\n",{} )

                self.SystemInformation = self.getWindowsInformation()
                if(self.SystemInformation):
                    if OS_Info == 'Windows':
                        Debuging.logInfo('System Information' + "\n" ,{})
                        Debuging.logInfo('platform = '+str(self.SystemInformation['platform'])  , {} )
                        Debuging.logInfo('major = '+ str(self.SystemInformation['major']) , {} )
                        Debuging.logInfo('minor = '+str(self.SystemInformation['minor'])  , {} )
                        Debuging.logInfo('build = '+str(self.SystemInformation['build'])  , {} )
                        Debuging.logInfo('platformType = '+str(self.SystemInformation['platformType'])  , {} )
                        Debuging.logInfo('isWindows = '+str(self.SystemInformation['isWindows'])  , {} )
                        Debuging.logInfo('WindowsType = '+str(self.SystemInformation['WindowsType'])  , {} )
                        Debuging.logInfo('bitType = '+str(self.SystemInformation['bitType'])  , {} )

                self.EmailPrefManager = EmailPref(self)
                self.AboutFixityManager = AboutFixity(self)
                self.EmailPrefManager.setVersion('0.4')
                self.DecryptionManager = DecryptionManager(self)
                self.FileChanged = FileChanged(self)
                self.ImportProjects = ImportProjects(self)
                self.ChangeName = ChangeName(self)
                self.changedNameIndex = None
                self.changedNameName = None
                self.FileChanged.setVersion('0.4')

                self.FilterFiles = FilterFiles(self)
                self.Threading = Threading

                self.setWindowIcon(QIcon(path.join(getcwd(), 'images'+str(os.sep)+'logo_sign_small.png')))
                self.versoin = self.EmailPrefManager.getVersion()
                self.setWindowTitle("Fixity "+self.versoin)
                self.unsaved = False
                menubar = self.menuBar()
                self.FileManuFixity = menubar.addMenu('&File')
                self.Preferences = menubar.addMenu('&Preferences')
                newp = QAction('&New Project', self)
                newp.setShortcut('CTRL+N')
                save = QAction('&Run Now', self)
                save.setShortcut('CTRL+R')
                usch = QAction('&Save Settings', self)
                usch.setShortcut('CTRL+S')
                dlte = QAction('&Delete Project', self)
                dlte.setShortcut(QKeySequence.DeleteStartOfWord)
                self.configemail = QAction('&Email Settings', self)
                self.configemail.setShortcut("CTRL+E")
                aboutFixity = QAction('&About Fixity', self)
                aboutFixity.setShortcut('CTRL+,')
                quitMenu = QAction('&Quit Fixity', self)
                quitMenu.setShortcut(QKeySequence.Quit)

                FilterFilesMane = QAction('&Filter Files', self)
                FilterFilesMane.setShortcut('CTRL+F')
                ChangeNameManu = QAction('&Change Project Name', self)
                ChangeNameManu.setShortcut("CTRL+U");
                DecryptionManagerMenu = QAction('&Select Checksum Algorithm', self)
                DecryptionManagerMenu.setShortcut("CTRL+A")

                self.Debuging = QAction('&Turn Debuging Off', self)
                self.Debuging.setShortcut("CTRL+D")
                self.ImportProjectfxy = QAction('&Import Project', self)
                self.ImportProjectfxy.setShortcut("CTRL+I");
                self.switchDebugger('start')

                self.FileManuFixity.addAction(newp)
                self.FileManuFixity.addAction(usch)
                self.FileManuFixity.addAction(save)
                self.FileManuFixity.addAction(dlte)
                self.FileManuFixity.addAction(ChangeNameManu)
                self.FileManuFixity.addAction(aboutFixity)
                self.FileManuFixity.addAction(quitMenu)

                self.Preferences.addAction(FilterFilesMane)

                self.Preferences.addAction(self.Debuging)
                self.Preferences.addAction(DecryptionManagerMenu)
                self.Preferences.addAction(self.ImportProjectfxy)
                self.Preferences.addAction(self.configemail)

                dlte.triggered.connect(self.deleteproject)
                newp.triggered.connect(self.new)
                self.configemail.triggered.connect(self.ConfigEmailView)
                save.triggered.connect(self.run)
                usch.triggered.connect(self.updateschedule)
                aboutFixity.triggered.connect(self.AboutFixityView)
                quitMenu.triggered.connect(self.close)

                FilterFilesMane.triggered.connect(self.FilterFilesBox)
                ChangeNameManu.triggered.connect(self.ChangeNameBox)

                DecryptionManagerMenu.triggered.connect(self.DecryptionManagerBox)
                self.Debuging.triggered.connect(self.switchDebugger)
                self.ImportProjectfxy.triggered.connect(self.importProjects)

                self.widget = QWidget(self)

                self.pgroup = QGroupBox("Projects")
                self.play = QVBoxLayout()
                self.projects = QListWidget(self)

                self.projects.setFixedSize(115, 190)
                allProjects = self.Database.getProjectInfo()

                projectLists = []
                if allProjects is not None:
                    if(len(allProjects) > 0):
                        for p in allProjects:
                            projectLists.append(str(allProjects[p]['title']))

                if projectLists is not  None:
                    if(len(projectLists) > 0):
                        for p in projectLists:
                            QListWidgetItem(str(p), self.projects)
                self.projects.setCurrentRow(0)
                self.play.addWidget(self.projects)
                self.pgroup.setLayout(self.play)

                self.sch = QGroupBox("Scheduling")
                self.monthly = QRadioButton("Monthly")
                self.weekly = QRadioButton("Weekly")
                self.daily = QRadioButton("Daily")

                self.runOnlyOnACPower = QCheckBox("Run when on battery power")
                self.StartWhenAvailable = QCheckBox("If missed, run upon restart")
                self.EmailOnlyWhenSomethingChanged = QCheckBox("Email only upon warning or failure")

                self.runOnlyOnACPower.setChecked(True)
                self.StartWhenAvailable.setChecked(True)
                self.EmailOnlyWhenSomethingChanged.setChecked(True)

                self.monthly.clicked.connect(self.monthclick)
                self.weekly.clicked.connect(self.weekclick)
                self.daily.clicked.connect(self.dayclick)

                slay = QVBoxLayout()

                slay.addWidget(self.monthly)
                slay.addWidget(self.weekly)
                slay.addWidget(self.daily)

                self.timer = QTimeEdit(QTime())
                self.timer.setDisplayFormat("HH:mm")
                slay.addWidget(self.timer)

                self.dow = QComboBox()
                self.dow.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
                self.dow.activated.connect(self.changed)
                slay.addWidget(self.dow)
                self.dow.hide()

                self.dom = QSpinBox()
                self.dom.setMaximum(31)
                self.dom.setMinimum(1)
                self.dom.valueChanged.connect(self.changed)
                slay.addWidget(self.dom)
                self.dom.hide()

                self.spacer = QSpacerItem(125, 30)
                slay.addItem(self.spacer)
                if OS_Info == 'Windows':
                    slay.addWidget(self.runOnlyOnACPower)
                    slay.addWidget(self.StartWhenAvailable)
                slay.addWidget(self.EmailOnlyWhenSomethingChanged)

                self.lastrun = QLabel("Last checked: ")
                slay.addWidget(self.lastrun)
                self.sch.setLayout(slay)
                self.sch.setFixedSize(255, 269)

                self.mlay = QVBoxLayout()
                self.mlay.setSpacing(0)
                self.mtx = []
                for n in xrange(0, 7):
                        self.mtx.append(QLineEdit())
                        self.mlay.addWidget(self.mtx[n])
                        self.mtx[n].textChanged.connect(self.changed)

                self.dlay = QVBoxLayout()
                self.dlay.setSpacing(0)
                self.dtx, self.but = [], []

                for n in xrange(0, 7):
                    hbox = QHBoxLayout()
                    hbox.setContentsMargins(0, 0, 0, 0)
                    hbox.setSpacing(0)
                    self.dtx.append(QLineEdit())
                    self.but.append(QPushButton('...'))
                    self.but[n].setFixedSize(30, 21)
                    self.dtx[n].setContentsMargins(0, 2, 7, 0)
                    self.dtx[n].setFixedSize(150,22)
                    self.but[n].clicked.connect(self.pickdir)
                    self.dtx[n].textChanged.connect(self.changed)
                    hbox.addWidget(self.dtx[n])
                    hbox.addWidget(self.but[n])
                    self.dlay.addLayout(hbox)

                self.dirs = QGroupBox("Directories")
                self.mail = QGroupBox("Recipient Email Addresses")
                self.dirs.setLayout(self.dlay)
                self.mail.setLayout(self.mlay)

                self.main = QHBoxLayout()

                self.main.addWidget(self.pgroup)
                self.main.addWidget(self.sch)
                self.main.addWidget(self.dirs)
                self.main.addWidget(self.mail)

                self.widget.setLayout(self.main)
                self.setCentralWidget(self.widget)
                self.projects.itemClicked.connect(self.update)
                if OS_Info == 'Windows':
                    if(self.SystemInformation and str(self.SystemInformation['WindowsType']) == '7'):
                        self.runOnlyOnACPower.setDisabled(False)
                        self.StartWhenAvailable.setDisabled(False)
                        self.EmailOnlyWhenSomethingChanged.setDisabled(False)
                    else:
                        self.runOnlyOnACPower.setDisabled(True)
                        self.StartWhenAvailable.setDisabled(True)
                        self.EmailOnlyWhenSomethingChanged.setDisabled(True)

                try:
                    self.old = self.projects.itemAt(0, 0)
                    self.update(self.old)
                    self.old.setSelected(True)
                except:
                    pass
                if(len(allProjects) <= 0):
                    self.runOnlyOnACPower.setDisabled(True)
                    self.StartWhenAvailable.setDisabled(True)
                    self.EmailOnlyWhenSomethingChanged.setDisabled(True)

                self.closeEvent(self.cleanObjects)

                self.unsaved = False
                self.toggler((self.projects.count() == 0))
                self.show()

        ''' Distructor '''
        def __del__(self):
            del self

        '''
        Clean All Objects Existed
        Closing opened Windows and database connections and Releasing the Variables
        '''
        def cleanObjects(self):

            '''  Closing opened Windows and database connections ''' 
            try:
                self.Database.closeConnection()
            except:
                pass
            try:
                self.EmailPrefManager.CloseClick()
            except:
                pass
            try:
                self.AboutFixityManager.Cancel()
            except:
                pass
            try:
                self.DecryptionManager.Cancel()
            except:
                pass
            try:
                self.FileChanged.CloseClick()
            except:
                pass
            try:
                self.ImportProjects.Cancel()
            except:
                pass
            try:
                self.ChangeName.Cancel()
            except:
                pass
            try:
                self.FilterFiles.Cancel()
            except:
                pass
            try:
                self.Threading = None
            except:
                pass

            '''  Releasing the Variables ''' 
            try:
                self.Database = None
            except:
                pass
            try:
                self.EmailPrefManager = None
            except:
                pass
            try:
                self.AboutFixityManager = None
            except:
                pass
            try:
                self.DecryptionManager = None
            except:
                pass
            try:
                self.FileChanged = None
            except:
                pass
            try:
                self.ImportProjects = None
            except:
                pass
            try:
                self.ChangeName = None
            except:
                pass
            try:
                self.FilterFiles = None
            except:
                pass
            try:
                self.__del__()
            except:
                pass


        '''
        Configure Email Address for the Tools
        '''
        def ConfigEmailView(self):
            self.EmailPrefManager.CloseClick()
            self.EmailPrefManager = None
            self.EmailPrefManager = EmailPref(self)
            self.EmailPrefManager.SetDesgin()
            self.EmailPrefManager.ShowDialog()

        '''
        PopUp to Import Project
        '''
        def importProjects(self):
            self.ImportProjects.destroyImportProjects()
            self.ImportProjects = None
            self.ImportProjects = ImportProjects(self)
            self.ImportProjects.projectListWidget = self.projects
            self.ImportProjects.SetDesgin()
            self.ImportProjects.ShowDialog()


        '''
        Pop up to Show About Fixity Information
        '''
        def AboutFixityView(self):

            self.AboutFixityManager.Cancel()
            self.AboutFixityManager = None
            self.AboutFixityManager = AboutFixity(self)
            self.AboutFixityManager.SetDesgin()
            self.AboutFixityManager.ShowDialog()

        '''
        Pop Up to Change Root Directory If any change occured
        @param orignalPathText: Path In Manifest
        @param changePathText: New Path Given in Fixity Tool
        
        '''

        def ChangeRootDirectoryInfor(self,orignalPathText, changePathText, code):
            self.FileChanged.DestroyEveryThing()
            self.FileChanged = None
            CodeOfDirectory =  str(code).split('-')
            
            
            self.FileChanged = FileChanged(self,orignalPathText, changePathText, int(CodeOfDirectory[1]))
            self.FileChanged.SetDesgin()
            self.FileChanged.ShowDialog()
            self.setWindowTitle("Fixity "+self.versoin)

        ''' Pop up to set Filters '''
        def FilterFilesBox(self):
            self.FilterFiles.Cancel()
            self.FilterFiles = None
            self.FilterFiles = FilterFiles(self)
            self.FilterFiles.SetDesgin()
            self.FilterFiles.ShowDialog()

        ''' Pop up to Change Project Name '''
        def ChangeNameBox(self):

            self.ChangeName.Cancel()
            self.ChangeName = None
            self.ChangeName = ChangeName(self)
            self.ChangeName.SetDesgin()
            self.ChangeName.ShowDialog()

            if self.changedNameIndex is not  None:
                try:
                    self.projects.item(int(self.changedNameIndex)).setSelected(True)
                    self.projects.setCurrentRow(int(self.changedNameIndex))
                    self.unsaved = False

                    self.update(self.changedNameName)
                    self.unsaved = True
                    self.updateschedule()
                    self.unsaved = False
                except Exception as Excep:
                    print(Excep[0])


        ''' Pop up to set Encryption Method. '''
        def DecryptionManagerBox(self):
            self.DecryptionManager.Cancel()
            self.DecryptionManager = None
            self.DecryptionManager = DecryptionManager(self)
            self.DecryptionManager.SetDesgin()
            self.DecryptionManager.ShowDialog()


        ''' Trigger to switch debugger on or off '''
        def switchDebugger(self,start= None):
            SqlLiteDataBase = Database()
            Information = {'debugger':0}
            info = SqlLiteDataBase.getConfiguration()
            if info is not None:
                if(len(info)>0):
                    Information = info[0]

            debugText = ''
            if start is None:
                if info is not  None:
                    if len(info) < 0:
                            Information['debugger'] = 1
                    elif Information['debugger'] == 0 or Information['debugger'] == '' or Information['debugger'] is None:
                        Information['debugger'] = 1
                    else:
                        Information['debugger'] = 0

                    if info is not  None:
                        if len(info) > 0:
                            SqlLiteDataBase.update(SqlLiteDataBase._tableConfiguration,Information,"id = '"+str(Information['id'])+"'")
                        else:
                            SqlLiteDataBase.insert(SqlLiteDataBase._tableConfiguration,Information)

            if Information['debugger'] == 0 or Information['debugger'] == '' or Information['debugger'] is None:
                debugText = 'Turn Debugging On'
            else:
                debugText = 'Turn Debugging Off'

            self.Debuging.setText(debugText)


        ''' Create New Fixity Again '''
        def newWindow(self):
            self = ProjectWin()
            self.show()
            sys.exit(app.exec_())


        '''
        
        Gets Detail information of Windows
        @return: tuple Windows Information
        
        '''
        def getWindowsInformation(self):
            WindowsInformation = {}
            try:
                major , minor , build , platformType , servicePack = sys.getwindowsversion()

                WindowsInformation['major'] = major
                WindowsInformation['minor'] = minor
                WindowsInformation['build'] = build

                WindowsInformation['platformType'] = platformType
                WindowsInformation['servicePack'] = servicePack
                windowDetailedName = platform.platform()
                WindowsInformation['platform'] = windowDetailedName
                windowDetailedName = str(windowDetailedName).split('-')

                if(windowDetailedName[0] is not  None and (str(windowDetailedName[0]) == 'Windows' or str(windowDetailedName[0]) == 'windows')):
                    WindowsInformation['isWindows'] =True
                else:
                    WindowsInformation['isWindows'] =False

                if(windowDetailedName[1] is not None and (str(windowDetailedName[1]) != '')):
                    WindowsInformation['WindowsType'] =str(windowDetailedName[1])
                else:
                    WindowsInformation['WindowsType'] =None

                WindowsInformation['ProcessorInfo'] = platform.processor()

                try:
                    os.environ["PROGRAMFILES(X86)"]
                    bits = 64
                except:
                    bits = 32

                WindowsInformation['bitType'] = "Win{0}".format(bits)
            except Exception as Excep:
                Debuging = Debuger()
                moreInformation = {"moreInfo":'null'}
                try:
                    if not Excep[0] is None:
                        moreInformation['LogsMore'] =str(Excep[0])
                except:
                    pass
                try:
                    if not Excep[1] is None:
                        moreInformation['LogsMore1'] =str(Excep[1])
                except:
                    pass

                Debuging.tureDebugerOn()
                Debuging.logError('Could Not get Windows Information Line range 220 - 240 File Fixity ', moreInformation)
                pass
            return WindowsInformation



        '''
        Updates Fields When Project Is Selected In List
        @Slot(str)
        @param new: Is New Project
        @param projetName: projet Name If Not Selected 
        
        '''
        def update(self, new, projetNameForce = None):

            if self.unsaved:
                    sbox = QMessageBox()
                    sbox.setText("There are unsaved changes to this project.")
                    sbox.setInformativeText("These will be discarded when opening a new project.\nWould you like to stay on this project?")
                    sbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Discard)
                    sbox.setDefaultButton(QMessageBox.Ok)
                    sval = sbox.exec_()
                    if sval == QMessageBox.Ok:
                            self.projects.setCurrentRow(self.projects.indexFromItem(self.old).row())
                            return
                        
            for n in range(0,7):
                self.dtx[(n)].setText("")
                self.mtx[(n)].setText("")
                
            self.runOnlyOnACPower.setChecked(False)
            self.StartWhenAvailable.setChecked(False)
            self.EmailOnlyWhenSomethingChanged.setChecked(False)

            if projetNameForce is None: 
                projectName = self.projects.currentItem().text()
            else:
                projectName = projetNameForce

            projectInfo = self.Database.getProjectInfo(projectName)
            
            pathInfo = self.Database.getProjectPathInfo(projectInfo[0]['id'] , projectInfo[0]['versionCurrentID'])
            emails = str(projectInfo[0]['emailAddress'])
            emails = emails.split(',')
            rlabel = projectInfo[0]['lastRan']
            
            countEmail = 0
            for email in emails:
                try:
                    self.mtx[(countEmail)].setText(str(email).strip())
                except:
                    pass
                countEmail = countEmail + 1
                
                
            n = 0
            for n in pathInfo:
                if n is not  None :
                    try:
                        self.dtx[(n)].setText(str(pathInfo[(n)]['path']).strip())
                    except:
                        self.dtx[(n)].setText("")


            for n in pathInfo:
                if n is not  None :
                    try:
                        self.dtx[(n)].setText(str(pathInfo[(n)]['path']).strip())
                    except:
                        self.dtx[(n)].setText("")
                        
            if int(projectInfo[0]['emailOnlyUponWarning']) == 1:
                self.EmailOnlyWhenSomethingChanged.setChecked(True)
            elif  int(projectInfo[0]['emailOnlyUponWarning']) == 0:
                self.EmailOnlyWhenSomethingChanged.setChecked(False)


            if  int(projectInfo[0]['runWhenOnBattery']) == 1:
                self.runOnlyOnACPower.setChecked(True)
            elif  int(projectInfo[0]['runWhenOnBattery']) == 0:
                self.runOnlyOnACPower.setChecked(False)

            if  int(projectInfo[0]['ifMissedRunUponRestart']) == 1:
                self.StartWhenAvailable.setChecked(True)
            elif  int(projectInfo[0]['ifMissedRunUponRestart']) == 0:
                self.StartWhenAvailable.setChecked(False)


            if str(projectInfo[0]['durationType']) == '1':
                    self.monthly.setChecked(True)
                    self.monthclick()
                    try:
                        self.dom.setValue(int(projectInfo[0]['runDayOrMonth']))
                    except Exception as Excep:
                        print(Excep)
                        pass
                    
            elif str(projectInfo[0]['durationType']) == '2':
                    self.weekly.setChecked(True)
                    self.weekclick()
                    self.dow.setCurrentIndex(int(projectInfo[0]['runDayOrMonth']))
                    
            elif str(projectInfo[0]['durationType']) == '3':
                    self.daily.setChecked(True)
                    self.dayclick()
            try:
                    t = str(projectInfo[0]['runTime']).split(':')
            except:
                    t = ['00', '00']

            self.timer.setTime(QTime(int(t[0]), int(t[1])))
            self.lastrun.setText("Last checked:\n" + rlabel)
            self.unsaved = False
            self.old = new



        '''
        New Project Creation
        '''
        def new(self):
            if self.unsaved:
                QMessageBox.warning(self, "Fixity", "Can not create New Project.Please save other unsaved Projects and try again.")
                return
            
            
            QID = QInputDialog(self)
            QID.setWindowModality(Qt.WindowModal)
            name = QID.getText(self, "Project Name", "Name for new Fixity project:", text="New_Project")
            
            if not name[1]:
                return
            
            IsProjectNameValid = self.ValidateProjectName(str(name[0]))
            
            if IsProjectNameValid is not None:
                QMessageBox.warning(self, "Fixity", str(IsProjectNameValid))
                return
            
            projectInfo =  self.Database.getProjectInfo(name[0])

            if len(projectInfo) > 0:
                QMessageBox.warning(self, "Fixity", "Invalid project name:\n*Project names must be unique\n*Project names cannot be blank\n*Project names cannot contain spaces\n*Project names must be legal filenames")
                return

            newitem = QListWidgetItem(name[0], self.projects)
            self.projects.setCurrentItem(newitem)
            self.monthly.setChecked(True)
            self.monthclick()
            self.dom.setValue(1)
            self.timer.setTime(QTime(0, 0))
            for SingleRangeValue  in xrange(0, 7):
                self.dtx[SingleRangeValue].setText("")
                self.mtx[SingleRangeValue].setText("")

            self.old = newitem
            self.toggler(False)
            self.unsaved = True

        '''
        Process the changes made in Fixity
        @return:  List-List Of Changed Paths
        '''
        def process(self, shouldRun=True):

            if all(d.text() == "" for d in self.dtx):
                    QMessageBox.warning(self, "Fixity", "No directories selected!\nPlease set directories to scan")
                    return
            dmonth, dweek = 99, 99
            if self.monthly.isChecked():
                    interval = 1
                    dmonth = int(self.dom.value())
            elif self.weekly.isChecked():
                    interval = 2
                    dweek = int(self.dow.currentIndex())
            elif self.daily.isChecked():
                    interval = 3
            else:
                    QMessageBox.warning(self, "Fixity", "Project schedule not set - please select an interval for scans")
                    return

            for ms in self.mtx:
                    SingleEmail = ms.text().strip()
                    if  SingleEmail != "":
                        errorMsg = self.EmailPrefManager.ValidateEmail(SingleEmail)
                        if not str(errorMsg).strip() == 'None':
                            QB = QMessageBox()
                            errorMsg = QB.information(self, "Error", errorMsg)
                            return

            isfileExists = False
            if path.isfile('projects\\' + self.projects.currentItem().text() + '.fxy'):
                isfileExists = True

            if isfileExists:
                projFile = open('projects\\' + self.projects.currentItem().text() + '.fxy', 'rb')
                projFileText = projFile.readlines()
                projFile.close()

                if not projFileText :
                    isfileExists = False

            if shouldRun or (not isfileExists):

                total = 0
                directoryIncreament = 1

                pathsInfoChanges = {}
                dontSave = False
                for ds in self.dtx:

                    if ds.text().strip() != "":
                        
                        self.checkForChanges(self.projects.currentItem().text(),ds.text(), 'Fixity-'+str(directoryIncreament))
                        orignalPathTextCode = FixityCore.pathCodeEncode(directoryIncreament)
                        changePathTextCode = FixityCore.pathCodeEncode(directoryIncreament)

                        CodeOfPath = ''
                        try:
                            self.FileChanged.changeThePathInformation
                        except:
                            self.FileChanged = FileChanged(self)
                            
                        FlagIsPathChanged = False 
                        if not self.FileChanged.changeThePathInformation:
                            if self.FileChanged.Code == directoryIncreament:
                                CodeOfPath = FixityCore.pathCodeEncode(directoryIncreament)
                                pathToSaveInManifest = str(str(self.FileChanged.orignalPathText))
                                pathsInfoChanges[directoryIncreament] =  str(str(self.FileChanged.orignalPathText))
                                FlagIsPathChanged = True
                            else:
                                FlagIsPathChanged = False 
                        
                        if not FlagIsPathChanged: 
                            CodeOfPath = FixityCore.pathCodeEncode(directoryIncreament)
                            pathToSaveInManifest = str(ds.text())
                            pathsInfoChanges[directoryIncreament]=str(ds.text())

                        if(pathToSaveInManifest ==''):
                            pathToSaveInManifest = str(ds.text())
                            if(str(ds.text()) != ''):
                                pathsInfoChanges[directoryIncreament] =  str(ds.text())
                            else:
                                pathsInfoChanges[directoryIncreament] =  str(self.FileChanged.orignalPathText)
                            CodeOfPath = FixityCore.pathCodeEncode(directoryIncreament)

                        if self.FileChanged.changeThePathInformation:
                            self.FileChanged.ReplacementArray[directoryIncreament]= {'orignalpath':self.FileChanged.orignalPathText ,'newPath': self.FileChanged.changePathText,  'orignal':orignalPathTextCode , 'new':changePathTextCode}

                        directoryIncreament = directoryIncreament + 1

                currentProject = self.projects.currentItem().text()

                projectInformation = {}
                projectInformation['title'] = self.projects.currentItem().text()

                projectInformation['runTime'] = self.timer.time().toString()

                if(dmonth == 99 and dweek == 99):
                    durationType = 2
                    
                elif (dmonth == 99 and dweek != 99):
                    durationType = 1
                    
                elif(dmonth != 99 and dweek == 99):
                    durationType = 0

                projectInformation['durationType'] = durationType
                projectInformation['runDayOrMonth'] = interval
                projectInformation['selectedAlgo'] = 'sha256'
                projectInformation['filters'] = ''
                if(self.runOnlyOnACPower.isChecked()):
                    projectInformation['runWhenOnBattery'] = 1
                else:
                    projectInformation['runWhenOnBattery'] = 0

                if(self.StartWhenAvailable.isChecked()):
                    projectInformation['ifMissedRunUponRestart'] = 1
                else:
                    projectInformation['ifMissedRunUponRestart'] = 0

                if(self.EmailOnlyWhenSomethingChanged.isChecked()):
                    projectInformation['emailOnlyUponWarning'] = 1
                else:
                    projectInformation['emailOnlyUponWarning'] = 0

                projectInformation['extraConf'] = ''

                data = str(datetime.datetime.now()).split('.')
                projectInformation['lastRan'] = data[0]

                Configurations = {}

                Configurations['RunWhenOnBatteryPower'] = self.runOnlyOnACPower.isChecked()
                Configurations['IfMissedRunUponAvailable'] = self.StartWhenAvailable.isChecked()
                Configurations['onlyonchange'] = self.EmailOnlyWhenSomethingChanged.isChecked()
                Configurations['RunInitialScan'] = False
                ConfigurationInfo = self.Database.getProjectInfo(currentProject)
                FiltersArray = {}

                if ConfigurationInfo:
                    if ConfigurationInfo[0]['id']:
                        Allfilters = ConfigurationInfo[0]['filters']
                        Allfilters = str(Allfilters.replace('\n', ''))
                        FiltersArray = Allfilters.split(',')

                if shouldRun:
                    for dx in self.dtx:
                        src = dx.text()
                        listOfDirectory = self.buildTable(src, 'sha256')
                        for n in xrange(len(listOfDirectory)):
                            if FiltersArray:
                                for SingleFilter in FiltersArray :
                                    if SingleFilter == '' or listOfDirectory[n][1].find(SingleFilter) < 0:
                                        total += 1
                
                if shouldRun:
                    
                    QMessageBox.information(self, "Fixity", str(total) + " files processed in project: " + self.projects.currentItem().text())
                    
                    return pathsInfoChanges
                       
                else:
                    QMessageBox.information(self, "Fixity", "Settings saved for " + self.projects.currentItem().text())
                    return pathsInfoChanges
            else :
                projfileFileText = []
                if isfileExists:
                    projfileFile = open('projects\\' + self.projects.currentItem().text() + '.fxy', 'rb')
                    projfileFileText = projfileFile.readlines()
                    projfileFile.close()

                    configurations = {}
                    configurations['directories'] = ''
                    configurations['emails'] = ''
                    configurations['timingandtype'] = ''

                    directoryIncreament = 0

                    for ds  in self.dtx:
                        directoryIncreament = directoryIncreament + 1
                        if ds.text().strip() != "":
                            self.checkForChanges(self.projects.currentItem().text(), ds.text(), directoryIncreament)
                            orignalPathTextCode = FixityCore.pathCodeEncode(directoryIncreament)
                            changePathTextCode = FixityCore.pathCodeEncode(directoryIncreament)
                            CodeOfPath = ''

                            if self.FileChanged.changeThePathInformation:
                                CodeOfPath = FixityCore.pathCodeEncode(directoryIncreament)
                                pathToSaveInManifest = str(ds.text())
                            else:
                                CodeOfPath = FixityCore.pathCodeEncode(directoryIncreament)
                                pathToSaveInManifest = str(str(self.FileChanged.orignalPathText))

                            if(pathToSaveInManifest ==''):
                                pathToSaveInManifest = str(ds.text())
                                CodeOfPath = FixityCore.pathCodeEncode(directoryIncreament)

                            if self.FileChanged.changeThePathInformation:
                                self.FileChanged.ReplacementArray[directoryIncreament]= {'orignalpath':self.FileChanged.orignalPathText ,'newPath': self.FileChanged.changePathText,  'orignal':orignalPathTextCode , 'new':changePathTextCode}

                            configurations['directories'] +=  (pathToSaveInManifest + "|-|-|" + CodeOfPath + "|-|-|" + str(directoryIncreament) + ";")

                    configurations['directories'] += "\n"

                    for ms in self.mtx:
                        if ms.text().strip() != "":
                            configurations['emails']+=str(ms.text()) +str(ms.text()) +";"

                    configurations['emails'] += "\n"
                    configurations['timingandtype'] = (str(interval) + " " + self.timer.time().toString() + " " + str(dmonth) + " " + str(dweek) + "\n")

                    projfileFileText[0] =  configurations['directories']
                    projfileFileText[1] =  configurations['emails']
                    projfileFileText[2] =  configurations['timingandtype']
                    projfile = open('projects\\' + self.projects.currentItem().text() + '.fxy', 'wb')
                    projfile.writelines(projfileFileText)
                    try:
                        projfileFile.close()

                    except:
                        pass
                    try:
                        projfile.close()

                    except:
                        pass
                    QMessageBox.information(self, "Fixity", "Settings saved for " + self.projects.currentItem().text())
            return


        '''
        Toggles all option fields on/off
        @param switch: switch could be True or False
        
        @return: None
        '''
        def toggler(self, switch):
            for n in xrange(len(self.mtx)):
                self.mtx[n].setDisabled(switch)
                self.dtx[n].setDisabled(switch)
                self.but[n].setDisabled(switch)
            self.timer.setDisabled(switch)
            self.monthly.setDisabled(switch)
            self.weekly.setDisabled(switch)
            self.daily.setDisabled(switch)
            self.timer.setDisabled(switch)
            self.dom.setDisabled(switch)
            self.dow.setDisabled(switch)
            try:
                self.runOnlyOnACPower.setDisabled(switch)
            except:
                pass
            try:
                self.StartWhenAvailable.setDisabled(switch)
            except:
                pass
            try:
                self.EmailOnlyWhenSomethingChanged.setDisabled(switch)
            except:
                pass



        '''
        turn True to anything change related to selected project
        @return:  None
        '''
        def changed(self):
                self.unsaved = True



        '''
        Day check box Click Trigger
        (Trigger on day Check box click)

        @return: None
        '''
        def dayclick(self):
            self.dom.hide()
            self.dow.hide()
            self.spacer.changeSize(30, 25)



        '''
        Month check box Click Trigger
        (Trigger on week Check box click)

        @return: None
        '''
        def weekclick(self):
            self.spacer.changeSize(0, 0)
            self.dom.hide()
            self.dow.show()




        '''
        Month check box Click Trigger
        (Trigger on Month Check box click)

        @return: None
        '''
        def monthclick(self):
            self.spacer.changeSize(0, 0)
            self.dow.hide()
            self.dom.show()



        '''
        Pick Directory
        (Trigger on Pick Directory Button Menu)

        @return: None
        '''
        def pickdir(self):
                n = self.but.index(self.sender())
                PathSelectedForthiDirectory = QFileDialog.getExistingDirectory(dir=path.expanduser('~') + '\\Desktop\\')
                if PathSelectedForthiDirectory and PathSelectedForthiDirectory !='':
                    self.dtx[n].setText(PathSelectedForthiDirectory)



        '''
        Provides Replace Path Information Array


        @return: None
        '''
        def replacePathInformation(self):
            projFileChangePath = open('projects\\' + self.projects.currentItem().text()+ 'ChangingPath' + '.fxy', 'wb')
            currentProjFile = open('projects\\' + self.projects.currentItem().text()+ '.fxy', 'rb')

            lineNumber = 1
            for line in currentProjFile:
                lineToWrite = line
                if lineNumber > 4:
                    for SingleReplace in self.FileChanged.ReplacementArray:
                        lineToWrite =line.replace(self.FileChanged.ReplacementArray[SingleReplace]['orignal'], self.FileChanged.ReplacementArray[SingleReplace]['new'])
                projFileChangePath.write(lineToWrite)
                lineNumber = lineNumber+1
            currentProjFile.close()

            projFileChangePath.close()

            shutil.copy('projects\\' + self.projects.currentItem().text()+ 'ChangingPath' + '.fxy', 'projects\\' + self.projects.currentItem().text()+ '.fxy')
            remove('projects\\' + self.projects.currentItem().text()+ 'ChangingPath' + '.fxy')



        '''
        Saves And Runs
        (Trigger on Run Menu)

        @return: None
        '''
        def run(self):
            
            if all(d.text() == "" for d in self.dtx):
                QMessageBox.warning(self, "Fixity", "No directories selected!\nPlease set directories to scan")
                return
            
            dmonth, dweek = 99, 99
            if self.monthly.isChecked():
                interval = 1
                dmonth = int(self.dom.value())
            elif self.weekly.isChecked():
                interval = 2
                dweek = int(self.dow.currentIndex())
            elif self.daily.isChecked():
                interval = 3
            else:
                QMessageBox.warning(self, "Fixity", "Project schedule not set - please select an interval for scans")
                return

            Configurations = {}

            SqlLiteDataBase = Database()
            Configurations = SqlLiteDataBase.getProjectInfo(self.projects.currentItem().text())
            if (len(Configurations)>0):
                if self.runOnlyOnACPower.isChecked():
                    Configurations[0]['runWhenOnBattery'] = 1
                else:
                    Configurations[0]['runWhenOnBattery'] = 0

                if self.StartWhenAvailable.isChecked():
                    Configurations[0]['ifMissedRunUponRestart'] = 1
                else:
                    Configurations[0]['ifMissedRunUponRestart'] = 0

                if self.EmailOnlyWhenSomethingChanged.isChecked():
                    Configurations[0]['emailOnlyUponWarning'] = 1
                else:
                    Configurations[0]['emailOnlyUponWarning'] = 0
                pathsInfoChanges = {}
                directoryIncreamentDirs = 1
                for ds in self.dtx:
                    pathsInfoChanges[directoryIncreamentDirs]=str(ds.text())
                    directoryIncreamentDirs = directoryIncreamentDirs + 1

                FilePath = getcwd()+'\\schedules\\'

                FixitySchtask.schedule(interval, dweek, dmonth, self.timer.time().toString(), self.projects.currentItem().text(), Configurations[0],self.SystemInformation, pathsInfoChanges)

                FileName = 'AutoFixity.exe'
                params = self.projects.currentItem().text() +' '+'Run'

                self.Threading = Threading(self.projects.currentItem().text(), self.projects.currentItem().text(), 1,FileName,FilePath , params)

                self.Threading.start()
                QMessageBox.information(self, "Fixity", "Run Now for "+self.projects.currentItem().text() + " has successfully started.")
                
            else:
                QMessageBox.information(self, "Fixity", "Project Configuration Not Found,Please Save the project and Try Again")



        '''
        DELETE Given PROJECT
        (Trigger on Delete Menu)

        @return: None
        '''
        def deleteproject(self):
            sbox = QMessageBox()
            try:
                sbox.setText("Are you certain that you want to delete " + self.projects.currentItem().text() + "?")
            except:
                QMessageBox.information(self, "Fixity", "No project selected for deletion!")
                return
            sbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            sbox.setDefaultButton(QMessageBox.Cancel)
            sval = sbox.exec_()
            if sval == QMessageBox.Cancel:
                return
            try:
                SqlLiteDataBase = Database()
                projInfo = SqlLiteDataBase.getProjectInfo(self.projects.currentItem().text())

                if len(projInfo) > 0:

                    SqlLiteDataBase.delete(SqlLiteDataBase._tableVersionDetail, "`projectID` = '"+str(projInfo[0]['id'])+"'")
                    SqlLiteDataBase.delete(SqlLiteDataBase._tableProjectPath, "`projectID` = '"+str(projInfo[0]['id'])+"'")
                    SqlLiteDataBase.delete(SqlLiteDataBase._tableVersions, "`id` = '"+str(projInfo[0]['versionCurrentID'])+"'")
                    SqlLiteDataBase.delete(SqlLiteDataBase._tableProject, "title like '"+self.projects.currentItem().text()+"'")
            except:
                pass

            FixitySchtask.deltask(self.projects.currentItem().text())
            self.projects.takeItem(self.projects.row(self.projects.currentItem()))
            self.unsaved = False

            try:
                    self.update(self.projects.selectedItems()[0])
            except:
                    for SingleRangeValue in xrange(0, 7):
                            self.dtx[SingleRangeValue].setText("")
                            self.mtx[SingleRangeValue].setText("")
                    self.monthly.setChecked(True)
                    self.monthclick()
                    self.timer.setTime(QTime(0, 0))
                    self.lastrun.setText("Last checked:")
            self.toggler((self.projects.count() == 0))
            self.unsaved = False



        '''
        Fetch All Directory with in this directory
        
        @return:  ListOfPaths in given Directory
        '''
        def buildTable(self, r, a):

            list = []
            fls = []
            progress = QProgressDialog()
            progress.setMaximum(100)
            progress.setMinimumDuration(0)
            for root, subFolders, files in walk(r):
                    for file in files:
                            fls.append(path.join(root, file))

            for f in xrange(len(fls)):
                    txt = path.abspath(fls[f])
                    if len(txt) > 43:
                            txt = txt[:20] + '...' + txt[-20:]
                    progress.setLabelText(txt.ljust(43))
                    p = path.abspath(fls[f])
                    if(OS_Info == 'Windows'):
                        h = FixityCore.fixity(p, a)
                    else:
                        h = FixityCore.fixity(p, a)

                    if(OS_Info == 'Windows'):
                        i = FixityCore.FixityCoreWin.ntfsIDForWindows(p)
                    else:
                        i = FixityCore.FixityCoreMac.ntfsIDForMac(p)

                    list.append((h, p, i))
                    progress.setValue(100 * float(f) / len(fls))
                    qApp.processEvents()
            progress.close()

            return list



        '''
        Update Schedule information

        @return: None
        '''
        def updateschedule(self,customPojectUpdate = None):

            flagInitialScanUponSaving = False
            isRcipentEmailAddressSet = False
            allEmailAddres = ''
            for ms in self.mtx:
                    SingleEmail = ms.text().strip()
                    if  SingleEmail != "":
                        allEmailAddres = allEmailAddres + str(SingleEmail) +','
                        isRcipentEmailAddressSet = True
                        errorMsg = self.EmailPrefManager.ValidateEmail(SingleEmail)
                        if not str(errorMsg).strip() == 'None':
                            QB = QMessageBox()
                            errorMsg = QB.information(self, "Error", errorMsg)
                            return

            if isRcipentEmailAddressSet:
                EmailInfo = self.EmailPrefManager.getConfigInfo()
                if len(EmailInfo) <= 0:
                    QMessageBox.information(self, "Email Validation", 'Please configure an email account in the Preferences menu')
                    return
            try:
                pathsInfoChanges = self.process(flagInitialScanUponSaving)
            except:
                pathsInfoChanges = {}
            dmonth, dweek = 99, 99
            
            
            if self.monthly.isChecked():
                    interval = 1
                    dmonth = int(self.dom.value())
            elif self.weekly.isChecked():
                    interval = 2
                    dweek = int(self.dow.currentIndex())
            elif self.daily.isChecked():
                    interval = 3


            projectInformation = {}
            projectInformation['title'] = self.projects.currentItem().text()
            projectInformation['durationType'] = interval
            projectInformation['runTime'] = self.timer.time().toString()

            runDayOrMonth = '2'

            if(dmonth == 99 and dweek == 99):
                runDayOrMonth = ''
            elif (dmonth == 99 and dweek != 99):
                runDayOrMonth = self.dow.currentIndex()

            elif(dmonth != 99 and dweek == 99):
                runDayOrMonth = self.dom.value()
            projectInformation['emailAddress'] = allEmailAddres
            projectInformation['runDayOrMonth'] = runDayOrMonth
            projectInformation['selectedAlgo'] = 'sha256'
            projectInformation['filters'] = ''

            if(self.runOnlyOnACPower.isChecked()):
                projectInformation['runWhenOnBattery'] = 1
            else:
                projectInformation['runWhenOnBattery'] = 0

            if(self.StartWhenAvailable.isChecked()):
                projectInformation['ifMissedRunUponRestart'] = 1
            else:
                projectInformation['ifMissedRunUponRestart'] = 0

            if(self.EmailOnlyWhenSomethingChanged.isChecked()):
                projectInformation['emailOnlyUponWarning'] = 1
            else:
                projectInformation['emailOnlyUponWarning'] = 0

            projectInformation['extraConf'] = ''
            data = str(datetime.datetime.now()).split('.')
            projectInformation['lastRan'] = data[0]
            
            Configurations = {}
            Configurations = self.EmailPrefManager.getConfigInfo(self.projects.currentItem().text())
            Configurations['RunWhenOnBatteryPower'] = self.runOnlyOnACPower.isChecked()
            Configurations['IfMissedRunUponAvailable'] = self.StartWhenAvailable.isChecked()
            Configurations['onlyonchange'] = self.EmailOnlyWhenSomethingChanged.isChecked()
            Configurations['RunInitialScan'] = False
            self.unsaved = False

            FixitySchtask.schedule(interval, dweek, dmonth, self.timer.time().toString(), self.projects.currentItem().text() , projectInformation,self.SystemInformation , pathsInfoChanges)
            self.unsaved = False



        '''
        Remove the file which are not required

        @return: None
        '''
        def removeNotRequiredFiles(self):

            if not str(self.projects.currentItem()) == 'None':
                if path.isfile('projects\\' + self.projects.currentItem().text() + '.fxy') and path.isfile('bin\\' + self.projects.currentItem().text() + '-conf.txt'):
                    projectFile = open('projects\\' + self.projects.currentItem().text() + '.fxy', 'rb')
                    binFile = open('bin\\' + self.projects.currentItem().text() + '-conf.txt', 'rb')
                    projectFileLines = projectFile.readlines()
                    binFileLines = binFile.readlines()
                    projectFile.close()

                    binFile.close()

                    if (not binFileLines) or (not projectFileLines):
                        remove('projects\\' + self.projects.currentItem().text() + '.fxy')
                        remove('bin\\' + self.projects.currentItem().text() + '-conf.txt')
            return



        '''
        Window close Event

        @return: None
        '''
        def closeEvent(self, event):
            if not str(self.projects.currentItem()) == 'None':
                if path.isfile('projects\\' + self.projects.currentItem().text() + '.fxy') and path.isfile('bin\\' + self.projects.currentItem().text() + '-conf.txt'):
                    projectFile = open('projects\\' + self.projects.currentItem().text() + '.fxy', 'rb')
                    binFile = open('bin\\' + self.projects.currentItem().text() + '-conf.txt', 'rb')
                    projectFileLines = projectFile.readlines()
                    binFileLines = binFile.readlines()
                    if (not binFileLines) or (not projectFileLines):
                        self.unsaved = True
                    projectFile.close()

                    binFile.close()


            if self.unsaved:
                    sbox = QMessageBox()
                    sbox.setText("There are unsaved changes to this project.")
                    sbox.setInformativeText("These will be discarded when opening a new project.\nWould you like to stay on this project?")
                    sbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Discard)
                    sbox.setDefaultButton(QMessageBox.Ok)
                    sval = sbox.exec_()

                    if sval == QMessageBox.Ok:
                        event.ignore()
                    else:
                        self.removeNotRequiredFiles()
                        event.accept()


        '''
        Check For Changes In the provided base  path and old given base path the given project name
        @param projectName: Project Name
        @param searchForPath: Path of a given base Dire
        @param code: Code of that specific path

        @return: None
        '''
        def checkForChanges(self,projectName , searchForPath ,code):
            try:
                SqlLiteDataBase = Database()
                info = SqlLiteDataBase.getProjectInfo(projectName)
                information = info[0]
                DirectoryDetail = SqlLiteDataBase.getProjectPathInfo(information['id'], information['versionCurrentID'])
                for  DirectoryDetailSingle in DirectoryDetail:
                    if (str(DirectoryDetail[DirectoryDetailSingle]['pathID']).strip() == str(code).strip()):
                        if(DirectoryDetail[DirectoryDetailSingle]['path'] != searchForPath):
                            
                            self.ChangeRootDirectoryInfor(DirectoryDetail[DirectoryDetailSingle]['path'] ,searchForPath, code )
            except:
                pass



        '''
        Get Project Index in projects listing of a given name

        @param projectName: Project Name
        @return: index
        '''
        def getProjectIndex(self,projectName):

            for index in xrange(self.projects.count()):
                if projectName in str(self.projects.item(index).text()):
                    return index


        '''
        Create All Required File And Directories For Windows

        @return: None
        '''
        def CreateAllRequiredFileAndDirectoriesForWindows(self):

            FixityResourcesBasePath = getcwd()
            ''' Create bin Folder '''
            try:
                self.createDirectory(str(FixityResourcesBasePath)+str(os.sep)+'bin')
            except:
                pass


            DatabasePath = FixityResourcesBasePath+str(os.sep)+'bin'+str(os.sep)+'Fixity.db'
            ''' Create Database File '''
            self.CreateDatabaseFile(DatabasePath)



            ''' Create history Folder '''
            try:
                self.createDirectory(str(FixityResourcesBasePath)+str(os.sep)+'history')
            except:
                pass



            ''' Create history Folder '''
            try:
                self.createDirectory(str(FixityResourcesBasePath)+str(os.sep)+'reports')
            except:
                pass



            ''' Create schedules Folder '''
            try:
                self.createDirectory(str(FixityResourcesBasePath)+str(os.sep)+'schedules')
            except:
                pass


            ''' Create debug Folder '''
            try:
                self.createDirectory(str(FixityResourcesBasePath)+str(os.sep)+'debug')
            except:
                pass



        '''
        Create All Required File And Directories For Mac

        @return: None
        '''
        def CreateAllRequiredFileAndDirectoriesForMac(self):
            FixityResourcesBasePath = getcwd()

            pathInfo = str(getcwd()).replace(str(os.sep)+'Contents'+str(os.sep)+'Resources','')
            pathInfo = str(pathInfo).replace('Fixity.app'+str(os.sep), '')
            pathInfo = str(pathInfo).replace('Fixity.app', '')
            DatabasePath = FixityResourcesBasePath+str(os.sep)+'bin'+str(os.sep)+'Fixity.db'


            ''' Create Database File '''
            self.CreateDatabaseFile(DatabasePath)

            ''' Create Schedules Folder '''
            schedulesPathOfFixiry = FixityResourcesBasePath+'schedules'

            try:
                self.createDirectory(schedulesPathOfFixiry)
            except:
                pass


            ''' Create Bin Folder '''
            try:
                self.createDirectory(str(FixityResourcesBasePath)+'bin')
            except:
                pass


            FixityPublicBasePath = str(pathInfo).replace(' ', '\\ ')

            ''' Create History Folder '''
            print(str(FixityPublicBasePath)+'history')
            try:
                self.createDirectory(str(FixityPublicBasePath)+'history')
            except Exception as exp:
                print(exp[0])
                pass


            ''' Create reports Folder '''
            print(str(FixityPublicBasePath)+'reports')
            try:
                self.createDirectory(str(FixityPublicBasePath)+'reports')
            except Exception as exp:
                print(exp[0])
                pass


        '''
        Create Directory given in the path if dose not exists
        @param directoryPath: Directory Path to be created

        @return: None
        '''
        def createDirectory(self,directoryPath):
            if  not os.path.isdir(str(directoryPath)) :
                try:
                    os.mkdir(str(directoryPath))
                except:
                    pass
                
                
        '''
        Create Database File that Fixity Uses
        @param DatabasePath:Database File Path To be created

        @return: None
        '''
        def CreateDatabaseFile(self,DatabasePath):
            if DatabasePath:
                if not os.path.isfile(DatabasePath):
                    try:
                        DatabaseFile = open(str(DatabasePath), 'w+')
                        DatabaseFile.close()
                    except:
                        pass

        ''' 
        create Database Tables
        @return:  None 
        '''
        def createDatabaseTables(self):

                try:
                    self.Database
                except:
                    self.Database = Database()
                    pass



                if not self.checkIfTableExistsInDatabase('configuration'):
                    ''' Create Configuration Table'''
                    try:
                        self.Database.sqlQuery('CREATE TABLE "configuration" ( id INTEGER NOT NULL,  smtp TEXT,  email TEXT,  pass TEXT,  port INTEGER,  protocol TEXT,  debugger SMALLINT,  "updatedAt" DATETIME,  "createdAt" DATETIME,  PRIMARY KEY (id) );')
                    except:
                        pass


                if not self.checkIfTableExistsInDatabase('project'):
                    ''' Create Project Table'''
                    try:
                        self.Database.sqlQuery('CREATE TABLE "project" (ignoreHiddenFiles NUMERIC, id INTEGER PRIMARY KEY, versionCurrentID INTEGER, title VARCHAR(255), durationType INTEGER, runTime TEXT(10), runDayOrMonth VARCHAR(12),selectedAlgo VARCHAR(8),filters TEXT, runWhenOnBattery SMALLINT, ifMissedRunUponRestart SMALLINT, emailOnlyUponWarning SMALLINT, emailAddress TEXT,extraConf TEXT, lastRan DATETIME, updatedAt DATETIME, createdAt DATETIME);')
                    except:
                        pass



                if not self.checkIfTableExistsInDatabase('projectPath'):
                    ''' Create ProjectPath Table'''
                    try:
                        self.Database.sqlQuery('CREATE TABLE "projectPath" ( id INTEGER NOT NULL,  "projectID" INTEGER NOT NULL,  "versionID" INTEGER,  path TEXT NOT NULL,  "pathID" VARCHAR(15) NOT NULL,  "updatedAt" DATETIME,"createdAt"DATETIME, PRIMARY KEY (id), FOREIGN KEY("projectID") REFERENCES project (id), FOREIGN KEY("versionID") REFERENCES versions (id));')
                    except:
                        pass


                if not self.checkIfTableExistsInDatabase('versionDetail'):
                    ''' Create VersionDetail Table'''
                    try:
                        self.Database.sqlQuery('CREATE TABLE "versionDetail" (id INTEGER NOT NULL, "versionID" INTEGER NOT NULL, "projectID" INTEGER NOT NULL, "projectPathID" INTEGER NOT NULL, "hashes" TEXT NOT NULL , "path" TEXT NOT NULL, inode TEXT NOT NULL, "updatedAt" DATETIME, "createdAt" DATETIME, PRIMARY KEY (id), FOREIGN KEY("versionID") REFERENCES versions (id), FOREIGN KEY("projectID") REFERENCES project (id), FOREIGN KEY("projectPathID") REFERENCES "projectPath" (id));')
                    except:
                        pass


                if not self.checkIfTableExistsInDatabase('versions'):
                    ''' Create Versions Table'''
                    try:
                        self.Database.sqlQuery('CREATE TABLE "versions" (id INTEGER NOT NULL, "versionType" VARCHAR(10) NOT NULL, name VARCHAR(255) NOT NULL, "updatedAt" DATETIME, "createdAt" DATETIME, PRIMARY KEY (id));')
                    except:
                        pass


        '''
            Check If Table Exists In Database
            @param tableName: Table Name

            @return List-list Of Result If Found Some
        '''
        def checkIfTableExistsInDatabase(self, tableName):
            return self.Database.getOne("SELECT * FROM sqlite_master WHERE name ='" + tableName + "'");
        
        
        ''' 
            Validate given email address
            @param Email: Email Address
           
            @return: String Message of failure
        ''' 
        def ValidateProjectName(self, projectName):
            if not re.match(r"^[a-zA-Z0-9-_]+$", projectName):
                msgProjectNameValidation = "Invalid Project Name provided.  Please provide a valid project Name and try again."
                return msgProjectNameValidation
            return None
            
'''
Auto Scan running handler
'''
def auto_run(project):
    AR = AutoRuner()
    IsemailSet = ''
    AR.runAutoFix(project , IsemailSet)

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-a', '--autorun')
        args = parser.parse_args()
    except:
        pass
    ''' If Received argument (project name and run command), it with run the scheduler other wise it will open Fixity Front end View)'''
    if(args.autorun == None or args.autorun == ''):
        app = QApplication(sys.argv)
        app.MainFixityWindow = ProjectWin(EmailPref , FilterFiles)

        app.connect(app, SIGNAL('quit()'), app.MainFixityWindow.cleanObjects)
        app.connect(app, SIGNAL('destroyed()'), app.MainFixityWindow.cleanObjects)
        app.MainFixityWindow.show()

        sys.exit(app.exec_())

    else:
        try:
            print('Scanning is in progress!........')
            auto_run(args.autorun)
            sys.exit()
        except:
            print("Could not run this Project ")