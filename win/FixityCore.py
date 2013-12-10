# Fixity Core module
# Version 0.1, 2013-10-28
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

# Checksum generation method
# Input: Filepath, algorithm
# Output: Hexadecimal value of hashed file
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
def verify(dict, line):
	
	# if the hash is a key in the dictionary, return the values
	# returns None on a miss
	vals = dict.get(line[0])
	copies = ""
	i = 0
	
	# if we found values, check file attendance
	if vals != None:
		for v in vals:
			id = (v[1] == line[2])
			path = (v[0] == line[1])
			if id and path:
				dict[line[0]][i][2] = True
				return line, "CONFIRMED\t" + str(v[0])
			elif id and not path:
				dict[line[0]][i][2] = True
				return line, "MOVED/RENAMED\t" + str(line[1]) + "\tmoved from " + str(v[0])
			elif path and not id:
				dict[line[0]][i][2] = True
				return line, "Possibly unsafe changes to\t" + str(v[0])
			copies += " " + str(v[0])
			i += 1
		return line, "NEW FILE\t" + line[1] + "\tcopy of " + copies

	# if we don't have a given hash, figure out why
	else:
		# iterate through the dictionary until we find a matching ID and/or path
		# this is regrettably slow and really needs to be improved
		for key in dict:
			vals = dict.get(key)
			i = 0
			for v in vals:
				id = (v[1] == line[2])
				path = (v[0] == line[1])
				if id or path:
					# found it! Set the found flag as True and return a corruption message
					dict[key][i][2] = True
					return (key, v[0], v[1]), "FAILURE\t" + str(v[0])
				i += 1
		# if the ID and/or path aren't in the dictionary, then we have an entirely new file
		return line, "NEW FILE\t" + str(line[1])
		

# Writes report about the most recent fixity check
# Input: algorithm used, start time, directories scanned, number of files found, good files, warned files, bad files, missing files, [out?], current time, old DB, new DB
# Output: All this, written nicely to a tab-delimited file, with the filepath returned
def writer(alg, proj, num, conf, moves, news, fail, dels, out):
	report = "Fixity report\n"
	report += "Project name\t" + proj + "\n"
	report += "Algorithm used\t" + alg + "\n"
	report += "Date\t" + str(datetime.date.today()) + "\n"
	report += "Total files\t" + str(num) + "\n"
	report += "Files confirmed\t" + str(conf) + "\n"
	report += "Files moved\t" + str(moves) + "\n"
	report += "Files created\t" + str(news) + "\n"
	report += "Files corrupted\t" + str(fail) + "\n"
	report += "Files missing\t" + str(dels) + "\n"
	report += out
	AutiFixPath = (getcwd()).replace('schedules','').replace('\\\\',"\\")
	rn = AutiFixPath+'\\reports\\report_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S')) + '.csv'
		
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
			if obj[2] is False:
				count += 1
				msg += "MISSING FILE\t" + obj[0]
	return msg, count

def run(file,filters=''):
	FiltersArray = filters.split(',')
	dict = defaultdict(list)
	c, f, mv, nw, = 0, 0, 0, 0
	rp = ""
	infile = open(file, 'r')
	tmp = open(file + ".tmp", 'w')
	first = infile.readline()
	second = infile.readline()
	roots = first.split(';')
	mails = second.split(';')
	keeptime = infile.readline()
	trash = infile.readline()
	
	tmp.write(first)
	tmp.write(second)
	tmp.write(keeptime)
	tmp.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
	
	for l in infile.readlines():
		x = toTuple(l)
		dict[x[0]].append([x[1], x[2], False])
	for r in roots:
		t = quietTable(r, 'sha256')
		for e in t:
			flag =True
			for Filter in FiltersArray:
				if Filter !='' and e[1].find(str(Filter).strip()) >= 0:
					flag =False
			
			if flag:
				response = verify(dict, e)
				rp += response[1] + "\n"
				if response[1].startswith('CONFIRMED'):
					c += 1
				elif response[1].startswith('MOVED'):
					mv += 1
				elif response[1].startswith('NEW'):
					nw += 1
				else:
					f += 1
				tmp.write(str(response[0][0]) + "\t" + str(response[0][1]) + "\t" + str(response[0][2]) + "\n")
	m = missing(dict)
	rp += m[0]
	tmp.close()
	infile.close()
	shutil.copy(file + ".tmp", file)
	remove(file + ".tmp")
	repath = writer('sha256', file.replace('.fxy','').replace('projects\\',''), c+mv+nw+f+m[1], c, mv, nw, f, m[1], rp)
	return c, mv, nw, f, m[1], repath