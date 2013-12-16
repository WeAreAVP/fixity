# Fixity Core module
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

import hashlib
from os import chdir, walk, path, stat, getcwd
from sys import *
from collections import defaultdict
from platform import platform
import datetime
import time
from glob import glob
from os import path, makedirs, remove
from re import sub, compile
import win32file
import shutil
from compiler.pycodegen import EXCEPT
from msilib.schema import Extension

# Checksum generation method
# Input: Filepath, algorithm
# Output: Hexadecimal value of hashed file
allreadyVisited = []
verifiedFiles = []

def fixity(f, alg): 
	if alg == 'md5':
		fix = hashlib.md5()
	elif alg == 'sha1':
		fix = hashlib.sha1()
	elif alg == 'sha256':
		fix = hashlib.sha256()
	
	with open(f, 'rb') as target:
		for piece in iter(lambda: target.read(4096), b''):
			fix.update(piece)
		return fix.hexdigest()

	
		
# File ID for NTFS
# Returns the complete file ID as a single long string
# (volume number, high index, low index)
def ntfsID(f):
	target = open(f, 'rb')
	
	id = str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[4]) + \
		str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[8]) + \
		str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[9])
	return id


# Method to create (hash, path, id) tables from file root
# Input: root, output (boolean), hash algorithm, QApplication
# Output: list of tuples of (hash, path, id)
def quietTable(r, a):
	list = []
	fls = []
	
	for root, subFolders, files in walk(r):
		for file in files:
			fls.append(path.join(root, file))
			
	for f in xrange(len(fls)):
		p = path.abspath(fls[f])
		h = fixity(p, a)
		i = ntfsID(p)
		list.append((h, p, i))		
	return list

# Method to convert database line into tuple
# Input: tab-delimited line from database file
# Output: tuple: (hash, abspath, id)
def toTuple(line):
	x = line.split('\t')
	return [x[0].strip(), x[1].strip(), x[2].strip()]

# Method to generate a dictionary, keyed to file hashes
# This is done to greatly speed up the eventual fixity checks
# Input: Database file
# Output: defaultdict keyed to hash values
def buildDict(file):
	table = open(file, 'r')
	warns = ""
	db = defaultdict(list)
	for line in table.readlines():
		x = toTuple(line)
		db[x[0]].append([x[1], x[2], False])
	return db

# Writes table to file
# Input: filepath, table (list of tuples from toTuple)
# Output: A nicely written file
def tableToFile(path, list):
	f = open(path, 'w')
	for item in list:
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

# Method to verify a tuple against the dictionary
# Input: defaultDict (from buildDict), tuple
# Output: Message based on whether the file was good or not
def verify(dict, line,allreadyVisited=[]):
	# if the hash is a key in the dictionary, return the values
	# returns None on a miss
	# Current Directory Status (Information of this directory using hash from the project file by scanning the directory)
	
	CurrentDirectoryStatus = dict.get(line[0])
	copies = ""
	i = 0
	# if we found values, check file attendance (If this file exist)
	if path.isfile(line[1]):
		if CurrentDirectoryStatus != None:
			print('i')
			for SingleDirectoryStatus in CurrentDirectoryStatus:
				
				isFilePresent , isSameHash , isSameFilepath , isSameinode = True , True , False , False
				
				# Check For File INODE Change 
				isSameinode = (SingleDirectoryStatus[1] == line[2])
				
				# Check For File Path Change
				isSameFilepath = (SingleDirectoryStatus[0] == line[1])
				
				
# 				if SingleDirectoryStatus[0] in allreadyVisited:
# 					print('skipped')
# 					continue
				allreadyVisited.append(SingleDirectoryStatus[0])
				
				# If Nothing changed 
				if   isSameFilepath and isSameinode:
					print(1)
					dict[line[0]][i][2] = True
					verifiedFiles.append(SingleDirectoryStatus[0])
					return line, "CONFIRMED\t" + str(SingleDirectoryStatus[0])
				# If  Path changed But Inode is same
				elif not isSameFilepath and isSameinode:
					print(2)
					dict[line[0]][i][2] = True
					
					verifiedFiles.append(SingleDirectoryStatus[0])
					print(verifiedFiles)
					return line, "MOVED/RENAMED\t" + str(line[1]) + "\tmoved from " + str(SingleDirectoryStatus[0])
				# If Inode changed But Path is same 
				elif (isSameFilepath and not isSameinode) :
					print(3)
					dict[line[0]][i][2] = True
					verifiedFiles.append(SingleDirectoryStatus[0])
	 				return line, "CONFIRMED\t" + str(SingleDirectoryStatus[0])
	 			# If Inode and Path both changed
				elif (not isSameFilepath and not isSameinode) :
					print(4)
					dict[line[0]][i][2] = False
					verifiedFiles.append(SingleDirectoryStatus[0])
	 				return line, "MOVED/RENAMED\t" + str(line[1]) + "\tmoved from " + str(SingleDirectoryStatus[0])
	 			
	 			# If File Dose not exist and path exists	
				elif not path.isfile(line[1]) and line[2] and line[1]:
					print(5)
					dict[key][i][2] = True
					verifiedFiles.append(SingleDirectoryStatus[0])
					return line, "MOVED/RENAMED\t" + str(line[1]) + "\tmoved from " + str(SingleDirectoryStatus[0])
				
				copies += " " + str(SingleDirectoryStatus[0])
				i += 1
			verifiedFiles.append(line[1])	
			return line, "NEW\t" + line[1] + "\tcopy of " + copies
	
		# if we don't have a given hash, figure out why
		else:
			print('e')
			# iterate through the dictionary until we find a matching ID and/or path
			isFilePresent , isSameHash , isSameFilepath , isSameinode = False , False , False , False
			
			for key in dict: 
				
				NewDirectoryStatus = dict.get(key)
				
				i = 0
				if NewDirectoryStatus:
					for SingleDirectoryStatus in NewDirectoryStatus:
						#skip Files already verified 
