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
#Built in Library
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

if(OS_Info == 'Windows'):
    import win32file

import shutil
import base64
import unicodedata

#Custom Library
from Debuger import Debuger
from EmailPref import EmailPref
from Database import Database

global verifiedFiles
verifiedFiles = []

Debugging = Debuger()

# Checksum generation method
# Input: Filepath, algorithm
# Output: Hexadecimal value of hashed file
def fixity(f, Algorithm , projectName= None):
    print('fixity')
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
        with open(f, 'rb') as target:
            print('Open '+f+' File')
            for piece in iter(lambda: target.read(4096), b''):
                fixmd5.update(piece)
                fixsha256.update(piece)
            print('closing '+f+' File')
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


# Get information from Project File matched with given information
# ProjectPath: Project File path to be scaned
# hash: search this hash from given Project File
# path: search this path from given Project File
# inode: search this inode from given Project File
def getFileInformationConditional(ProjectPath ,hashVal='',path='',inode=''):
    print('getFileInformationConditional')
    Information=[]
    try:
        editedPadth = path.replace('\\\\','\\')
        f = open(ProjectPath)
        print('Open '+ProjectPath+' File')
        try:
            content = f.readlines()
            for singleLine in content:
                if ( hashVal in str(singleLine) or hashVal == '' ) and ( inode in str(singleLine) or inode == '' ) and ( path in str(singleLine) or editedPadth in str(singleLine) or path == ''  ):
                    Information.append(singleLine)
        except:
            pass
        try:
            f.close()
            print('closing '+ProjectPath+' File')
        except:
            pass
        return Information

    except:

        return Information

# File ID for NTFS
# Returns the complete file ID as a single long string
# (volume number, high index, low index)
def ntfsID(f):
    id=''
    print('ntfsID')
    try:
        target = os.open(u''+f , os.O_RDWR|os.O_CREAT )
        print('Open '+f+' File')
        # Now get  the touple
        info = os.fstat(target)
        # Now get uid of the file
        id = str(info.st_ino)

        os.close(target)
        print('closing '+f+' File')
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
        print(moreInformation)
        try:
            target.close()
            print('closing '+f+' File')
        except:
            pass
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
    print('GetDirectoryInformationUsingInode')
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
    print('quietTable')
    listOfValues = []
    fls = []
    try:
        for root, subFolders, files in walk(u''+r):
            for Singlefile in files:
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

            p = path.abspath(u''+fls[f])

            EcodedBasePath = InfReplacementArray[r]['code']
            #print('Getting File Information of File: '+str(p))
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
    print('buildDict')
    try:

        table = open(file, 'r')
        print('Open '+file+' File')
        db = defaultdict(list)

        for line in table.readlines():
            try:
                x = toTuple(line)
                db[x[0]].append([x[1], x[2], False])
            except:
                pass
        try:
            table.close()
            print('closing '+file+' File')
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
                print('closing '+file+' File')
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
    print('tableToFile')
    f = open(path, 'w')
    print('Open '+path+' File')
    for item in listOfValue:
        x = str(item[0]) + "\t" + str(item[1]) + "\t" + str(item[2])
        f.write("%s\n" % x)
    f.close()
    print('closing '+path+' File')
    return

# Writes one tuple to file
# Input: filepath, tuple (hash, path, id)
# Output: file has one new line
def tupleToFile(path, t):
    print('tupleToFile')
    print('Open '+path+' File')
    f = open(path, 'a')
    print('Open '+path+' File')
    x = str(t[0]) + "\t" + str(t[1]) + "\t" + str(t[2])
    f.write("%s\n" % x)
    f.close()
    print('closing '+path+' File')
    return
#Get hash from list
def getHash(string):
    newString = str(string)[2:66]
    return newString

#Get Directory information
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

#Verify File Changes
def verify_using_inode (dicty, dictHash, dictFile, line, fileNamePath='' , dctValue = '',Algorithm='sha256'):
    print('verify_using_inode')
    global verifiedFiles
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

                verifiedFiles.append(line[1])
            if (not isHashSame) and isFilePathSame:
                verifiedFiles.append(line[1])
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

# Writes report about the most recent fixity check
# Input: algorithm used, start time, directories scanned, number of files found, good files, warned files, bad files, missing files, [out?], current time, old DB, new DB
# Output: All this, written nicely to a tab-delimited file, with the filepath returned
def writer(alg, proj, num, conf, moves, news, fail, dels, out,projectName=''):
    print('writer')
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

        if(OS_Info == 'Windows'):
            AutiFixPath = (getcwd()).replace('schedules','').replace('\\\\',"\\")
            rn = AutiFixPath+str(os.sep)+'reports'+str(os.sep)+'fixity_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S')) + '_' + str(projectName[0])  + '.tsv'
        else:

            AutiFixPath = (getcwd()).replace('schedules','').replace('//',"/")
            NameOfFile = str(projectName[1]).split('/')

            NameOfFile[(len(NameOfFile)-1)]
            rn = AutiFixPath+str(os.sep)+'reports'+str(os.sep)+'fixity_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S')) + '_' + str(NameOfFile[(len(NameOfFile)-1)])  + '.tsv'

        r = open(rn, 'w+')
        print('Open '+rn+' File')
        r.write(report)
        r.close()
        print('closing '+rn+' File')
    except Exception as e:
        print(e[0])

    return rn


