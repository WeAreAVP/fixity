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
        projects_path = getcwd()+'\\projects\\'
        Information = FixityCore.getConfigInfo(selectedProject)
        
        aloValueSelected = ''
        if self.methods.currentText() == None or self.methods.currentText() == '':
            aloValueSelected = 'algo|sha256' 
        else:
            aloValueSelected = 'algo|' + str(self.methods.currentText())
        
        sameValueFlag = False
        if aloValueSelected != Information['Algorithm']:
            sameValueFlag =True
            response = self.slotWarning(selectedProject)
            if response:
                msgBox.setWindowTitle("Processing ....")
                msgBox.setText("Reading Files, please wait ...")
                msgBox.show()
                QCoreApplication.processEvents()

                hasChanged = self.run(projects_path + selectedProject + '.fxy' , '' , selectedProject, True)
                if hasChanged:
                    Information['Algorithm'] = aloValueSelected
                    response = True
            else:
                response = False
        else:
            sameValueFlag = False
        if selectedProject == '':
            QMessageBox.information(self, "Failure", "No Project Selected")
            return
        
        flag = self.EmailPref.setConfigInfo(Information, selectedProject)
        if response:
            if flag and hasChanged:
                if not self.run(projects_path + selectedProject + '.fxy' , '' , selectedProject, True):
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
        
        Information = FixityCore.getConfigInfo(selectedProject)
        
    
        Algorithm = str(Information['Algorithm']).replace('algo|', '').replace('\n', '')
    
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

        
    def run(self,file,filters='',projectName = '',checkForChanges = False):
        
        
        FiltersArray = filters.split(',')
        dict = defaultdict(list)
        dict_Hash = defaultdict(list)
        dict_File = defaultdict(list)
        confirmed , moved , created , corruptedOrChanged  = 0, 0, 0, 0
        FileChangedList = ""
        InfReplacementArray = {} 
        dctValue = FixityCore.getDirectoryDetail(projectName , file)
        
        infile = open(file, 'r')
        tmp = open(file + ".tmp", 'w')
        first = infile.readline()
        second = infile.readline()
        ToBeScannedDirectoriesInProjectFile = []
        ToBeScannedDirectoriesInProjectFileRaw = first.split(';')
        
        for SingleDircOption in ToBeScannedDirectoriesInProjectFileRaw:
            SingleDircOption = SingleDircOption.strip()
            SignleDirCodeAndPath = SingleDircOption.split('|-|-|')
            if SignleDirCodeAndPath[0].strip():
                ToBeScannedDirectoriesInProjectFile.append(SignleDirCodeAndPath[0].strip())
                InfReplacementArray[SignleDirCodeAndPath[0].strip()]= {'path':SignleDirCodeAndPath[0].strip(),'code':'Fixity-'+SignleDirCodeAndPath[2] ,'number': SignleDirCodeAndPath[2]}
        mails = second.split(';')
        keeptime = infile.readline()
        trash = infile.readline()
        
        tmp.write(first)
        tmp.write(second)
        tmp.write(keeptime)
        tmp.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        
        check = 0
        for l in infile.readlines():
            try:
                x = FixityCore.toTuple(l)
                if x != None and x:
                    pathInformation = str(x[1]).split('||')
                    if pathInformation:
                        CodeInfoormation=''
                        CodeInfoormation = pathInformation[0]
                        pathInfo = FixityCore.getCodePathMore(CodeInfoormation ,dctValue)
                    
                        dict[x[2]].append([pathInfo+pathInformation[1], x[0], False])
                        dict_Hash[x[0]].append([pathInfo+pathInformation[1], x[2], False])
                        dict_File[pathInfo+pathInformation[1]].append([x[0], x[2], False])
                else:
                    raise Exception
            
            except Exception as ex :
                moreInformation = {"moreInfo":'null'}
                try:
                    if not ex[0] == None:
                        moreInformation['LogsMore'] =str(ex[0])
                except:
                    pass
                try:    
                    if not ex[1] == None:
                        moreInformation['LogsMore1'] =str(ex[1])
                except:
                    pass
                try:
                    moreInformation['directoryScanning']
                except:
                    moreInformation['directoryScanning'] = ''
                for SingleVal in ToBeScannedDirectoriesInProjectFile:
                    moreInformation['directoryScanning']= str(moreInformation['directoryScanning']) + "\t \t"+str(SingleVal)
                    
                Debugging = Debuger()
                Debugging.tureDebugerOn()    
                Debugging.logError('Error Reporting 615  - 621 File FixityCore While inserting information'+"\n", moreInformation)    
        
        try:
            ToBeScannedDirectoriesInProjectFile.remove('\n')
        except:
            pass    
        flagAnyChanges = False
        
        information = FixityCore.getConfigInfo(projectName)
        Algorithm = str(information['Algorithm']).replace('algo|', '').replace('\n', '')
        if Algorithm == '' or Algorithm == None :
            Algorithm = 'sha256'
        for SingleDirectory in ToBeScannedDirectoriesInProjectFile:
            counter = self.getnumberoffiles(SingleDirectory)
            DirectorysInsideDetails = self.quietTable(SingleDirectory, Algorithm,InfReplacementArray , projectName,counter)
            
            for e in DirectorysInsideDetails:
                
                flag =True
                e = list(e)
                filePath = str(e[1]).split('||')
                pathInfo = FixityCore.getCodePath(filePath[0], InfReplacementArray)
                
                valDecoded = pathInfo
                e[1] = (str(valDecoded)+str(filePath[1]))
                
                for Filter in FiltersArray:
                    if Filter !='' and e[1].find(str(Filter).strip()) >= 0:
                        flag =False
                
                if flag:
                    check+= 1
                    
                    try:
                        response = FixityCore.verify_using_inode(dict,dict_Hash,dict_File, e , file)
                        
                        
                    except Exception as ex :
                        moreInformation = {"moreInfo":'null'}
                        try:
                            if not ex[0] == None:
                                moreInformation['LogsMore'] =str(ex[0])
                        except:
                            pass
                        try:    
                            if not ex[1] == None:
                                moreInformation['LogsMore1'] =str(ex[1])
                        except:
                            pass
                        
                        Debugging = Debuger()
                        Debugging.tureDebugerOn()    
                        Debugging.logError('Error Reporting Line 500 FixityCore While Verfiying file status' +str(file)+' '+'||'+str(e[0])+'||'+'||'+str(e[1])+' '+'||'+str(e[2])+'||'+"\n", moreInformation)
                        pass
                    try:
                        
                        FileChangedList += response[1] + "\n"
                        if response[1].startswith('Confirmed'): 
                            confirmed += 1
                        elif response[1].startswith('Moved'):
                            flagAnyChanges = True
                            moved += 1
                        elif response[1].startswith('New'):
                            flagAnyChanges = True
                            created += 1
                        else:
                            flagAnyChanges = True
                            corruptedOrChanged += 1
                            
                    except:
                        pass
                    
                    pathCode = FixityCore.getPathCode(str(SingleDirectory),InfReplacementArray)
                    newCodedPath = str(response[0][1]).replace(SingleDirectory, pathCode+"||")
                    
                    tmp.write(str(response[0][0]) + "\t" + str(newCodedPath) + "\t" + str(response[0][2]) + "\n")
                        
                    
        missingFile =[0,0,0]            
        try:  
            missingFile = FixityCore.missing(dict_Hash,SingleDirectory)
            if missingFile[0] > 0:
                flagAnyChanges = True
            if len(missingFile) > 0:
                FileChangedList += str(missingFile[0])
        except:
            pass
        tmp.close()
        infile.close()
        
        
        
        information = str(file).split('\\')
        projectName = information[(len(information)-1)]
        projectName = str(projectName).split('.')
        
        
        if(flagAnyChanges):
            shutil.copy(file , getcwd()+'\\history\\'+projectName[0]+'-'+str(datetime.date.today())+'-'+str(datetime.datetime.now().strftime('%H%M%S'))+'.inf')
        
            
        shutil.copy(file + ".tmp", file)
        remove(file + ".tmp")
        
#         total = confirmed + moved + created + corruptedOrChanged + missingFile[1]
#         repath = FixityCore.writer(Algorithm, file.replace('.fxy','').replace('projects\\',''), total, confirmed, moved, created, corruptedOrChanged, missingFile[1], FileChangedList,projectName)
        
        return flagAnyChanges
        
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
#          
# projects_path = getcwd()+'\\projects\\'
# print(w.run(projects_path+'New_Project.fxy','','New_Project'))