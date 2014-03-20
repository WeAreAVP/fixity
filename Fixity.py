# Fixity GUI
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0


#Bultin Libraries
from PySide.QtCore import *
from PySide.QtGui import *
from os import path, listdir, remove, walk , getcwd  , spawnl , system
from collections import deque
from genericpath import exists
import re
import datetime
import shutil
import sys
import platform
import os

#Custom Libraries
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

class ProjectWin(QMainWindow):
        def __init__(self, EmailPref , FilterFiles):
                self.Database = Database()
                QMainWindow.__init__(self)
                Debuggin = Debuger()
                Debuggin.tureDebugerOn()
                Debuggin.logInfo('Logger started!::::::::::::::::::' + "\n" ,{} )

                self.SystemInformation = self.getWindowsInformation()
                if(self.SystemInformation):
                    Debuggin.logInfo('System Information' + "\n" ,{})
                    Debuggin.logInfo('platform = '+str(self.SystemInformation['platform'])  , {} )
                    Debuggin.logInfo('major = '+ str(self.SystemInformation['major']) , {} )
                    Debuggin.logInfo('minor = '+str(self.SystemInformation['minor'])  , {} )
                    Debuggin.logInfo('build = '+str(self.SystemInformation['build'])  , {} )
                    Debuggin.logInfo('platformType = '+str(self.SystemInformation['platformType'])  , {} )
                    Debuggin.logInfo('isWindows = '+str(self.SystemInformation['isWindows'])  , {} )
                    Debuggin.logInfo('WindowsType = '+str(self.SystemInformation['WindowsType'])  , {} )
                    Debuggin.logInfo('bitType = '+str(self.SystemInformation['bitType'])  , {} )

                self.EP = EmailPref()
                self.EP.setVersion('0.3')
                self.DecryptionManager = DecryptionManager()
                self.FileChanged = FileChanged()
                self.ImportProjects = ImportProjects()
                self.FileChanged.setVersion('0.3')

                self.FilterFiles = FilterFiles()
                self.Threading = Threading

                self.setWindowIcon(QIcon(path.join(getcwd(), 'images\\logo_sign_small.png')))
                versoin = self.EP.getVersion()
                self.setWindowTitle("Fixity "+versoin);
                self.unsaved = False
                menubar = self.menuBar()
                self.f = menubar.addMenu('&File')
                self.Preferences = menubar.addMenu('&Preferences')
                newp = QAction('&New Project', self)

                save = QAction('&Run Now', self)
                usch = QAction('&Save Settings', self)
                dlte = QAction('&Delete Project', self)
                configemail = QAction('&Configure Sender Email', self)
                quit = QAction('&Quit Fixity', self)

                FilterFilesMane = QAction('&Filter Files', self)
                DecryptionManagerMenu = QAction('&Select Checksum Algorithm', self)

                self.Debuging = QAction('&Turn Debugging Off', self)
                self.ImportProjectfxy = QAction('&Import Project', self)
                self.switchDebugger('start')

                self.f.addAction(newp)
                self.f.addAction(usch)
                self.f.addAction(save)
                self.f.addAction(dlte)
                self.f.addAction(quit)

                self.Preferences.addAction(FilterFilesMane)
                self.Preferences.addAction(configemail)
                self.Preferences.addAction(self.Debuging)
                self.Preferences.addAction(DecryptionManagerMenu)
                self.Preferences.addAction(self.ImportProjectfxy)

                dlte.triggered.connect(self.deleteproject)
                newp.triggered.connect(self.new)
                configemail.triggered.connect(self.ConfigEmailView)
                save.triggered.connect(self.run)
                usch.triggered.connect(self.updateschedule)
                quit.triggered.connect(self.close)

                FilterFilesMane.triggered.connect(self.FilterFilesBox)
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
                if allProjects != None:
                    if(len(allProjects) > 0):
                        for p in allProjects:
                            projectLists.append(str(allProjects[p]['title']))

                if projectLists != None:
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
                    self.but[n].setFixedSize(30, 20)
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

                self.unsaved = False
                self.toggler((self.projects.count() == 0))
                self.show()

        # Configure Email Address for the Tools
        def ConfigEmailView(self):
            self.EP.CloseClick()
            self.EP = None
            self.EP = EmailPref()
            self.EP.SetDesgin()
            self.EP.ShowDialog()

        # Pop Up to Change Root Directory If any change occured
        # orignalPathText:: Path In Manifest
        # changePathText:: New Path Given in Fixity Tool
        def ChangeRootDirectoryInfor(self,orignalPathText,changePathText):

            self.FileChanged.DestroyEveryThing()
            self.FileChanged = None
            self.FileChanged = FileChanged(orignalPathText,changePathText)
            self.FileChanged.SetDesgin()
            self.FileChanged.ShowDialog()

        # Pop up to set Filters
        def FilterFilesBox(self):
            self.FilterFiles.Cancel()
            self.FilterFiles = None
            self.FilterFiles = FilterFiles()
            self.FilterFiles.SetDesgin()
            self.FilterFiles.ShowDialog()

        # Pop up to set Filters
        def DecryptionManagerBox(self):
            self.DecryptionManager.Cancel()
            self.DecryptionManager = None
            self.DecryptionManager = DecryptionManager()
            self.DecryptionManager.SetDesgin()
            self.DecryptionManager.ShowDialog()

        def switchDebugger(self,start= None):
            DB = Database()
            Information = {'debugger':0}
            info = DB.getConfiguration()
            if info != None:
                if(len(info)>0):
                    Information = info[0]

            debugText = ''

            if start == None:
                if info != None:
                    if len(info) < 0:
                            Information['debugger'] = 1
                    elif Information['debugger'] == 0 or Information['debugger'] == '' or Information['debugger'] == None:
                        Information['debugger'] = 1
                    else:
                        Information['debugger'] = 0

                    if info != None:
                        if len(info) > 0:
                            DB.update(DB._tableConfiguration,Information,"id = '"+str(Information['id'])+"'")
                        else:
                            DB.insert(DB._tableConfiguration,Information)

            if Information['debugger'] == 0 or Information['debugger'] == '' or Information['debugger'] == None:
                debugText = 'Turn Debugging On'
            else:
                debugText = 'Turn Debugging Off'

            self.Debuging.setText(debugText)

        def newWindow(self):
            self = ProjectWin()
            self.show()
            sys.exit(app.exec_())
        def getWindowsInformation(self):
            WindowsInformation = {};
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

                if(windowDetailedName[0] != None and (str(windowDetailedName[0]) == 'Windows' or str(windowDetailedName[0]) == 'windows')):
                    WindowsInformation['isWindows'] =True
                else:
                    WindowsInformation['isWindows'] =False

                if(windowDetailedName[1] != None and (str(windowDetailedName[1]) != '')):
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
            except Exception as e:
                Debuging = Debuger()
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

                Debuging.tureDebugerOn()
                Debuging.logError('Could Not get Windows Information Line range 220 - 240 File Fixity ', moreInformation)
                pass

            return WindowsInformation

        #Updates Fields When Project Is Selected In List
        @Slot(str)
        def update(self, new):
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

                information = {}
                projectName = self.projects.currentItem().text()
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
                    if n != None :
                        try:
                            self.dtx[(n)].setText(str(pathInfo[(n)]['path']).strip())
                        except:
                            self.dtx[(n)].setText("")

                for n in pathInfo:
                    if n != None :
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
                        except Exception as e:
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

        # New Project Creation
        def new(self):

                name = QInputDialog.getText(self, "Project Name", "Name for new Fixity project:", text="New_Project")
                projectInfo =  self.Database.getProjectInfo(name[0])
                if projectInfo:
                    if projectInfo[0]:
                        QMessageBox.warning(self, "Fixity", "Invalid project name:\n*Project names must be unique\n*Project names cannot be blank\n*Project names cannot contain spaces\n*Project names must be legal filenames")
                        return

                newitem = QListWidgetItem(name[0], self.projects)
                self.projects.setCurrentItem(newitem)
                self.monthly.setChecked(True)
                self.monthclick()
                self.dom.setValue(1)
                self.timer.setTime(QTime(0, 0))
                for x in xrange(0, 7):
                    self.dtx[x].setText("")
                    self.mtx[x].setText("")

                self.old = newitem
                self.toggler(False)

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
                            errorMsg = self.EP.ValidateEmail(SingleEmail)
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
                            if self.FileChanged.changeThePathInformation:
                                CodeOfPath = FixityCore.pathCodeEncode(directoryIncreament)
                                pathToSaveInManifest = str(ds.text())
                                pathsInfoChanges[directoryIncreament]=str(ds.text())
                            else:
                                CodeOfPath = FixityCore.pathCodeEncode(directoryIncreament)
                                pathToSaveInManifest = str(str(self.FileChanged.orignalPathText))
                                pathsInfoChanges[directoryIncreament] =  str(str(self.FileChanged.orignalPathText))

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
                    projectInformation['lastRan'] = None


                    Configurations = {}

                    Configurations['RunWhenOnBatteryPower'] = self.runOnlyOnACPower.isChecked()
                    Configurations['IfMissedRunUponAvailable'] = self.StartWhenAvailable.isChecked()
                    Configurations['onlyonchange'] = self.EmailOnlyWhenSomethingChanged.isChecked()
                    Configurations['RunInitialScan'] = False

                    FixitySchtask.schedule(interval, dweek, dmonth, self.timer.time().toString(), self.projects.currentItem().text(), projectInformation,self.SystemInformation , pathsInfoChanges)

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
                            l = self.buildTable(src, 'sha256')
                            for n in xrange(len(l)):
                                if FiltersArray:
                                    for FA in FiltersArray :
                                        if FA == '' or l[n][1].find(FA) < 0:
