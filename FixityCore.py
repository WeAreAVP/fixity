# -*- coding: utf-8 -*-
# Fixity Core module
# Version 0.3, 2013-10-28
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



'''
Built in Library
'''
import hashlib
from os import chdir, walk, path, stat, getcwd, O_RDWR, O_CREAT
from sys import argv ,exit
from collections import defaultdict
from platform import platform
import datetime
import time
from glob import glob
from os import path, makedirs, remove
from re import sub, compile
import fnmatch
import sys
import codecs
import StringIO
import parser
import ctypes

if(OS_Info == 'Windows'):
    import win32file
    import win32api, win32con

import shutil
import base64
import unicodedata
reload(sys)

'''
Custom Library
'''

if OS_Info == 'Windows':
    import FixityCoreWin
    
else:
    import FixityCoreMac
    
    
from Debuger import Debuger
from EmailPref import EmailPref
from Database import Database
from AboutFixity import AboutFixity
global verifiedFiles
try:
    verifiedFiles =[]
except:
    verifiedFiles =[]

Debugging = Debuger()
from FileLock import FileLock


'''
Checksum Generation Method.
Input: File Path, Algorithm.
Output: Hexadecimal Value Of Hashed File.

'''
def fixity(filePath, Algorithm , projectName= None):
    moreInformation= {}
    
    try:
        if Algorithm =='md5':
            fixmd5 = hashlib.md5()
        else:
            fixsha256 = hashlib.sha256()
        
    except Exception as Excep:

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

        Debugging.tureDebugerOn()
        Debugging.logError('Error Reporting Line 36 - 40 While encrypting File into hashes using Algo:' + str(Algorithm)  +" File FixtyCore\n", moreInformation)

        pass
    try:
        if OS_Info == 'Windows':
            filePath = str(filePath).replace('\\\\','\\')
            filePath = str(filePath).replace('\\',str(os.sep)+str(os.sep))
       
        
        if OS_Info == 'Windows':
            with open(filePath.decode('utf-8'), 'r') as target:
                for piece in iter(lambda: target.read(4096), b''):
                    if Algorithm =='md5':
                        fixmd5.update(piece)
                    else:
                        fixsha256.update(piece)
                    
                target.close()
                
                if Algorithm =='md5':
                    return fixmd5.hexdigest()
                else:
                    return fixsha256.hexdigest()
        else:
            
            with open(filePath, 'r') as target:
                for piece in iter(lambda: target.read(4096), b''):
                    if Algorithm =='md5':
                        fixmd5.update(piece)
                    else:
                        fixsha256.update(piece)
                    
                target.close()
                
                if Algorithm =='md5':
                    return fixmd5.hexdigest()
                else:
                    return fixsha256.hexdigest()
                
    except Exception as Excep:
        moreInformation = {"moreInfo":'none'}
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
        
        
        Debugging.tureDebugerOn()
        Debugging.logError('Error Reporting Line 59 - 63 While encrypting File into hashes using Algo:' + str(Algorithm)  +" File FixtyCore\n", moreInformation)
        pass
    





'''
Get information from Project File matched with given information

@param ProjectPath: Project File path to be scaned
@param hash: search this hash from given Project File
@param path: search this path from given Project File
@param inode: search this inode from given Project File

@return: Tuple file information matching the given conditions

'''
def getFileInformationConditional(ProjectPath ,hashVal='',path='',inode=''):

    Information=[]
    try:
        editedPadth = path.replace('\\\\','\\')
        f = open(ProjectPath)
        try:
            content = f.readlines()
            for singleLine in content:
                if ( hashVal in str(singleLine) or hashVal == '' ) and ( inode in str(singleLine) or inode == '' ) and ( path in str(singleLine) or editedPadth in str(singleLine) or path == ''  ):
                    Information.append(singleLine)
        except:
            pass
        try:
            f.close()
        except:
            pass
        return Information

    except:

        return Information



'''
Get Directory Information Using Inode from the given directory (scan given path and searches for the File which have this given Inode)

@param Path : Path of the Directory
@param Inode: Inode To Be Searched

@return:  Boolean
'''

def GetDirectoryInformationUsingInode(Path,Inode):
    try:
        if Path and Inode:
            for root, subFolders, files in walk(Path):
                for SingleFile in files:
                    path.join(root, SingleFile)

                    if(OS_Info == 'Windows'):
                        ThisInode = str(FixityCoreWin.ntfsIDForWindows(path.join(root, SingleFile)))
                    else:
                        ThisInode = str(FixityCoreMac.ntfsIDForMac(path.join(root, SingleFile)))
                    if  ThisInode == Inode:
                        return Inode
        return True
    except:
        return True