# Method to find which files are missing in the scanned directory
# Input: defaultdict (from buildDict)
# Output: warning messages about missing files (one long string and printing to stdout)
def missing(dict,file=''):
    print('missing')
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

    return msg, count

# Updating/Creating Manifest
# With on the given directory

def run(file,filters='',projectName = '',checkForChanges = False):
    print('run')
    global verfiedFiels

    verfiedFiels = []
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

    historyFile = getcwd()+str(os.sep)+'history'+str(os.sep)+str(projectName).replace('.fxy', '')+str(datetime.date.today())+'-'+str(datetime.datetime.now().strftime('%H%M%S'))+'.tsv'
    print('Open '+historyFile+' File')
    HistoryFile = open(historyFile , 'w+')
    print('closing '+historyFile+'File')
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

    HistoryFile.write(str(first)+"\n")
    HistoryFile.write(str(projectInformation[0]['emailAddress'])+"\n")
    keeptime = ''
    keeptime += str(projectInformation[0]['durationType'])
    keeptime +=' ' + str(projectInformation[0]['lastRan'])

    if int(projectInformation[0]['durationType']) == 3 :
        keeptime += ' 99 99'
    elif int(projectInformation[0]['durationType']) == 2 :
        keeptime += ' 99 '+str(projectInformation[0]['runDayOrMonth'])
    elif int(projectInformation[0]['durationType']) == 1 :
        keeptime += ' ' + str(projectInformation[0]['runDayOrMonth']) + ' 99'

    HistoryFile.write(keeptime+"\n")
    HistoryFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

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
                    response = []
                    response = verify_using_inode(dict,dict_Hash,dict_File, e , file , Algorithm)

                    if not response or len(response) < 1:
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

    HistoryFile.close()
    print('closing '+historyFile+' File')

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
    try:
        HistoryFile.close()
        print('closing '+historyFile+' File')
    except:
        pass

    repath = writer(Algorithm, file.replace('.fxy','').replace('projects\\',''), total, confirmed, moved, created, corruptedOrChanged, missingFile[1], FileChangedList,projectName)
    return confirmed, moved, created, corruptedOrChanged , missingFile[1], repath

#Path Encoding to a Code To Identify the Path of each file
def pathCodeEncode(pathStr):
    return 'Fixity-'+str(pathStr)

#Path decoding to a Path From Encoded Code To Identify the Path of each file
def pathCodedecode(code):
    return base64.b64decode(code)

#Verify File Changes
def getCodePath(code , InfReplacementArray):
    for single in InfReplacementArray:
        if InfReplacementArray[single]['code'] == code:
            return single

#Get Code using Path
def getPathCode(path , InfReplacementArray):
    for single in InfReplacementArray:
        if InfReplacementArray[single]['path'] == path:
            return InfReplacementArray[single]['code']

#Get Path Id using path
def getPathId(path , InfReplacementArray):
    for single in InfReplacementArray:
        if InfReplacementArray[single]['path'] == path:
            return InfReplacementArray[single]['id']

#Get Path Id using path
def getCodePathMore(code , InfReplacementArray):
    for single in InfReplacementArray:
        if InfReplacementArray[single]['code'] and InfReplacementArray[single]['code'] != None and InfReplacementArray[single]['code'] == code:
            return InfReplacementArray[single]

#Get Directory Detail
def getDirectoryDetail(projectName ,fullpath = False):
    print('getDirectoryDetail')
    DirectoryDetail = [[],[],[],[],[],[],[],[]]
    if fullpath:
        projfile = open(fullpath, 'rb')
        print('Open '+fullpath+' File')
    else:
        projfile = open('projects\\' + projectName + '.fxy', 'rb')
        print('Open '+'projects\\' + projectName + '.fxy'+' File')

    allProjectDirectoryList = projfile.readline()
    projectDirectoryList = allProjectDirectoryList.split(';')
    for  SigleDir in projectDirectoryList:
        if SigleDir !=None and SigleDir != '' and ('|-|-|' in SigleDir):
            detialInformation = str(SigleDir).split('|-|-|')
            if detialInformation[2] != None and detialInformation[2] !='' :
                indexOfDet = int(detialInformation[2])
                DirectoryDetail[indexOfDet] = detialInformation
    projfile.close()
    print('closing '+fullpath+' File')
    return DirectoryDetail


def EncodeInfo(stringToBeEncoded):
    stringToBeEncoded = str(stringToBeEncoded).strip()
    return base64.b16encode(base64.b16encode(stringToBeEncoded))

def DecodeInfo(stringToBeDecoded):
    stringToBeDecoded = str(stringToBeDecoded).strip()
    return base64.b16decode(base64.b16decode(stringToBeDecoded))