#                                             projfile.write(l[n][0] + "\t" + l[n][1] + "\t" + l[n][2] + "\n")
                                            total += 1

                    if shouldRun:
                        QMessageBox.information(self, "Fixity", str(total) + " files processed in project: " + self.projects.currentItem().text())
                        return pathsInfoChanges
                    else:

                        QMessageBox.information(self, "Fixity", "Settings saved for " + self.projects.currentItem().text())
                        return pathsInfoChanges


#                     projfile.close()
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

                        QMessageBox.information(self, "Fixity", "Settings saved for " + self.projects.currentItem().text())


                return

        # Toggles fields on/off
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


        def changed(self):
                self.unsaved = True

        def dayclick(self):
                self.dom.hide()
                self.dow.hide()
                self.spacer.changeSize(30, 25)

        def weekclick(self):
                self.spacer.changeSize(0, 0)
                self.dom.hide()
                self.dow.show()

        def monthclick(self):
                self.spacer.changeSize(0, 0)
                self.dow.hide()
                self.dom.show()


        def pickdir(self):
                n = self.but.index(self.sender())
                self.dtx[n].setText(QFileDialog.getExistingDirectory(dir=path.expanduser('~') + '\\Desktop\\'))


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



        #Saves And Runs
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

            DB = Database()
            Configurations = DB.getProjectInfo(self.projects.currentItem().text())

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

            FileName = 'AutoFixity.exe';
            params = self.projects.currentItem().text() +' '+'Run'

            self.Threading = Threading(self.projects.currentItem().text(), self.projects.currentItem().text(), 1,FileName,FilePath , params)

            self.Threading.start()
            QMessageBox.information(self, "Fixity", "Scheduler for Project "+self.projects.currentItem().text() + " is in progress,you will receive an email when process is completed")

        #DELETE Given PROJECT
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
                    DB = Database()
                    projInfo = DB.getProjectInfo(self.projects.currentItem().text())

                    if len(projInfo) > 0:

                        DB.delete(DB._tableVersionDetail, "`projectID` = '"+str(projInfo[0]['id'])+"'")
                        DB.delete(DB._tableProjectPath, "`projectID` = '"+str(projInfo[0]['id'])+"'")
                        DB.delete(DB._tableVersions, "`id` = '"+str(projInfo[0]['versionCurrentID'])+"'")
                        DB.delete(DB._tableProject, "title like '"+self.projects.currentItem().text()+"'")

                except:
                    pass

                FixitySchtask.deltask(self.projects.currentItem().text())
                self.projects.takeItem(self.projects.row(self.projects.currentItem()))
                self.unsaved = False

                try:
                        self.update(self.projects.selectedItems()[0])
                except:
                        for x in xrange(0, 7):
                                self.dtx[x].setText("")
                                self.mtx[x].setText("")
                        self.monthly.setChecked(True)
                        self.monthclick()
                        self.timer.setTime(QTime(0, 0))
                        self.lastrun.setText("Last checked:")
                self.toggler((self.projects.count() == 0))
                self.unsaved = False

        #Fetch All Directory with in this directory
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
                        h = FixityCore.fixity(p, a)
                        i = FixityCore.ntfsID(p)
                        list.append((h, p, i))
                        progress.setValue(100 * float(f) / len(fls))
                        qApp.processEvents()
                progress.close()
                return list


        #Update Schedule information
        def updateschedule(self):
                flagInitialScanUponSaving = False
                isRcipentEmailAddressSet = False
                allEmailAddres = ''
                for ms in self.mtx:
                        SingleEmail = ms.text().strip()
                        if  SingleEmail != "":
                            allEmailAddres = allEmailAddres + str(SingleEmail) +','
                            isRcipentEmailAddressSet = True
                            errorMsg = self.EP.ValidateEmail(SingleEmail)
                            if not str(errorMsg).strip() == 'None':
                                QB = QMessageBox()
                                errorMsg = QB.information(self, "Error", errorMsg)
                                return

                if isRcipentEmailAddressSet:
                    EmailInfo = self.EP.getConfigInfo()
                    if len(EmailInfo) <= 0:
                        QMessageBox.information(self, "Email Validation", 'Please configure an email account in the Preferences menu')
                        return

                pathsInfoChanges = self.process(flagInitialScanUponSaving)
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
                    runDayOrMonth = '2'
                elif (dmonth == 99 and dweek != 99):
                    runDayOrMonth = '1'
                elif(dmonth != 99 and dweek == 99):
                    runDayOrMonth = '0'
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
                projectInformation['lastRan'] = self.timer.time().toString()

                Configurations = {}
                Configurations = self.EP.getConfigInfo(self.projects.currentItem().text())
                Configurations['RunWhenOnBatteryPower'] = self.runOnlyOnACPower.isChecked()
                Configurations['IfMissedRunUponAvailable'] = self.StartWhenAvailable.isChecked()
                Configurations['onlyonchange'] = self.EmailOnlyWhenSomethingChanged.isChecked()
                Configurations['RunInitialScan'] = False
                self.unsaved = False
                self.update(self.projects.currentItem().text())
                self.unsaved = True