'''
Method to handle all special characters

@param StringToBeHandled: String To Be Handled 

@return:  String - Fixed characters String
'''  
def scpecialCharacterHandler(StringToBeHandled):
    
    
    try:
        StringToBeHandled = StringToBeHandled.decode('cp1252')
    except Exception as Excep:
        print(Excep[0])
        pass
    try:
        StringToBeHandled = StringToBeHandled.encode('utf8')
    except Exception as Excep:
        print(Excep[0])
        pass
    
    return StringToBeHandled



'''
Method to convert database line into tuple
@param line: Information of a single File

@return tuple: (hash, abspath, id)
'''
def toTuple(line):
    
    try:
        return [line['hashes'], str(line['path'].encode('utf-8')).strip(), line['inode']]
    except Exception as Excep:

        Debugging.tureDebugerOn();
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
        Debugging.tureDebugerOn()
        Debugging.logError('Error Reporting Line 148-150 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)

        return None




'''
Method to generate a dictionary, keyed to file hashes
This is done to greatly speed up the eventual fixity checks
@param file: Database file
@return : defaultdict keyed to hash values
'''
def buildDict(filePathFix):

    try:

        table = open(filePathFix, 'r')
        db = defaultdict(list)

        for line in table.readlines():
            try:
                x = toTuple(line)
                db[x[0]].append([x[1], x[2], False])
            except:
                pass
        try:
            table.close()
        except:
            pass
        return db
    except Exception as Excep:

        Debugging.tureDebugerOn();
        moreInformation = {"moreInfo":'null'}
        try:
            if not Excep[0] is None:
                moreInformation['LogsMore'] =str(Excep[0])
        except:
            pass
        try:
            if not Excep[1] is None:
                table.close()

                moreInformation['LogsMore1'] =str(Excep[1])
        except:
            pass
        Debugging.tureDebugerOn()
        Debugging.logError('Error Reporting Line 173-179 FixityCore While building directory and files FixityCore' +"\n", moreInformation)

        return None




'''
Writes table to file
@param path: filepath, table (list of tuples from toTuple)
@param listOfValue: All File scanned in last scan

@return Output: A nicely written file
'''
def tableToFile(path, listOfValue):
    f = open(path, 'w')
    for item in listOfValue:
        x = str(item[0]) + "\t" + str(item[1]) + "\t" + str(item[2])
        f.write("%s\n" % x)
    f.close()
    return





'''
Writes one tuple to file
# Input: filepath, tuple (hash, path, id)
# Output: file has one new line
'''
def tupleToFile(path, InformationOfFileToBeWriten):

    f = open(path, 'a')
    x = str(InformationOfFileToBeWriten[0]) + "\t" + str(InformationOfFileToBeWriten[1]) + "\t" + str(InformationOfFileToBeWriten[2])
    f.write("%s\n" % x)
    f.close()
    return




'''
Get hash from list
@param String:

@return: String
'''
def getHash(string):
    newString = str(string)[2:66]
    return newString





'''
Get Directory information
@param directory: directory path
@param inode: inode of File
@param filePath: File Path
@param dicty: List of all directory with inode , hash and path information

@return:  List - list of match directory

'''
def getDirectory(directory,inode,filePath,dicty):

    mainDirectory = ''
    try:
        directory[1]
    except:
        mainDirectory = None

    if mainDirectory is None:
        mainDirectory = directory[0]
        if not mainDirectory[1] == inode :
            mainLine = getFileInformationConditional(filePath,'','',inode)
            mainLine = getHash(mainLine)
            mainDirectory = dicty.get(mainLine)
            if not mainDirectory is None :
                return None;
    else:
        secDirectory = directory[0]
        if secDirectory[1] == inode :
            mainDirectory = directory[0]

        secDirectory = directory[1]
        if secDirectory[1] == inode :
            mainDirectory = directory[1]
        mainDirectory = directory[1]
    return mainDirectory





'''
Verify File Changes when scanning
Method to verify a tuple against the dictionary
Input: defaultDict (from buildDict), tuple
Output: Message based on whether the file was good or not


@param dicty: List of all directory with inode , hash and path information  with indexed using Inode
@param dictHash: List of all directory with inode , hash and path information with indexed using hash
@param dictFile: List of all directory with inode , hash and path information
@param line: lsit of file to be scanned in this run
@param fileNamePath: File Path with file name to be scanned in this run
@param dctValue: Index of dict to be scanned
@param Algorithm: Algo set be the user for this project to be used for file formation to be stored

@return: List - list of result of scanning occurred in this file for a single file

'''

def verify_using_inode (dicty, dictHash, dictFile, line, fileNamePath='' , dctValue = '',Algorithm='sha256'):
    
    global verifiedFiles
    
    
    try:
        ''' Check if I-Node related information Exists in the Given Directory  '''
        CurrentDirectory = dicty.get(line[2])
    except Exception as Excep:

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
        
        Debugging.tureDebugerOn()
        Debugging.logError('Error Reporting Line 250 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)
        pass
    
    if path.isfile(line[1].decode('utf-8')):
        '''' IF SAME INODE EXISTS '''
        if CurrentDirectory is not None :
            print('if')
            CurrentDirectory = CurrentDirectory[0]
            isHashSame , isFilePathSame = '' , ''

            ''' Check For File Hash Change '''
            isHashSame = (CurrentDirectory[1] == line[0])

            ''' Check For File Path Change ''' 
            isFilePathSame = (CurrentDirectory[0] == line[1])
            
            '''   FileExists::YES  ||SameHashOfFile::YES  ||SameFilePath::YES ||SameI-Node::YES  '''
            if isHashSame and isFilePathSame:
                verifiedFiles.append(line[1])
                return line, "Confirmed File :\t" + str(line[1])
            
            
            '''   FileExists::YES  ||SameHashOfFile::YES  ||SameFilePath::NO ||SameI-Node::YES  '''
            if isHashSame and (not isFilePathSame):
                verifiedFiles.append(line[1])
                verifiedFiles.append(CurrentDirectory[0])
                return line, "Moved or Renamed File :\t" + str(CurrentDirectory[0]) + "\t changed to\t" + str(line[1])
            
            
            '''   FileExists::YES  ||SameHashOfFile::NO  ||SameFilePath::YES ||SameI-Node::YES  '''
            if (not isHashSame) and isFilePathSame:

                verifiedFiles.append(line[1])
                return line, "Changed File :\t" + str(line[1])
            
            
            '''   FileExists::YES  #SameHashOfFile::NO  #SameFilePath::NO #SameI-Node::YES  '''
            if (not isHashSame) and (not isFilePathSame):
                
                verifiedFiles.append(line[1])
                verifiedFiles.append(CurrentDirectory[0])
                return line, "Changed File :\t" + str(line[1])

        else :
            print('else')
            CurrentDirectory = []
            
            for dictionarySingle in dictHash:
                allInforHashRelated = dictHash[dictionarySingle]
                
                for singleInforHashRelated in allInforHashRelated:
                    
                    '''  FileExists::YES   #SameHashOfFile::YES   #SameFilePath::YES    #SameI-Node::NO  '''
                    if singleInforHashRelated[0] == line[1] and dictionarySingle == line[0]:
                        verifiedFiles.append(line[1])            
                        return line, "Confirmed File :\t" + str(line[1])

                    
                        '''  FileExists::YES   #SameHashOfFile::NO   #SameFilePath::YES   #SameI-Node::NO  '''
                    elif singleInforHashRelated[0] == line[1] and dictionarySingle != line[0]:
                        verifiedFiles.append(line[1])
                        return line, 'Changed File :\t' + str(line[1])
                    
                        '''  FileExists::YES   #SameHashOfFile::YES   #SameFilePath::NO  #SameI-Node::NO  '''
                    elif singleInforHashRelated[0] != line[1] and dictionarySingle == line[0]:
                        verifiedFiles.append(line[1])
                        return line, 'New File :\t' + str(line[1])
                    
        
        '''  FileExists::YES   #SameHashOfFile::NO    #SameFilePath::NO     #SameI-Node::NO  '''
        verifiedFiles.append(line[1])
        return line, 'New File :\t' + str(line[1])



'''
Writes report about the most recent fixity check
Input: algorithm used, start time, directories scanned, number of files found, good files, warned files, bad files, missing files, [out?], current time, old DB, new DB
Output: All this, written nicely to a tab-delimited file, with the file returned

@param algoUsed: Algorithm used for the project to record changes
@param projectPath: Project Name With Path
@param TotalFilesScanned: Total number of File Scanned
@param confirmedFileScanned: confirmed File Scanned
@param movedFileScanned: moved File Scanned
@param newFileScanned: new File Scanned
@param failedFileScanned: failed File Scanned
@param deletedFileScanned: deleted File Scanned
@param DetailOutputOfAllFilesChanges: Detail Output Of All FilesChanges
@param projectName: List of all directory with inode , hash and path information  with indexed using Inode

@return: String-File Path of the report writen

'''
def writer(algoUsed, projectPath, TotalFilesScanned, confirmedFileScanned , movedFileScanned, newFileScanned, failedFileScanned, deletedFileScanned, DetailOutputOfAllFilesChanges, projectName=''):
    print('writer')
    rn = ''
    try:
        report = "Fixity report\n"
        report += "Project name\t" + projectPath + "\n"
        report += "Algorithm used\t" + algoUsed + "\n"
        report += "Date\t" + str(datetime.date.today()) + "\n"
        report += "Total Files\t" + str(TotalFilesScanned) + "\n"
        report += "Confirmed Files\t" + str(confirmedFileScanned) + "\n"
        report += "Moved or Renamed Files\t" + str(movedFileScanned) + "\n"
        report += "New Files\t" + str(newFileScanned) + "\n"
        report += "Changed Files\t" + str(failedFileScanned) + "\n"
        report += "Removed Files\t" + str(deletedFileScanned) + "\n"
        print(1)
        try:
            report += DetailOutputOfAllFilesChanges.encode('utf8')
        except:
            pass
        try:
            report += DetailOutputOfAllFilesChanges.decode('utf8')
        except:
            pass
        print(report)
        print(2)
    except Exception as Excep:
        print(Excep[0])
        
        
    print(3)
    print(projectName)
    print(4)
    if(OS_Info == 'Windows'):
        AutiFixPath = (getcwd()).replace('schedules','').replace('\\\\',"\\")
        rn = AutiFixPath+str(os.sep)+'reports'+str(os.sep)+'fixity_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S')) + '_' + str(projectName[0])  + '.tsv'
    else:
        fromDycruptionClass = False
        AutiFixPath = (getcwd()).replace('schedules','').replace('//',"/")
        try:
            NameOfFile = str(projectName[1]).split('/')
        except:
            NameOfFile = str(projectName[0])
            fromDycruptionClass = True
        print(NameOfFile)
        

        print(len(NameOfFile))
        pathInfo = getFixityHomePath()
        createPath = str(pathInfo).replace(' ', '\\ ')

        if not os.path.isdir( str(createPath) + 'reports' ):
            try:
                os.mkdir( str(createPath) + 'reports' )
            except Exception as Excep:
                print(Excep[0])
        if not fromDycruptionClass:
            rn = str(pathInfo)+'reports'+str(os.sep)+'fixity_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S')) + '_' + str(NameOfFile[(len(NameOfFile)-1)])  + '.tsv'
        else:
            rn = str(pathInfo)+'reports'+str(os.sep)+'fixity_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S')) + '_' + str(NameOfFile)  + '.tsv'
        try:
            rn = str(rn).replace(' ', '\\ ')
        except Exception as Ex:
            print(Ex[0])
    print(rn)
    print(5)
    try:
        r = open(rn, 'w+')
        try:
            r.write(report.decode('utf8'))
        except:
            pass
        
        try:
            r.write(report.encode('utf8'))
        except:
            pass
        
        r.close()
    except Exception as Excep:
        print(Excep[0])
    return rn