# 						if SingleDirectoryStatus[0] in allreadyVisited:
# 							print('skipped')
# 							continue
						allreadyVisited.append(SingleDirectoryStatus[0])
						# Check For File INODE Change 
						isSameinode = (SingleDirectoryStatus[1] == line[2])
						
						# Check For File Path Change
						isSameFilepath = (SingleDirectoryStatus[0] == line[1])
						
						# found it! Set the found flag as True and return a Changed message
						if isSameinode and isSameFilepath:
							dict[key][i][2] = True
							verifiedFiles.append(SingleDirectoryStatus[0])
							return (key, SingleDirectoryStatus[0], SingleDirectoryStatus[1]), "Changed\t" + str(SingleDirectoryStatus[0])
						
						# If  Path changed But Inode is same
						elif isSameinode and not isSameFilepath:
							
							dict[key][i][2] = True
							verifiedFiles.append(SingleDirectoryStatus[0])
							return (key, SingleDirectoryStatus[0], SingleDirectoryStatus[1]), "Changed\t" + str(SingleDirectoryStatus[0])
						
						# If  Path same But Inode changed
						elif not isSameinode and isSameFilepath:
							print(3)
							dict[key][i][2] = True
							verifiedFiles.append(SingleDirectoryStatus[0])
							return (key, SingleDirectoryStatus[0], SingleDirectoryStatus[1]), "Changed\t" + str(SingleDirectoryStatus[0])
						

						i += 1
			verifiedFiles.append(line[1])
			return line, "NEW FILE\t" + str(line[1])
		

# Writes report about the most recent fixity check
# Input: algorithm used, start time, directories scanned, number of files found, good files, warned files, bad files, missing files, [out?], current time, old DB, new DB
# Output: All this, written nicely to a tab-delimited file, with the filepath returned
def writer(alg, proj, num, conf, moves, news, fail, dels, out):
	report = "Fixity report\n"
	report += "Project name\t" + proj + "\n"
	report += "Algorithm used\t" + alg + "\n"
	report += "Date\t\t" + str(datetime.date.today()) + "\n"
	report += "Total\t\t" + str(num) + "\n"
	report += "Confirmed\t" + str(conf) + "\n"
	report += "Moved\t\t" + str(moves) + "\n"
	report += "Created\t\t" + str(news) + "\n"
	report += "Changed\t\t" + str(fail) + "\n"
	report += "Missing\t\t" + str(dels) + "\n"
	report += out
	AutiFixPath = (getcwd()).replace('schedules','').replace('\\\\',"\\")
	rn = AutiFixPath+'\\reports\\report_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S')) + '.csv'
	print(report)
	r = open(rn, 'w+')
	r.write(report)
	r.close()
	return rn

# Method to find which files are missing in the scanned directory
# Input: defaultdict (from buildDict)
# Output: warning messages about missing files (one long string and printing to stdout)
def missing(dict):
	msg = ""
	count = 0
	# walks through the dict and returns all False flags
	for keys in dict:
		for obj in dict[keys]:
			if not path.isfile(obj[0]):			
				
				#check if file already exists in the manifest 
				if not obj[0] in verifiedFiles:
					count += 1
					msg += "MISSING\t" + obj[0]
	return msg, count

def run(file,filters=''):
	FiltersArray = filters.split(',')
	dict = defaultdict(list)
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
		x = toTuple(l)
		dict[x[0]].append([x[1], x[2], False])
	for SingleDirectory in ToBeScannedDirectoriesInProjectFile:
		
		DirectorysInsideDetails = quietTable(SingleDirectory, 'sha256')
		
		for e in DirectorysInsideDetails:
			
			flag =True
			for Filter in FiltersArray:
				if Filter !='' and e[1].find(str(Filter).strip()) >= 0:
					flag =False
					
			if flag:
				check+= 1
				response = verify(dict, e,allreadyVisited)
				FileChangedList += response[1] + "\n"
				if response[1].startswith('CONFIRMED'): 
					confirmed += 1
				elif response[1].startswith('MOVED'):
					moved += 1
				elif response[1].startswith('NEW'):
					created += 1
				else:
					corruptedOrChanged += 1
				tmp.write(str(response[0][0]) + "\t" + str(response[0][1]) + "\t" + str(response[0][2]) + "\n")
			
	missingFile = missing(dict) 
	FileChangedList += missingFile[0]
	tmp.close()
	infile.close()
	shutil.copy(file + ".tmp", file)
	remove(file + ".tmp")
	
	total = confirmed + moved + created + corruptedOrChanged + missingFile[1]
	repath = writer('sha256', file.replace('.fxy','').replace('projects\\',''), total, confirmed, moved, created, corruptedOrChanged, missingFile[1], FileChangedList)
	
	return confirmed, moved, created, corruptedOrChanged , missingFile[1], repath
#  
# projects_path = getcwd()+'\\projects\\'
# run(projects_path+'test.fxy')
