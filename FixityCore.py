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
import os
OS_Info = ''
if os.name == 'posix':
    OS_Info = 'linux'
elif os.name == 'nt':
    OS_Info = 'Windows'
elif os.name == 'os2':
    OS_Info = 'check'


if(OS_Info == 'Windows'):
    import win32file

import shutil
import base64
import unicodedata
#Custom
from Debuger import Debuger
from EmailPref import EmailPref
from Database import Database
global verifiedFiles
verifiedFiles = []

# Checksum generation method
# Input: Filepath, algorithm
# Output: Hexadecimal value of hashed file
def fixity(f, Algorithm , projectName= None):
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

        Debugging = Debuger()
        Debugging.tureDebugerOn()
        Debugging.logError('Error Reporting Line 36 - 40 While encrypting File into hashes using Algo:' + str(Algorithm)  +" File FixtyCore\n", moreInformation)

        pass
    try:
        with open(f, 'rb') as target:

            for piece in iter(lambda: target.read(4096), b''):
                fixmd5.update(piece)
                fixsha256.update(piece)
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

        Debugging = Debuger()
        Debugging.tureDebugerOn()
        Debugging.logError('Error Reporting Line 59 - 63 While encrypting File into hashes using Algo:' + str(Algorithm)  +" File FixtyCore\n", moreInformation)
        pass


# Get information from Project File matched with given information
# ProjectPath: Project File path to be scaned
# hash: search this hash from given Project File
# path: search this path from given Project File
# inode: search this inode from given Project File
def getFileInformationConditional(ProjectPath ,hashVal='',path='',inode=''):
    Information=[]
    try:
        editedPadth = path.replace('\\\\','\\')
        f = open(ProjectPath)
        content = f.readlines()
        for singleLine in content:
            if ( hashVal in str(singleLine) or hashVal == '' ) and ( inode in str(singleLine) or inode == '' ) and ( path in str(singleLine) or editedPadth in str(singleLine) or path == ''  ):
                Information.append(singleLine)
        return Information
    except:
        return Information

# File ID for NTFS
# Returns the complete file ID as a single long string
# (volume number, high index, low index)
def ntfsID(f):
    id=''
    try:
        target = os.open(u''+f , os.O_RDWR|os.O_CREAT )
        # Now get  the touple
        info = os.fstat(target)
        # Now get uid of the file
        id = str(info.st_ino)
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
        Debugging.logError('Error Reporting Line 89 - 95 While Creating INode for File :' + str(f)  +" File FixtyCore\n", moreInformation)

        pass
    return id

# Params:
# Path : Path of the Directory
# Inode: Inode To Be Searched
#
# Description:
# scan given path and searches for the File which have this given Inode

def GetDirectoryInformationUsingInode(Path,Inode):
    try:
        if Path and Inode:
            for root, subFolders, files in walk(Path):
                for SingleFile in files:
                    path.join(root, SingleFile)
                    ThisInode = str(ntfsID(path.join(root, SingleFile)))
                    if  ThisInode == Inode:
                        return Inode
        return True
    except:
        return True

# Method to create (hash, path, id) tables from file root
# Input: root, output (boolean), hash algorithm, QApplication
# Output: list of tuples of (hash, path, id)
def quietTable(r, a , InfReplacementArray = {} , projectName = ''):

    listOfValues = []
    fls = []
    try:
        for root, subFolders, files in walk(u''+r):
            for Singlefile in files:
#                 print('Listing File: '+str(Singlefile))
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

            Debugging = Debuger();
            Debugging.tureDebugerOn()
            Debugging.logError('Error Reporting Line 140-143 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)
            pass

    try:
        for f in xrange(len(fls)):

            p = path.abspath(u''+fls[f])

            EcodedBasePath = InfReplacementArray[r]['code']
            print('Getting File Information of File: '+str(p))
            givenPath = u''+str(p).replace(r, EcodedBasePath + '||')

            h = fixity(p, a , projectName)
            i = ntfsID(p)

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

            Debugging = Debuger();
            Debugging.tureDebugerOn()
            Debugging.logError('Error Reporting Line 169-183 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)

            pass

    return listOfValues

# Method to convert database line into tuple
# Input: tab-delimited line from database file
# Output: tuple: (hash, abspath, id)
def toTuple(line):

    try:
        return [line['ssh256_hash'], line['path'].strip(), line['inode']]
    except Exception as e:
        Debugging = Debuger();
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

# Method to generate a dictionary, keyed to file hashes
# This is done to greatly speed up the eventual fixity checks
# Input: Database file
# Output: defaultdict keyed to hash values
def buildDict(file):

    try:

        table = open(file, 'r')
        db = defaultdict(list)
        for line in table.readlines():
            x = toTuple(line)
            db[x[0]].append([x[1], x[2], False])
        return db
    except Exception as e:
        Debugging = Debuger();
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
        Debugging.logError('Error Reporting Line 173-179 FixityCore While building directory and files FixityCore' +"\n", moreInformation)

        return None

# Writes table to file
# Input: filepath, table (list of tuples from toTuple)
# Output: A nicely written file
def tableToFile(path, listOfValue):
    f = open(path, 'w')
    for item in listOfValue:
        x = str(item[0]) + "\t" + str(item[1]) + "\t" + str(item[2])
        f.write("%s\n" % x)
    f.close()
    return

# Writes one tuple to file
# Input: filepath, tuple (hash, path, id)
# Output: file has one new line
def tupleToFile(path, t):
    f = open(path, 'a')
    x = str(t[0]) + "\t" + str(t[1]) + "\t" + str(t[2])
    f.write("%s\n" % x)
    f.close()
    return

def getHash(string):
    newString = str(string)[2:66]
    return newString

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


def verify_using_inode (dicty, dictHash, dictFile, line, fileNamePath='' , dctValue = '',Algorithm='sha256'):
    global verifiedFiles

    try:
        CurrentDirectory = dicty.get(line[2])
    except Exception as e:
        Debugging = Debuger();
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
                return line, "Moved or Renamed File :\t" + str(CurrentDirectory[0]) + "\t changed to\t" + str(line[1])

                verifiedFiles.append(line[1])
            if (not isHashSame) and isFilePathSame:
                return line, "Changed File :\t" + str(line[1])

            if (not isHashSame) and (not isFilePathSame):
                verifiedFiles.append(line[1])
                return line, "Changed File :\t" + str(line[1])
        else :

            CurrentDirectory = []

            for dictionarySingle in dictHash:
                allInforHashRelated = dictHash[dictionarySingle]
                for singleInforHashRelated in allInforHashRelated:
                    # Y     Y    Y N    Confirmed File
                    if singleInforHashRelated[0] == line[1] and dictionarySingle == line[0][Algorithm]:
                        verifiedFiles.append(line[1])
                        return line, "Confirmed File :\t" + str(line[1])

                    # Y     N    Y N    Changed File
                    elif singleInforHashRelated[0] == line[1] and dictionarySingle != line[0][Algorithm]:
                        verifiedFiles.append(line[1])
                        return line, 'File Changed :\t' + str(line[1])

            for dictionarySingle1 in dictHash:
                allInforHashRelated1 = dictHash[dictionarySingle1]
                for singleInforHashRelated1 in allInforHashRelated1:
                    if singleInforHashRelated1[0] == line[1] :
                        verifiedFiles.append(line[1])
                        return line, "Moved or Renamed :\t" + line[1]
        verifiedFiles.append(line[1])
        return line, 'New File :\t' + str(line[1])

# Method to verify a tuple against the dictionary
# Input: defaultDict (from buildDict), tuple
# Output: Message based on whether the file was good or not

def verify(dict, line, fileNamePath=''):

    # if the hash is a key in the dictionary, return the values
    # returns None on a miss
    # Current Directory Status (Information of this directory using hash from the project file by scanning the directory)
    global verifiedFiles

    CurrentDirectoryStatus = dict.get(line[0])

    copies = ""

    i = 0

    # if we found values, check file attendance (If this file exist)
    if path.isfile(line[1]):
        if CurrentDirectoryStatus != None:
            mainDirectory = getDirectory(CurrentDirectoryStatus,line[2],fileNamePath,dict);
            SingleDirectoryStatus = mainDirectory

            isFilePresent , isSameHash , isSameFilepath , isSameinode = True , True , False , False

            if not SingleDirectoryStatus is None :
                # Check For File INODE Change
                isSameinode = (SingleDirectoryStatus[1] == line[2])

                # Check For File Path Change
                isSameFilepath = (SingleDirectoryStatus[0] == line[1])

                # If Nothing changed
                if isSameFilepath and isSameinode:
                    verifiedFiles.append(line[1])
                    dict[line[0]][i][2] = True
                    return line, "Confirmed Files\t" + str(line[1])

                # If  Path changed But Inode is same
                elif not isSameFilepath and isSameinode:
                    verifiedFiles.append(line[1])
                    dict[line[0]][i][2] = True
                    return line, "Moved or Renamed Files\t" + str(SingleDirectoryStatus[0]) + "\t changed to " + str(line[1])

                # If Inode changed But Path is same
                elif (isSameFilepath and not isSameinode) :
                    verifiedFiles.append(line[1])
                    dict[line[0]][i][2] = True
                    return line, "Confirmed Files\t" + str(line[1])
                # If Inode and Path both changed
                elif (not isSameFilepath and not isSameinode) :
                    verifiedFiles.append(line[1])
                    dict[line[0]][i][2] = True
                    Response = getFileInformationConditional(fileNamePath  ,line[0],line[1])
                    if len(Response) <=0:
                        copies += " " + str(SingleDirectoryStatus[0])
                        return line, "New Files\t" + line[1] + "\tcopy of " + copies
                    else:
                        #check if both manifest , directory file exists in manifest
                        IfFileInLineExistsInMenifest = getFileInformationConditional(fileNamePath  , '' ,str(line[1]))
                        IfMovedFileExistsInMenifest = getFileInformationConditional(fileNamePath  , '' ,str(SingleDirectoryStatus[0]))
                        if len(IfFileInLineExistsInMenifest) > 0 and len(IfMovedFileExistsInMenifest) > 0:
                            verifiedFiles.append(line[1])
                            return line, "Confirmed Files\t" + str(line[1])
                        else:
                            verifiedFiles.append(line[1])
                            return line, "Moved or Renamed Files\t" + str(SingleDirectoryStatus[0]) + "\t changed to " + str(line[1])

                # If File Dose not exist and path exists
                elif not path.isfile(line[1]) and line[2] and line[1]:
                    verifiedFiles.append(line[1])
                    dict[line[0]][i][2] = True
                    return line, "Moved or Renamed Files\t" + str(SingleDirectoryStatus[0]) + "\t changed to " + str(line[1])

                copies += " " + str(SingleDirectoryStatus[0])
                i += 1
                verifiedFiles.append(line[1])
                return line, "New Files\t" + line[1] + "\tcopy of " + copies
            else:
                verifiedFiles.append(line[1])

                return (line[0], line[1], line[2]), "Changed Files\t" + str(line[1])
        # if we don't have a given hash, figure out why
        else:

            # iterate through the dictionary until we find a matching ID and/or path
            isFilePresent , isSameHash , isSameFilepath , isSameinode = False , False , False , False

            for key in dict:

                NewDirectoryStatus = dict.get(key)
                i = 0
                if NewDirectoryStatus:

                    for SingleDirectoryStatus in NewDirectoryStatus:
                        # Check if its the same inode
                        isSameinode = (SingleDirectoryStatus[1] == line[2])

                        # Check For File Path Change
                        isSameFilepath = (SingleDirectoryStatus[0] == line[1])
                        lengthRes = 0
                        try:
                            Response1231 = []
                            Response1231 = getFileInformationConditional(fileNamePath ,'',line[1],line[2])
                            lengthRes = len(Response1231)
                        except:
                            pass

                        # First Condition: If both Path and inode changed
                        # Second Condition: If  Path changed But Inode is same
                        # Third Condition: If  Path same But Inode changed
                        # Found it! Set the found flag as True and return a Changed message
                        if (isSameinode and isSameFilepath) or (isSameinode and (not isSameFilepath)) or ((not isSameinode) and isSameFilepath):
                            dict[key][i][2] = True
                            verifiedFiles.append(SingleDirectoryStatus[0])
                            return (line[0], line[1], line[2]), "Changed Files\t" + str(line[1])
                        elif ( lengthRes and lengthRes > 0 ):
                            dict[key][i][2] = True
                            verifiedFiles.append(SingleDirectoryStatus[0])
                            return (line[0], line[1], line[2]), "Changed Files\t" + str(line[1])

                        i += 1
            verifiedFiles.append(line[1])
            return line, "New File\t" + str(line[1])

# Writes report about the most recent fixity check
# Input: algorithm used, start time, directories scanned, number of files found, good files, warned files, bad files, missing files, [out?], current time, old DB, new DB
# Output: All this, written nicely to a tab-delimited file, with the filepath returned
def writer(alg, proj, num, conf, moves, news, fail, dels, out,projectName=''):
    rn = ''
    try:
        report = "Fixity report\n"
        report += "Project name\t" + proj + "\n"
        report += "Algorithm used\t" + alg + "\n"
        report += "Date\t" + str(datetime.date.today()) + "\n"
        report += "Total Files\t" + str(num) + "\n"
        report += "Confirmed Files\t" + str(conf) + "\n"
        report += "Moved or Renamed Files\t" + str(moves) + "\n"
        report += "New Files\t" + str(news) + "\n"
        report += "Changed Files\t" + str(fail) + "\n"
        report += "Removed Files\t" + str(dels) + "\n"

        report += str(out)
        print(report)
        if(OS_Info == 'Windows'):
            AutiFixPath = (getcwd()).replace('schedules','').replace('\\\\',"\\")
            rn = AutiFixPath+'\\reports\\fixity_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S')) + '_' + str(projectName[0])  + '.csv'
        else:
            AutiFixPath = (getcwd()).replace('schedules','').replace('//',"/")
            NameOfFile = str(projectName[0]).split('/')
            NameOfFile[(len(NameOfFile)-1)]
            rn = AutiFixPath+'/reports/fixity_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S')) + '_' + str(NameOfFile[(len(NameOfFile)-1)])  + '.csv'

        r = open(rn, 'w+')
        r.write(report)
        r.close()
    except Exception as e:
        print(e[0])

    return rn