'''
Method to find which files are missing in the scanned directory
Input: defaultdict (from buildDict)
Output: warning messages about missing files (one long string and printing to stdout)

@param dict: Directory of all file exists in the scanned folder
@param file: List of all directory with inode , hash and path information  with indexed using Inode

@return: removed Messgae if removed and count of removed file

'''
def missing(dict,file=''):

    msg = ""
    count = 0
    global verifiedFiles
    ''' walks through the dict and returns all False flags ''' 
    for keys in dict:
        for obj in dict[keys]:

            if not path.isfile(obj[0]):
                ''' check if file already exists in the manifest ''' 
                if not obj[0] in verifiedFiles:
                    verifiedFiles.append(obj[0])
                    msg += "Removed Files\t" + obj[0] +"\n"
                    count = count + 1

    return msg, count




'''
---------------------------------------------------------------------------------------------------------
Logic For Selection of Scheduler time In History or Depreciated Manifest Functionality                  |
---------------------------------------------------------------------------------------------------------
If Loop is Weekly ---- Time to Run On ---- Day of Loop To Run On ---- If Loop Is Monthly     |  Result
(day of week to                                                        (day of month to 
run on if none 99)                                                     run on if none 99)
==========================================================================================================
==========================================================================================================
     99           ----    00:00:00    ----         99            ----        99              |  Daily    |
     1            ----    00:00:00    ----         1             ----        99              |  weekly   |
     99           ----    00:00:00    ----         99             ----        2              |  Monthly  |
----------------------------------------------------------------------------------------------------------
          
'''


