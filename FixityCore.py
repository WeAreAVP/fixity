# -*- coding: UTF-8 -*-

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

if(OS_Info == 'Windows'):
    import win32file

import shutil
import base64
import unicodedata

'''
Custom Library
'''
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
Checksum generation method
Input: Filepath, algorithm
Output: Hexadecimal value of hashed file


'''
def fixity(filePath, Algorithm , projectName= None):
    moreInformation= {}

    try:
        fixmd5 = hashlib.md5()
        fixsha256 = hashlib.sha256()
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


        Debugging.tureDebugerOn()
        Debugging.logError('Error Reporting Line 36 - 40 While encrypting File into hashes using Algo:' + str(Algorithm)  +" File FixtyCore\n", moreInformation)

        pass
    try:
        with open(filePath, 'rb') as target:

            for piece in iter(lambda: target.read(4096), b''):
                fixmd5.update(piece)
                fixsha256.update(piece)

            target.close()
            return {'md5':fixmd5.hexdigest() , 'sha256':fixsha256.hexdigest()}
    except Exception as e:


        moreInformation = {"moreInfo":'none'}
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
File ID for NTFS
Returns the complete file ID as a single long string
(volume number, high index, low index)
'''
def ntfsIDForWindows(filePath):
    id = '';
    try:
        target = open(filePath, 'rb')
    except Exception as e:
        moreInformation = {"moreInfo":'none'}
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
        Debugging = Debuger()
        Debugging.tureDebugerOn()
        Debugging.logError('Error Reporting Line 106 - 108 While reading file to Creating INode for File :' + str(filePath)  +" File FixtyCore\n", moreInformation)
        pass
    try:
        id = str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[4]) + \
            str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[8]) + \
            str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[9])
        return id
    except Exception as e:


            moreInformation = {"moreInfo":'none'}
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
            Debugging = Debuger()
            Debugging.tureDebugerOn()
            Debugging.logError('Error Reporting Line 89 - 95 While Creating INode for File :' + str(filePath)  +" File FixtyCore\n", moreInformation)
            pass
    return id



'''
File ID for NTFS
Returns the complete file ID as a single long string
(volume number, high index, low index)
'''

