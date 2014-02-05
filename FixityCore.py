# Fixity Core module
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

import hashlib
from os import chdir, walk, path, stat, getcwd
from sys import argv
from collections import defaultdict
from platform import platform
import datetime
import time
from glob import glob
from os import path, makedirs, remove
from re import sub, compile
import win32file
import shutil

#Custom
from Debuger import Debuger
# Checksum generation method
# Input: Filepath, algorithm
# Output: Hexadecimal value of hashed file



global verifiedFiles
verifiedFiles = []

def fixity(f, alg): 
	
	
	try:
		if alg == 'md5':
			fix = hashlib.md5()
		elif alg == 'sha1':
			fix = hashlib.sha1()
		elif alg == 'sha256':
			fix = hashlib.sha256()
	except Exception as e:
			Debugging = Debuger()
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
			Debugging.logError('Error Reporting Line 36 - 40 While encrypting File into hashes using Algo:' + str(alg)  +" File FixtyCore\n", moreInformation)
			pass		
		
	with open(f, 'rb') as target:
		for piece in iter(lambda: target.read(4096), b''):
			fix.update(piece)
		return fix.hexdigest()
	
	
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
	id = '';
	
	try:
		target = open(f, 'rb')
		
		id = str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[4]) + \
			str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[8]) + \
			str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[9])
		return id
	except Exception as e:
			Debugging = Debuger()
			Debugging.tureDebugerOn();
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
def quietTable(r, a):
	listOfValues = []
	fls = []
	
	try:
		
		for root, subFolders, files in walk(r):
			for Singlefile in files:
				fls.append(path.join(root, Singlefile))
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
			Debugging.logError('Error Reporting Line 140-143 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)
			pass	
	try:	
		for f in xrange(len(fls)):
			p = path.abspath(fls[f])
			h = fixity(p, a)
			i = ntfsID(p)
			listOfValues.append((h, p, i))
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
			Debugging.logError('Error Reporting Line 125-129 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)
			pass		
		
	return listOfValues

# Method to convert database line into tuple
# Input: tab-delimited line from database file
# Output: tuple: (hash, abspath, id)
def toTuple(line):
	
	try:	
		x = line.split('\t')
		return [x[0].strip(), x[1].strip(), x[2].strip()]
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


def verify_using_inode (dicty, dictHash, dictFile, line, fileNamePath=''):
	global verifiedFiles
	
	try:
		CurrentDirectory = dicty.get(line[2])
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
		Debugging.logError('Error Reporting Line 250 FixityCore While listing directory and files FixityCore' +"\n", moreInformation)
		pass
		
	if path.isfile(line[1]):
		
		if CurrentDirectory != None :
			CurrentDirectory = CurrentDirectory[0]
			
			isHashSame , isFilePathSame = '' , ''
			
			# Check For File Hash Change 
			isHashSame = (CurrentDirectory[1] == line[0])

			
			# Check For File Path Change
			isFilePathSame = (CurrentDirectory[0] == line[1])
			
			if isHashSame and isFilePathSame:
				verifiedFiles.append(line[1])
				return line, "Confirmed File :\t" + str(line[1])
				#print 'File Confirmed : ' + line[1]
				
			if isHashSame and (not isFilePathSame):
				verifiedFiles.append(line[1])
				return line, "Moved or Renamed File :\t" + str(CurrentDirectory[0]) + "\t changed to\t" + str(line[1])
# 				print 'File Moved from '+ line[1] + ' to ' + SingleDirectoryStatus[0]
				
			if (not isHashSame) and isFilePathSame:
				verifiedFiles.append(line[1])
				return line, 'Changed File :\t' + str(line[1])
# 				print 'File Changed : ' + line[1]
				
			if (not isHashSame) and (not isFilePathSame):
				verifiedFiles.append(line[1])
				return line, "Moved or Renamed File :\t" + str(CurrentDirectory[0]) + "\t changed to\t" + str(line[1])
# 				print 'File Moved and Changed' + line[1]
				
		else :
			#New Inode
			CurrentDirectory = dictHash.get(line[0])
			if CurrentDirectory != None:
				CurrentDirectory = CurrentDirectory[0]
				isFilePathSame = ''
				
				# Check For File Path Change
				isFilePathSame = (CurrentDirectory[0] == line[1])
				
				if isFilePathSame :
					verifiedFiles.append(line[1])
					return line, "Confirmed File :\t" + str(line[1])
				else :
					verifiedFiles.append(line[1])
					return line, "New Files\t" + line[1] + "\tcopy of\t" + str(CurrentDirectory[0])
				
			else :
				CurrentDirectory = dictFile.get(line[1])
				if CurrentDirectory != None:
					verifiedFiles.append(line[1])
					return line, 'File Changed :\t' + str(line[1])
					
			verifiedFiles.append(line[1])
			return line, 'New FIle :\t' + str(line[1])
# 				print 'new file' + line[1]
# 	else:
# 		verifiedFiles.append(line[1])
# 		return line, 'Removed File :\t' + str(line[1])
# 				msg += "Removed Files\t" + obj[0] +"\n"
				
# Method to verify a tuple against the dictionary
# Input: defaultDict (from buildDict), tuple
# Output: Message based on whether the file was good or not

def verify(dicty, line, fileNamePath=''):

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

	report += out

	AutiFixPath = (getcwd()).replace('schedules','').replace('\\\\',"\\")
	rn = AutiFixPath+'\\reports\\fixity_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S')) + '_' + str(projectName) + '.csv'
	
	r = open(rn, 'w+')
	r.write(report)
	r.close()
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
					response = GetDirectoryInformationUsingInode(file,obj[1])
					if not response == True :   						
						continue
					count += 1
					msg += "Removed Files\t" + obj[0] +"\n"

	return msg, count