#                 pathsInfoChanges = {}
#                 directoryIncreamentDirs = 1
#
#                 for ds in self.dtx:
#                     pathsInfoChanges[directoryIncreamentDirs]=str(ds.text())
#                     directoryIncreamentDirs = directoryIncreamentDirs + 1
#
                FixitySchtask.schedule(interval, dweek, dmonth, self.timer.time().toString(), self.projects.currentItem().text() , projectInformation,self.SystemInformation , pathsInfoChanges)
                self.unsaved = False

        #Remove the file which are not required
        def removeNotRequiredFiles(self):

            if not str(self.projects.currentItem()) == 'None':
                if path.isfile('projects\\' + self.projects.currentItem().text() + '.fxy') and path.isfile('bin\\' + self.projects.currentItem().text() + '-conf.txt'):
                    projectFile = open('projects\\' + self.projects.currentItem().text() + '.fxy', 'rb')
                    binFile = open('bin\\' + self.projects.currentItem().text() + '-conf.txt', 'rb')
                    projectFileLines = projectFile.readlines();
                    binFileLines = binFile.readlines();
                    projectFile.close()
                    binFile.close()
                    if (not binFileLines) or (not projectFileLines):
                        remove('projects\\' + self.projects.currentItem().text() + '.fxy')
                        remove('bin\\' + self.projects.currentItem().text() + '-conf.txt')
            return

        #Window close Event
        def closeEvent(self, event):
            if not str(self.projects.currentItem()) == 'None':
                if path.isfile('projects\\' + self.projects.currentItem().text() + '.fxy') and path.isfile('bin\\' + self.projects.currentItem().text() + '-conf.txt'):
                    projectFile = open('projects\\' + self.projects.currentItem().text() + '.fxy', 'rb')
                    binFile = open('bin\\' + self.projects.currentItem().text() + '-conf.txt', 'rb')
                    projectFileLines = projectFile.readlines();
                    binFileLines = binFile.readlines();
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

        def importProjects(self):
            self.ImportProjects.destroyImportProjects()
            self.ImportProjects = None
            self.ImportProjects = ImportProjects()
            self.ImportProjects.CreateWindow()
            self.ImportProjects.SetWindowLayout()
            self.ImportProjects.SetDesgin()
            self.ImportProjects.ShowDialog()
            app.exec_()

        def checkForChanges(self,projectName , searchForPath ,code):
                    try:
                        DB = Database()
                        info = DB.getProjectInfo(projectName)
                        information = info[0]
                        DirectoryDetail = DB.getProjectPathInfo(information['id'], information['versionCurrentID'])
                        for  DD in DirectoryDetail:
                            if (str(DirectoryDetail[DD]['pathID']).strip() == str(code).strip()):
                                if(DirectoryDetail[DD]['path'] != searchForPath):
                                    self.ChangeRootDirectoryInfor(DirectoryDetail[DD]['path'] , searchForPath )
                    except:
                        pass

if __name__ == '__main__':
        app = QApplication(sys.argv)
        w = ProjectWin(EmailPref , FilterFiles)
        w.show()
        sys.exit(app.exec_())