'''
Updating/Creating Manifest
With on the given directory

@param file: project Name with path to be scanned
@param filters: Filters Will be applied on the given project by the user
@param projectName: project Name to be scanned
@param checkForChanges: check For Changes


@return: removed Messgae if removed and count of removed file

'''
def run(file,filters='',projectName = '',checkForChanges = False):

    global verifiedFiles
    flagAnyChanges = False
    print('Started:::'+projectName)
    try:
        processID = os.getpid()
    except:
        processID = None

    try:
        lock = FileLock(getcwd()+str(os.sep)+'bin'+str(os.sep)+'dblocker.log',processID, timeout=20)

        IsDeadLock = lock.isProcessLockFileIsDead()
    except:
        pass
    try:
        if(IsDeadLock):
            lock.is_locked = True
            lock.release()
    except Exception as ex:
            print(ex[0])

    try:
        print('acquire')
        lock.acquire()
    except Exception as ex:
        print(ex[0])

    verifiedFiles = list()
    DB = Database()
    
    missingFile = ('','')

    projectInformation = DB.getProjectInfo(str(projectName).replace('.fxy', ''))

    if len(projectInformation) <=0:
        return
    projectPathInformation = DB.getProjectPathInfo(projectInformation[0]['id'],projectInformation[0]['versionCurrentID'])
    projectDetailInformation = DB.getVersionDetails( projectInformation[0]['id'] , projectInformation[0]['versionCurrentID'] ,' id DESC')

    if(projectDetailInformation is not None):
        if (len(projectDetailInformation)<=0):
            if(len(projectInformation) > 0):
                projectDetailInformation = DB.getVersionDetailsLast(projectInformation[0]['id'])

    FiltersArray = filters.split(',')
    
    dict = defaultdict(list)
    dict_Hash = defaultdict(list)
    dict_File = defaultdict(list)
    
    confirmed , moved , created , corruptedOrChanged  = 0, 0, 0, 0
    FileChangedList = ""
    InfReplacementArray = {}
    
    if(OS_Info == 'Windows'):

        historyFile = getcwd()+str(os.sep)+'history'+str(os.sep)+str(projectName).replace('.fxy', '')+'_-_-_'+str(datetime.date.today())+'-'+str(datetime.datetime.now().strftime('%H%M%S'))+'.tsv'
    else:

        pathInfo = pathInfo = getFixityHomePath()
        createPath = str(pathInfo).replace(' ', '\\ ')
        
        if  not os.path.isdir(str(createPath)+'history') :
            try:
                os.mkdir(str(createPath)+'history')
            except:
                pass

        historyFile = str(pathInfo) + 'history' + str(os.sep)+str(projectName).replace('.fxy', '')+'_-_-_'+str(datetime.date.today())+'-'+str(datetime.datetime.now().strftime('%H%M%S'))+'.tsv'
        historyFile = str(historyFile).replace(' ', '\\ ')

    try:
        HistoryFile = open(historyFile , 'w+')
    except:
        pass
    print('writing ::: History File')

    first = ''
    for singlePathDF in projectPathInformation:
        first = str(first) + str(projectPathInformation[singlePathDF]['path'])+';'
    
    ToBeScannedDirectoriesInProjectFile = []
    for pathInfo in projectPathInformation:
        IdInfo = str(projectPathInformation[pathInfo]['pathID']).split('-')
        indexPathInfor = r''+str(str(projectPathInformation[pathInfo]['path']).strip())
        ToBeScannedDirectoriesInProjectFile.append(indexPathInfor)
        InfReplacementArray[indexPathInfor]= {'path':indexPathInfor,'code':str(projectPathInformation[pathInfo]['pathID']) ,'number': str(IdInfo[1]),'id':projectPathInformation[pathInfo]['id']}
    
    mails = str(projectInformation[0]['emailAddress']).split(',')
    print('writing ::: Stared Worked')
    check = 0
    
    for l in projectDetailInformation:
        
        try:
            x = toTuple(projectDetailInformation[l])
            
            if x is not None and x:
                pathInformation = str(x[1]).split('||')
                
                if pathInformation:
                    CodeInfoormation=''
                    CodeInfoormation = pathInformation[0]

                    pathInfo = getCodePathMore(CodeInfoormation ,InfReplacementArray)
                    
                    dict[str(x[2]).replace('\r\n','')].append([str(pathInfo['path']).replace('\r\n','')+str(pathInformation[1]).replace('\r\n',''), str(x[0]).replace('\r\n',''), False])
                    dict_Hash[x[0]].append([str(pathInfo['path']) + str(pathInformation[1]).replace('\r\n',''), str(x[2]).replace('\r\n',''), False])
                    dict_File[str(pathInfo['path']).replace('\r\n','')+str(pathInformation[1]).replace('\r\n','')].append([str(x[0]).replace('\r\n',''),str( x[2]).replace('\r\n',''), False])
                    
        except Exception as Excep :

            moreInformation = {"moreInfo":'null'}
            try:
                if not Excep[0] is None:
                    moreInformation['LogsMore'] =str(Excep[0])
            except Exception as Excep:
                print('moreInformation 771 FC')
                print(Excep[0])
            try:
                if not Excep[1] is None:
                    moreInformation['LogsMore1'] =str(Excep[1])
            except Exception as Excep:
                print('moreInformation 776 FC')
                print(Excep[0])
            try:
                moreInformation['directoryScanning']
            except:
                moreInformation['directoryScanning'] = ''
            
            for SingleVal in ToBeScannedDirectoriesInProjectFile:
                moreInformation['directoryScanning']= str(moreInformation['directoryScanning']) + "\t \t"+str(SingleVal)

            
            Debugging.tureDebugerOn()
            Debugging.logError('Error Reporting 615  - 621 File FixityCore While inserting information'+"\n", moreInformation)
            
    
    print('added all files to dictionary')
    try:
        ToBeScannedDirectoriesInProjectFile.remove('\n')
    except Exception as Excep:
            print('ToBeScannedDirectoriesInProjectFile 794 FC')
            print(Excep[0])
    

    Algorithm = str(projectInformation[0]['selectedAlgo'])
    print('--------------------- History ----------------')
    counter = 0
    thisnumber = 0
    CurrentDate = time.strftime("%Y-%m-%d")
    
    Information = {}
    
    Information['versionType'] = 'save'
    Information['name'] = EncodeInfo(str(CurrentDate))
    
    versionID  = DB.insert(DB._tableVersions, Information)
    
    HistoryFile.write(str(first).replace('\n', '')+"\n")
    
    HistoryFile.write(str(projectInformation[0]['emailAddress']).replace('\r\n', '').replace('\n', '')+"\n")
    keeptime = ''
    
    '''
    #-----------------------------
    # Duration Type From Database|
    #-----------------------------
    # - 1 = Monthly
    # - 2 = Week
    # - 3 = Daily
    '''
    
    if int(projectInformation[0]['durationType']) == 3 :
        keeptime += '99 ' + str(projectInformation[0]['runTime']).replace('\r\n', '').replace('\n', '').replace('\n', '') + ' 99 99'
    elif int(projectInformation[0]['durationType']) == 2 :
        keeptime += '99 ' + str(projectInformation[0]['runTime']).replace('\r\n', '').replace('\n', '').replace('\n', '') + ' ' + str(projectInformation[0]['runDayOrMonth']).replace('\r\n', '').replace('\n', '') + ' 99'
    elif int(projectInformation[0]['durationType']) == 1 :
        keeptime += '99 ' + str(projectInformation[0]['runTime']).replace('\r\n', '').replace('\n', '').replace('\n', '') + ' 99 '+ str(projectInformation[0]['runDayOrMonth']).replace('\r\n', '').replace('\n', '')
    
    HistoryFile.write(keeptime.replace('\n', '').replace('\r\n', '')+"\n")
    HistoryFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    
    HistoryFile.write( str( projectInformation[0]['filters'] )+'||-||'+str(projectInformation[0]['ignoreHiddenFiles']) + "\n")
    HistoryFile.write( str( projectInformation[0]['selectedAlgo'] ) + "\n")
    
    '''
    Running Script Against All Given Directory In Given Project
    '''

    for SingleDirectory in ToBeScannedDirectoriesInProjectFile:
        '''
        Getting all files and directory  in side "SingleDirectory" with detail information (inode, path and file hash)
        '''
        DirectorysInsideDetails = quietTable(r''+SingleDirectory, Algorithm,InfReplacementArray , projectName)

        for DirectorysInsideDetailsSingle in DirectorysInsideDetails:
            
            thisnumber=thisnumber+1
            flag =True
            DirectorysInsideDetailsSingle = list(DirectorysInsideDetailsSingle)
            filePath = str(DirectorysInsideDetailsSingle[1]).split('||')
            pathInfo = getCodePath(filePath[0], InfReplacementArray)
            
            print('Fetched File information============')
            
            valDecoded = pathInfo

            DirectorysInsideDetailsSingle[1] = (str(valDecoded)+str(filePath[1]))
            for Filter in FiltersArray:
                if Filter !='' and DirectorysInsideDetailsSingle[1].find(str(Filter).strip()) >= 0:
                    flag =False
            
            
            if(projectInformation[0]['ignoreHiddenFiles'] == 1 or projectInformation[0]['ignoreHiddenFiles'] == '1'):
                try:
                    PathExploded = str(DirectorysInsideDetailsSingle[1]).split(str(os.sep))
                    lastIndexName = PathExploded[len(PathExploded) - 1]

                    if fnmatch.fnmatch(lastIndexName, '.*'):
                        flag = False
                        
                    if isThisFileHidden(DirectorysInsideDetailsSingle[1]):
                        flag = False
                        
                except Exception as Excep:
                    print('fnmatch 865 FC')
                    print(Excep[0])

                try:
                    
                    PathExploded = str(DirectorysInsideDetailsSingle[1]).split(str(os.sep))
                    
                    for SingleDirtory in PathExploded:
                        if fnmatch.fnmatch(SingleDirtory, '.*'):
                            flag = False
                            
                        if isThisFileHidden(SingleDirtory):
                            flag = False
                            
                except Exception as Excep:
                    print('PathExploded 873 FC')
                    print(Excep[0])

            if flag:
                check+= 1
                try:
                    response = []
                    print('Verify Using Inode:::::'+file )
                    response = verify_using_inode(dict,dict_Hash,dict_File, DirectorysInsideDetailsSingle , file , Algorithm)
                    
                    if not response or len(response) < 1:
                            continue
                    print('Response from Verification=====')
                except Exception as Excep :
                    moreInformation = {"moreInfo":'null'}
                    try:
                        if not Excep[0] is None:
                            moreInformation['LogsMore'] =str(Excep[0])
                    except Exception as Excep1:
                        print(Excep1[0])
                        
                    try:
                        if not Excep[1] is None:
                            moreInformation['LogsMore1'] =str(Excep[1])
                    except Exception as Excep2:
                        print(Excep2[0])


                    Debugging.tureDebugerOn()
                    Debugging.logError('Error Reporting Line 500 FixityCore While Verfiying file status' +str(file)+' '+'||'+str(DirectorysInsideDetailsSingle[0])+'||'+'||'+str(DirectorysInsideDetailsSingle[1])+' '+'||'+str(DirectorysInsideDetailsSingle[2])+'||'+"\n", moreInformation)
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

                except Exception as Excep:
                    print('corruptedOrChanged 920 FC')
                    print(Excep[0])
                
                pathCode = getPathCode(str(SingleDirectory),InfReplacementArray)
                pathID = getPathId(str(SingleDirectory),InfReplacementArray)
                
                try:
                    newCodedPath = str(response[0][1]).replace(SingleDirectory, pathCode+"||")
                except Exception as Excep:
                    newCodedPath = ' '
                    print('newCodedPath 929 FC')
                    print(Excep[0])
                try:
                    
                    print('----Saving Details For :' + str(newCodedPath))
                    versionDetailOptions = {}
                    
                    versionDetailOptions['hashes'] = str(response[0][0])
                    versionDetailOptions['path'] = newCodedPath
                    versionDetailOptions['inode'] = str(response[0][2])
                    versionDetailOptions['versionID'] = str(versionID['id'])
                    versionDetailOptions['projectID'] = projectInformation[0]['id']
                    versionDetailOptions['projectPathID'] = pathID
                    DB.insert(DB._tableVersionDetail, versionDetailOptions)
                    
                except Exception as excp:
                    print('versionDetailOptions 946 FC')
                    print(excp[0])
                    pass
                
                try:
                    HistoryFile.write(str(response[0][0]) + "\t" + str(response[0][1]) + "\t" + str(response[0][2]) + "\n")
                except Exception as excp:
                    print('HistoryFile 955 FC')
                    print(excp[0])
                    pass
                
            print('')
            print('================================================================================')
            print('')
    try:
        missingFile = missing(dict_Hash,SingleDirectory)
        FileChangedList += missingFile[0]
        
        try:
            if missingFile[1] > 0:
                flagAnyChanges = True
        except:
            pass
        
    except Exception as Excep:
        print('missing 965 FC')
        print(Excep)
        pass

    informationToUpate = {}
    informationToUpate['versionCurrentID'] = versionID['id']
    DB.update(DB._tableProject, informationToUpate, "id='" + str(projectInformation[0]['id']) + "'")
    
    print('===== Updating Project Information =====')
    
    cpyProjectPathInformation  = projectPathInformation
    for PDI in cpyProjectPathInformation:
        del cpyProjectPathInformation[PDI]['id']
        cpyProjectPathInformation[PDI]['versionID'] = versionID['id']
        DB.insert(DB._tableProjectPath, cpyProjectPathInformation[PDI])
    try:
        HistoryFile.close()
    except Exception as Excep:
            print('HistoryFile 983 FC')
            print(Excep[0])


    information = str(file).split('\\')
    projectName = information[(len(information)-1)]
    projectName = str(projectName).split('.')
    
    total =  confirmed
    total += moved
    total += created
    total += corruptedOrChanged
    
    print('checking for missing files FC')
    try:
        total += missingFile[1]
    except:
        missingFile = ('','')
        pass
    
    try:
        HistoryFile.close()
    except Exception as Excep:
            print('HistoryFile 1005 FC')
            print(Excep[0])
    
    ProjectName = file.replace('.fxy','').replace('projects\\','')
    ProjectName = ProjectName.replace('.fxy','').replace('projects//','')
    ProjectName = ProjectName.replace('.fxy','').replace('//','/')
    ProjectName = ProjectName.replace('.fxy','').replace('projects/','')
    ProjectName = ProjectName.replace('.fxy','').replace('\\\\','\\')
    
    repath = writer(Algorithm, ProjectName , total, confirmed, moved, created, corruptedOrChanged, missingFile[1], FileChangedList,projectName)

    try:
        lock.release()
        print('relased the file')
    except Exception as Excep:
            print('release 1020 FC')
            print(Excep[0])
    if checkForChanges:
        return flagAnyChanges , repath
    
    return confirmed, moved, created, corruptedOrChanged , missingFile[1], repath