def run(file,filters='',projectName = ''):
	
	FiltersArray = filters.split(',')
	dict = defaultdict(list)
	dict_Hash = defaultdict(list)
	dict_File = defaultdict(list)
	confirmed , moved , created , corruptedOrChanged  = 0, 0, 0, 0
	FileChangedList = "" 
	infile = open(file, 'r')
	tmp = open(file + ".tmp", 'w')
	first = infile.readline()
	second = infile.readline()
	ToBeScannedDirectoriesInProjectFile = first.split(';')
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
		
			x = toTuple(l);
			dict[x[2]].append([x[1], x[0], False])
			dict_Hash[x[0]].append([x[1], x[2], False])
			dict_File[x[1]].append([x[0], x[2], False])
		except Exception as ex :
			Debugging = Debuger()
			Debugging.tureDebugerOn();
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
			Debugging.logError('Error Reporting 468  - 471 File FixityCore While inserting information' +x[0]+' '+'||'+x[1]+'||'+'||'+x[2]+"\n", moreInformation)
			pass
		
	ToBeScannedDirectoriesInProjectFile.remove('\n')
	for SingleDirectory in ToBeScannedDirectoriesInProjectFile:
		
		DirectorysInsideDetails = quietTable(SingleDirectory, 'sha256')
		for e in DirectorysInsideDetails:
			flag =True
			for Filter in FiltersArray:
				if Filter !='' and e[1].find(str(Filter).strip()) >= 0:
					flag =False
					
			if flag:
				check+= 1
				try:
					#response = verify_using_inode(dict,dict_Hash,dict_File, e , file)
					response = verify(dict, e , file)
				except Exception as ex :
					Debugging = Debuger()
					Debugging.tureDebugerOn();
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
					Debugging.logError('Error Reporting Line 500 FixityCore While Verfiying file status' +str(file)+' '+'||'+str(x[0])+'||'+'||'+str(x[1])+' '+'||'+str(x[2])+'||'+"\n", moreInformation)
					pass
						
				
				FileChangedList += response[1] + "\n"
				if response[1].startswith('Confirmed'): 
					confirmed += 1
				elif response[1].startswith('Moved'):
					moved += 1
				elif response[1].startswith('New'):
					created += 1
				else:
					corruptedOrChanged += 1
				
				tmp.write(str(response[0][0]) + "\t" + str(response[0][1]) + "\t" + str(response[0][2]) + "\n")
				
	missingFile = missing(dict_Hash,SingleDirectory) 
	FileChangedList += missingFile[0]
	tmp.close()
	infile.close()
	
	shutil.copy(file + ".tmp", file)
	remove(file + ".tmp")
	
	total = confirmed + moved + created + corruptedOrChanged + missingFile[1]
	repath = writer('sha256', file.replace('.fxy','').replace('projects\\',''), total, confirmed, moved, created, corruptedOrChanged, missingFile[1], FileChangedList,projectName)
	return confirmed, moved, created, corruptedOrChanged , missingFile[1], repath


# ## To check Main Functionality  
#projects_path = getcwd()+'\\projects\\'
#run(projects_path+'New_Project.fxy')
#test()