# Method to find which files are missing in the scanned directory
# Input: defaultdict (from buildDict)
# Output: warning messages about missing files (one long string and printing to stdout)
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
                    count += 1
                    msg += "Removed Files\t" + obj[0] +"\n"

    return msg, count

# Updating/Creating Manifest
# With on the given directory

def run(file,filters='',projectName = '',checkForChanges = False):
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
    historyFile = str(file).replace('projects', 'history')
    historyFile = str(historyFile).replace('.fxy',str(datetime.date.today())+'-'+str(datetime.datetime.now().strftime('%H%M%S'))+'.inf')
    tmp = open(historyFile , 'w')
    first = ''
    for singlePathDF in projectPathInformation:
        first = str(first) + str(projectPathInformation[singlePathDF]['path'])+';'

    ToBeScannedDirectoriesInProjectFile = []

    for pathInfo in projectPathInformation:
        ToBeScannedDirectoriesInProjectFile.append(str(projectPathInformation[pathInfo]['path']))
        IdInfo =str(projectPathInformation[pathInfo]['pathID']).split('-')
        InfReplacementArray[projectPathInformation[pathInfo]['path'].strip()]= {'path':str(projectPathInformation[pathInfo]['path']),'code':str(projectPathInformation[pathInfo]['pathID']) ,'number': str(IdInfo[1]),'id':projectPathInformation[pathInfo]['id']}

    mails = str(projectInformation[0]['emailAddress']).split(',')

    check = 0
    print('1')
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

    Algorithm = str(projectInformation[0]['selectedAlgo'])

    counter = 0
    thisnumber = 0
    CurrentDate = time.strftime("%Y-%m-%d")
    Information = {}
    Information['versionType'] = 'save'
    Information['name'] = EncodeInfo(str(CurrentDate))
    versionID  = DB.insert(DB._tableVersions, Information)

    tmp.write(first+"\n")
    tmp.write(str(projectInformation[0]['emailAddress'])+"\n")

    keeptime = ''
    keeptime += str(projectInformation[0]['durationType'])
    keeptime +=' ' + str(projectInformation[0]['lastRan'])

    if int(projectInformation[0]['durationType']) == 3 :
        keeptime += ' 99 99'
    elif int(projectInformation[0]['durationType']) == 2 :
        keeptime += ' 99 '+str(projectInformation[0]['runDayOrMonth'])
    elif int(projectInformation[0]['durationType']) == 1 :
        keeptime += ' ' + str(projectInformation[0]['runDayOrMonth']) + ' 99'

    tmp.write(keeptime+"\n")
    tmp.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

    for SingleDirectory in ToBeScannedDirectoriesInProjectFile:
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

            if flag:
                check+= 1
                try:

                    response = verify_using_inode(dict,dict_Hash,dict_File, e , file , Algorithm)

                    if not response:
                            continue

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

                pathCode = getPathCode(str(SingleDirectory),InfReplacementArray)
                pathID = getPathId(str(SingleDirectory),InfReplacementArray)

                newCodedPath = str(response[0][1]).replace(SingleDirectory, pathCode+"||")

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
                        tmp.write(str(response[0][0]['md5']) + "\t" + str(response[0][1]) + "\t" + str(response[0][2]) + "\n")
                    else:
                        tmp.write(str(response[0][0]['sha256']) + "\t" + str(response[0][1]) + "\t" + str(response[0][2]) + "\n")
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

    tmp.close()

    information = str(file).split('\\')
    projectName = information[(len(information)-1)]
    projectName = str(projectName).split('.')

    total = confirmed
    total +=moved
    total +=created
    total +=corruptedOrChanged

    try:
        total +=missingFile[1]
    except:
        missingFile = ('','')
        pass

    repath = writer(Algorithm, file.replace('.fxy','').replace('projects\\',''), total, confirmed, moved, created, corruptedOrChanged, missingFile[1], FileChangedList,projectName)
    return confirmed, moved, created, corruptedOrChanged , missingFile[1], repath