def ntfsIDForMac(f):
    id=''
    try:
        target = os.open(u''+f , os.O_RDWR|os.O_CREAT )
        # Now get  the touple
        info = os.fstat(target)
        id = str(info.st_ino)

        os.close(target)
        return id

    except Exception as e:

        moreInformation = {"moreInfo":'none'}
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

        try:
            target.close()
        except:
            pass
        Debugging.tureDebugerOn()
        Debugging.logError('Error Reporting Line 89 - 95 While Creating INode for File :' + str(f)  +" File FixtyCore\n", moreInformation)

        pass
    return id



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
                        ThisInode = str(ntfsIDForWindows(path.join(root, SingleFile)))
                    else:
                        ThisInode = str(ntfsIDForMac(path.join(root, SingleFile)))
                    if  ThisInode == Inode:
                        return Inode
        return True
    except:
        return True


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
        for root, subFolders, files in walk(u''+DirectortPathToBeScanned):
            for Singlefile in files:
                print('scanning:::'+str(Singlefile))
                fls.append(path.join(root, u''+Singlefile))

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


            Debugging.tureDebugerOn()
            Debugging.logError('Error Reporting Line 140-143 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)
            pass


    try:
        for f in xrange(len(fls)):

            print('Listing:::'+str(fls[f]))

            pathOftheFile = path.abspath(u''+fls[f])

            EcodedBasePath = InfReplacementArray[DirectortPathToBeScanned]['code']

            givenPath = u''+str(pathOftheFile).replace(DirectortPathToBeScanned, EcodedBasePath + '||')

            h = fixity(pathOftheFile, AlgorithumUsedForThisProject , projectName)
            if(OS_Info == 'Windows'):
                i = ntfsIDForWindows(pathOftheFile)
            else:
                i = ntfsIDForMac(pathOftheFile)
            listOfValues.append((h, u''+givenPath, i))


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


            Debugging.tureDebugerOn()
            Debugging.logError('Error Reporting Line 169-183 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)

            pass

    return listOfValues



'''
Method to convert database line into tuple
@param line: Information of a single File

@return tuple: (hash, abspath, id)
'''
def toTuple(line):

    try:
        return [line['ssh256_hash'], line['path'].strip(), line['inode']]
    except Exception as e:

        Debugging.tureDebugerOn();
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
        Debugging.tureDebugerOn()
        Debugging.logError('Error Reporting Line 148-150 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)

        return None



'''
Method to generate a dictionary, keyed to file hashes
This is done to greatly speed up the eventual fixity checks
@param file: Database file
@return : defaultdict keyed to hash values
'''
def buildDict(file):

    try:

        table = open(file, 'r')
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
    except Exception as e:

        Debugging.tureDebugerOn();
        moreInformation = {"moreInfo":'null'}
        try:
            if not e[0] == None:
                moreInformation['LogsMore'] =str(e[0])
        except:
            pass
        try:
            if not e[1] == None:
                table.close()

                moreInformation['LogsMore1'] =str(e[1])
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
    print('verifying:::'+str(line[1]))

    try:
        CurrentDirectory = dicty.get(line[2])
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
        Debugging.tureDebugerOn()
        Debugging.logError('Error Reporting Line 250 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)
        pass

    if path.isfile(u''+line[1]):

        if CurrentDirectory != None :

            CurrentDirectory = CurrentDirectory[0]
            isHashSame , isFilePathSame = '' , ''

            # Check For File Hash Change
            isHashSame = (CurrentDirectory[1] == line[0][Algorithm])

            # Check For File Path Change
            isFilePathSame = (CurrentDirectory[0] == line[1])

            if isHashSame and isFilePathSame:
                verifiedFiles.append(line[1])
                return line, "Confirmed File :\t" + str(line[1])
            if isHashSame and (not isFilePathSame):
                verifiedFiles.append(line[1])
                verifiedFiles.append(CurrentDirectory[0])
                return line, "Moved or Renamed File :\t" + str(CurrentDirectory[0]) + "\t changed to\t" + str(line[1])
            if (not isHashSame) and isFilePathSame:

                verifiedFiles.append(line[1])
                return line, "Changed File :\t" + str(line[1])

            if (not isHashSame) and (not isFilePathSame):
                print(line)
                print(CurrentDirectory)
                verifiedFiles.append(line[1])
                verifiedFiles.append(CurrentDirectory[0])
                return line, "Changed File :\t" + str(line[1])

        else :

            CurrentDirectory = []

            for dictionarySingle in dictHash:
                allInforHashRelated = dictHash[dictionarySingle]
                for singleInforHashRelated in allInforHashRelated:
                    # Y     Y    Y     N    Confirmed File
                    if singleInforHashRelated[0] == line[1] and dictionarySingle == line[0][Algorithm]:
                        verifiedFiles.append(line[1])
                        return line, "Confirmed File :\t" + str(line[1])

                    # Y     N    Y    N    Changed File
                    elif singleInforHashRelated[0] == line[1] and dictionarySingle != line[0][Algorithm]:
                        verifiedFiles.append(line[1])
                        return line, 'Changed File :\t' + str(line[1])

            for dictionarySingle1 in dictHash:
                allInforHashRelated1 = dictHash[dictionarySingle1]
                for singleInforHashRelated1 in allInforHashRelated1:
                    if singleInforHashRelated1[0] == line[1] :
                        verifiedFiles.append(line[1])
                        return line, "Moved or Renamed :\t" + line[1]
        verifiedFiles.append(line[1])
        return line, 'New File :\t' + str(line[1])





'''
Writes report about the most recent fixity check
Input: algorithm used, start time, directories scanned, number of files found, good files, warned files, bad files, missing files, [out?], current time, old DB, new DB
Output: All this, written nicely to a tab-delimited file, with the filepath returned

@param algoUsed: Algorithum used for the project to record changes
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

        report += str(DetailOutputOfAllFilesChanges)
        print(report)
        if(OS_Info == 'Windows'):
            AutiFixPath = (getcwd()).replace('schedules','').replace('\\\\',"\\")
            rn = AutiFixPath+str(os.sep)+'reports'+str(os.sep)+'fixity_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S')) + '_' + str(projectName[0])  + '.tsv'
        else:

            AutiFixPath = (getcwd()).replace('schedules','').replace('//',"/")
            NameOfFile = str(projectName[1]).split('/')

            NameOfFile[(len(NameOfFile)-1)]

            pathInfo = str(getcwd()).replace(str(os.sep)+'Contents'+str(os.sep)+'Resources','')
            pathInfo = str(pathInfo).replace('Fixity.app'+str(os.sep), '')
            pathInfo = str(pathInfo).replace('Fixity.app', '')
            createPath = str(pathInfo).replace(' ', '\\ ')

            if not os.path.isdir( str(createPath) + 'reports' ):
                try:
                    os.mkdir( str(createPath) + 'reports' )
                except Exception as ex:
                    print(ex[0])

            rn = str(pathInfo)+'reports'+str(os.sep)+'fixity_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S')) + '_' + str(NameOfFile[(len(NameOfFile)-1)])  + '.tsv'
            try:
                rn = str(rn).replace(' ', '\\ ')
            except Exception as Ex:
                print(Ex[0])


        r = open(rn, 'w+')
        r.write(report)
        r.close()
    except Exception as e:
        print(e[0])

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
    # walks through the dict and returns all False flags
    for keys in dict:
        for obj in dict[keys]:

            if not path.isfile(obj[0]):
                #check if file already exists in the manifest
                if not obj[0] in verifiedFiles:
                    verifiedFiles.append(obj[0])
                    msg += "Removed Files\t" + obj[0] +"\n"
                    count = count + 1

    return msg, count



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

    if(projectDetailInformation != None):
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

        historyFile = getcwd()+str(os.sep)+'history'+str(os.sep)+str(projectName).replace('.fxy', '')+str(datetime.date.today())+'-'+str(datetime.datetime.now().strftime('%H%M%S'))+'.tsv'
    else:

        pathInfo = str(getcwd()).replace(str(os.sep)+'Contents'+str(os.sep)+'Resources','')
        pathInfo = str(pathInfo).replace('Fixity.app'+str(os.sep), '')
        pathInfo = str(pathInfo).replace('Fixity.app', '')

        createPath = str(pathInfo).replace(' ', '\\ ')

        if  not os.path.isdir(str(createPath)+'history') :
            try:
                os.mkdir(str(createPath)+'history')
            except:
                pass

        historyFile = str(pathInfo) + 'history' + str(os.sep)+str(projectName).replace('.fxy', '')+str(datetime.date.today())+'-'+str(datetime.datetime.now().strftime('%H%M%S'))+'.tsv'
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
        ToBeScannedDirectoriesInProjectFile.append(str(projectPathInformation[pathInfo]['path']))
        IdInfo =str(projectPathInformation[pathInfo]['pathID']).split('-')
        InfReplacementArray[projectPathInformation[pathInfo]['path'].strip()]= {'path':str(projectPathInformation[pathInfo]['path']),'code':str(projectPathInformation[pathInfo]['pathID']) ,'number': str(IdInfo[1]),'id':projectPathInformation[pathInfo]['id']}

    mails = str(projectInformation[0]['emailAddress']).split(',')
    print('writing ::: Stared Worked')
    check = 0
    for l in projectDetailInformation:

        try:
            x = toTuple(projectDetailInformation[l])

            if x != None and x:
                pathInformation = str(x[1]).split('||')
                if pathInformation:
                    CodeInfoormation=''
                    CodeInfoormation = pathInformation[0]

                    pathInfo = getCodePathMore(CodeInfoormation ,InfReplacementArray)
                    dict[x[2]].append([pathInfo['path']+pathInformation[1], x[0], False])
                    dict_Hash[x[0]].append([pathInfo['path']+pathInformation[1], x[2], False])
                    dict_File[pathInfo['path']+pathInformation[1]].append([x[0], x[2], False])

        except Exception as ex :

            moreInformation = {"moreInfo":'null'}
            try:
                if not ex[0] == None:
                    moreInformation['LogsMore'] =str(ex[0])
            except Exception as ex:
                print(ex[0])
            try:
                if not ex[1] == None:
                    moreInformation['LogsMore1'] =str(ex[1])
            except Exception as ex:
                print(ex[0])
            try:
                moreInformation['directoryScanning']
            except:
                moreInformation['directoryScanning'] = ''
            for SingleVal in ToBeScannedDirectoriesInProjectFile:
                moreInformation['directoryScanning']= str(moreInformation['directoryScanning']) + "\t \t"+str(SingleVal)


            Debugging.tureDebugerOn()
            Debugging.logError('Error Reporting 615  - 621 File FixityCore While inserting information'+"\n", moreInformation)

    try:
        ToBeScannedDirectoriesInProjectFile.remove('\n')
    except Exception as ex:
                print(ex[0])
    flagAnyChanges = False

    Algorithm = str(projectInformation[0]['selectedAlgo'])

    counter = 0
    thisnumber = 0
    CurrentDate = time.strftime("%Y-%m-%d")
    Information = {}
    Information['versionType'] = 'save'
    Information['name'] = EncodeInfo(str(CurrentDate))
    versionID  = DB.insert(DB._tableVersions, Information)

    try:
        HistoryFile.write(str(first)+"\n")
        HistoryFile.write(str(projectInformation[0]['emailAddress'])+"\n")
    except:
        pass
    keeptime = ''
    keeptime += str(projectInformation[0]['durationType'])
    keeptime +=' ' + str(projectInformation[0]['lastRan'])

    if int(projectInformation[0]['durationType']) == 3 :
        keeptime += ' 99 99'
    elif int(projectInformation[0]['durationType']) == 2 :
        keeptime += ' 99 '+str(projectInformation[0]['runDayOrMonth'])
    elif int(projectInformation[0]['durationType']) == 1 :
        keeptime += ' ' + str(projectInformation[0]['runDayOrMonth']) + ' 99'
    try:
        HistoryFile.write(keeptime+"\n")
        HistoryFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    except Exception as ex:
            print(ex[0])




    '''
    Running Scrpit against all given directory in given project
    '''

    for SingleDirectory in ToBeScannedDirectoriesInProjectFile:
        '''
        Getting all files and directory  in side "SingleDirectory" with detail information (inode, path and file hash)
        '''
        DirectorysInsideDetails = quietTable(SingleDirectory, Algorithm,InfReplacementArray , projectName)

        for e in DirectorysInsideDetails:

            thisnumber=thisnumber+1
            flag =True
            e = list(e)
            filePath = str(e[1]).split('||')
            pathInfo = getCodePath(filePath[0], InfReplacementArray)

            valDecoded = pathInfo

            e[1] = (str(valDecoded)+str(filePath[1]))
            for Filter in FiltersArray:
                if Filter !='' and e[1].find(str(Filter).strip()) >= 0:
                    flag =False

            if OS_Info == 'linux':
                    if(projectInformation[0]['ignoreHiddenFiles'] == 1 or projectInformation[0]['ignoreHiddenFiles'] == '1'):
                        try:
                            PathExploded = str(e[1]).split(str(os.sep))
                            lastIndexName = PathExploded[len(PathExploded) - 1]

                            if fnmatch.fnmatch(lastIndexName, '.*'):
                                flag = False
                        except Exception as ex:
                            print(ex[0])

                        try:
                            PathExploded = str(e[1]).split(str(os.sep))
                            for SingleDirtory in PathExploded:
                                if fnmatch.fnmatch(SingleDirtory, '.*'):
                                    flag = False
                        except Exception as ex:
                            print(ex[0])


            if flag:
                check+= 1
                try:
                    response = []
                    print('Verify Using Inode:::::'+file )
                    response = verify_using_inode(dict,dict_Hash,dict_File, e , file , Algorithm)

                    if not response or len(response) < 1:
                            continue

                except Exception as ex :
                    moreInformation = {"moreInfo":'null'}
                    try:
                        if not ex[0] == None:
                            moreInformation['LogsMore'] =str(ex[0])
                    except Exception as ex:
                        print(ex[0])
                    try:
                        if not ex[1] == None:
                            moreInformation['LogsMore1'] =str(ex[1])
                    except Exception as ex:
                        print(ex[0])


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

                except Exception as ex:
                    print(ex[0])

                pathCode = getPathCode(str(SingleDirectory),InfReplacementArray)
                pathID = getPathId(str(SingleDirectory),InfReplacementArray)
                try:
                    newCodedPath = str(response[0][1]).replace(SingleDirectory, pathCode+"||")
                except Exception as ex:
                    print(ex[0])

                versionDetailOptions = {}
                try:
                    versionDetailOptions['md5_hash'] = str(response[0][0]['md5'])
                    versionDetailOptions['ssh256_hash'] = str(response[0][0]['sha256'])
                    versionDetailOptions['path'] = newCodedPath
                    versionDetailOptions['inode'] = str(response[0][2])
                    versionDetailOptions['versionID'] = str(versionID['id'])
                    versionDetailOptions['projectID'] = projectInformation[0]['id']
                    versionDetailOptions['projectPathID'] = pathID
                    DB.insert(DB._tableVersionDetail, versionDetailOptions)
                except:
                    print(e[0])
                    pass
                try:
                    if(Algorithm == 'md5'):
                        HistoryFile.write(str(response[0][0]['md5']) + "\t" + str(response[0][1]) + "\t" + str(response[0][2]) + "\n")
                    else:
                        HistoryFile.write(str(response[0][0]['sha256']) + "\t" + str(response[0][1]) + "\t" + str(response[0][2]) + "\n")
                except:
                    print(e[0])
                    pass


    try:
        missingFile = missing(dict_Hash,SingleDirectory)
        FileChangedList += missingFile[0]
    except Exception in e:
        print(e)
        pass

    informationToUpate = {}
    informationToUpate['versionCurrentID'] = versionID['id']
    DB.update(DB._tableProject, informationToUpate, "id='" + str(projectInformation[0]['id']) + "'")
    cpyProjectPathInformation  = projectPathInformation

    for PDI in cpyProjectPathInformation:
        del cpyProjectPathInformation[PDI]['id']
        cpyProjectPathInformation[PDI]['versionID'] = versionID['id']
        DB.insert(DB._tableProjectPath, cpyProjectPathInformation[PDI])
    try:
        HistoryFile.close()
    except Exception as ex:
            print(ex[0])


    information = str(file).split('\\')
    projectName = information[(len(information)-1)]
    projectName = str(projectName).split('.')

    total = confirmed
    total +=moved
    total +=created
    total +=corruptedOrChanged

    try:
        total += missingFile[1]
    except:
        missingFile = ('','')
        pass
    try:
        HistoryFile.close()

    except Exception as ex:
            print(ex[0])

    ProjectName = file.replace('.fxy','').replace('projects\\','')
    ProjectName = ProjectName.replace('.fxy','').replace('projects//','')
    ProjectName = ProjectName.replace('.fxy','').replace('//','/')
    ProjectName = ProjectName.replace('.fxy','').replace('projects/','')
    ProjectName = ProjectName.replace('.fxy','').replace('\\\\','\\')

    repath = writer(Algorithm, ProjectName , total, confirmed, moved, created, corruptedOrChanged, missingFile[1], FileChangedList,projectName)

    try:
        lock.release()
        print('relased the file')
    except Exception as ex:
            print(ex[0])
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
        if InfReplacementArray[single]['code'] and InfReplacementArray[single]['code'] != None and InfReplacementArray[single]['code'] == code:
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
        if SigleDir !=None and SigleDir != '' and ('|-|-|' in SigleDir):
            detialInformation = str(SigleDir).split('|-|-|')
            if detialInformation[2] != None and detialInformation[2] !='' :
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

#projects_path = getcwd()+'\\projects\\'
#run(projects_path+'New_Project.fxy','','New_Project')