'''
Path Encoding to a Code To Identify the Path of each file
'''
def pathCodeEncode(pathStr):
    return 'Fixity-'+str(pathStr)


'''
Path decoding to a Path From Encoded Code To Identify the Path of each file
'''
def pathCodedecode(code):
    return base64.b64decode(code)


'''
Verify File Changes
'''
def getCodePath(code , InfReplacementArray):
    for single in InfReplacementArray:
        if InfReplacementArray[single]['code'] == code:
            return single

'''
Get Code using Path
'''
def getPathCode(path , InfReplacementArray):
    for single in InfReplacementArray:
        if InfReplacementArray[single]['path'] == path:
            return InfReplacementArray[single]['code']


'''
Get Path Id using path
'''
def getPathId(path , InfReplacementArray):
    for single in InfReplacementArray:
        if InfReplacementArray[single]['path'] == path:
            return InfReplacementArray[single]['id']


'''
Get Path Id using path
'''
def getCodePathMore(code , InfReplacementArray):
    for single in InfReplacementArray:
        if InfReplacementArray[single]['code'] and InfReplacementArray[single]['code'] is not None and InfReplacementArray[single]['code'] == code:
            return InfReplacementArray[single]


'''
Get Directory Detail
'''
def getDirectoryDetail(projectName ,fullpath = False):

    DirectoryDetail = [[],[],[],[],[],[],[],[]]
    if fullpath:
        projfile = open(fullpath, 'rb')

    else:
        projfile = open('projects\\' + projectName + '.fxy', 'rb')

    allProjectDirectoryList = projfile.readline()
    projectDirectoryList = allProjectDirectoryList.split(';')
    for  SigleDir in projectDirectoryList:
        if SigleDir is not None and SigleDir != '' and ('|-|-|' in SigleDir):
            detialInformation = str(SigleDir).split('|-|-|')
            
            if detialInformation[2] is not None and detialInformation[2] !='' :
                indexOfDet = int(detialInformation[2])
                DirectoryDetail[indexOfDet] = detialInformation

    projfile.close()
    return DirectoryDetail