#Path Encoding to a Code To Identify the Path of each file
def pathCodeEncode(pathStr):
    return 'Fixity-'+str(pathStr)

#Path decoding to a Path From Encoded Code To Identify the Path of each file
def pathCodedecode(code):
    return base64.b64decode(code)

def getCodePath(code , InfReplacementArray):
    for single in InfReplacementArray:
        if InfReplacementArray[single]['code'] == code:
            return single

def getPathCode(path , InfReplacementArray):
    for single in InfReplacementArray:
        if InfReplacementArray[single]['path'] == path:
            return InfReplacementArray[single]['code']

def getPathId(path , InfReplacementArray):
    for single in InfReplacementArray:
        if InfReplacementArray[single]['path'] == path:
            return InfReplacementArray[single]['id']

def getCodePathMore(code , InfReplacementArray):
    for single in InfReplacementArray:
        if InfReplacementArray[single]['code'] and InfReplacementArray[single]['code'] != None and InfReplacementArray[single]['code'] == code:
            return InfReplacementArray[single]

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

    return DirectoryDetail

# Fetch information related to email configuration
# Triggers
def EncodeInfo(stringToBeEncoded):
    stringToBeEncoded = str(stringToBeEncoded).strip()
    return base64.b16encode(base64.b16encode(stringToBeEncoded))

def DecodeInfo(stringToBeDecoded):
    stringToBeDecoded = str(stringToBeDecoded).strip()
    return base64.b16decode(base64.b16decode(stringToBeDecoded))

## To test Main Functionality
#projects_path = getcwd()+'/projects/'
#run(projects_path+'Fixity0.2.fxy','','Fixity0.2')
# exit()