def EncodeInfo(stringToBeEncoded):
    stringToBeEncoded = str(stringToBeEncoded).strip()
    return base64.b16encode(base64.b16encode(stringToBeEncoded))

def DecodeInfo(stringToBeDecoded):
    stringToBeDecoded = str(stringToBeDecoded).strip()
    return base64.b16decode(base64.b16decode(stringToBeDecoded))

'''Get Fixity Home Path'''
def getFixityHomePath():
    pathInfo = str(getcwd()).replace(str(os.sep)+'Contents'+str(os.sep)+'Resources','')
    pathInfo = str(pathInfo).replace('Fixity.app'+str(os.sep), '')
    pathInfo = str(pathInfo).replace('Fixity.app', '')
        
    return pathInfo



'''
Method to create (hash, path, id) tables from file root

@param Input: root, output (boolean), hash algorithm, QApplication
@param Output: list of tuples of (hash, path, id)

@return:  List - List of scanned Directory
'''
def quietTable(DirectortPathToBeScanned, AlgorithumUsedForThisProject , InfReplacementArray = {} , projectName = ''):

    listOfValues = []
    fls = []

    try:
        for root, subFolders, files in walk(r''+DirectortPathToBeScanned):

            for Singlefile in files :
                
                print('Getting File :::'+str(Singlefile))
                if OS_Info == 'Windows':
                    Singlefile = scpecialCharacterHandler(Singlefile)
                fls.append(path.join(root, Singlefile))
    
    except Exception as Excep:
  
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
  
            
            Debugging.tureDebugerOn()
            Debugging.logError('Error Reporting Line 140-143 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)
            pass


    try:
        for f in xrange(len(fls)):

            print('Listing:::'+str(fls[f]))

            pathOftheFile = r''+path.abspath(fls[f])
            EcodedBasePath = InfReplacementArray[DirectortPathToBeScanned]['code']
            givenPath = str(pathOftheFile).replace(DirectortPathToBeScanned, EcodedBasePath + '||')            
            hashOfThisFileContent = fixity(pathOftheFile, AlgorithumUsedForThisProject , projectName)
            
            
            if(OS_Info == 'Windows'):
                i = FixityCoreWin.ntfsIDForWindows(pathOftheFile)
            else:
                i = FixityCoreMac.ntfsIDForMac(pathOftheFile)
            listOfValues.append((hashOfThisFileContent, givenPath, i))
        

    except Exception as Excep:

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

            
            Debugging.tureDebugerOn()
            Debugging.logError('Error Reporting Line 169-183 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)

            pass

    return listOfValues

''' 
Check weather this file is Hidden or Not
@param pathOfFile: Path Of File or Directory to be checked

@return: 0 if hidden and 2 if not in windows and in MAC true if hidden and false if not
''' 
def isThisFileHidden(pathOfFile):
    if os.name== 'nt':
        '''Windows Condition'''
        attribute = win32api.GetFileAttributes(pathOfFile)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        '''linux'''
        return pathOfFile.startswith('.') 