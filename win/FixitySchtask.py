# Fixity Scheduler
# Version 0.1, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

import subprocess
from os import getcwd, remove

# Deletes the SCHTASK entry and its corresponding files
def deltask(project):
	startupinfo = subprocess.STARTUPINFO()
	startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	subprocess.call("schtasks /Delete /F /TN \"Fixity-" + project.replace(' ','_') + "\"", startupinfo=startupinfo)
	try:
		remove("schedules\\fixity-" + project + ".bat")
	except:
		pass
	try:
		remove("schedules\\fixity-" + project + ".vbs")
	except:
		pass
		
# Writes a task to SCHTASKS and creates necessary VBS/BAT files
def schedule(interval, dow, dom, time, project):
	prj = project.replace(' ', '_')
	deltask(prj)
	
	spec = ""
	
	if interval == 1:
		mo = "MONTHLY"
	if interval == 2:
		mo = "WEEKLY"
	if interval == 3:
		mo = "DAILY"
	
	if dow != 99:
		days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
		spec = " /D " + days[dow] + " "
	elif dom != 99:
		spec = " /D " + str(dom) + " "
	
	f = open("schedules\\fixity-" + prj + ".bat", "w")
	f.write("@ECHO OFF\n")
	f.write("cd /d %~dp0\n")
	f.write("cd ..\n")
	f.write("\"" + getcwd() + "\\AutoFixity.exe\" \"" + prj + "\"\n")
	f.close()
	
	x = open("schedules\\fixity-" + prj + ".vbs", "w")
	x.write("Dim location, p\n")
	x.write("location = WScript.ScriptFullName\n")
	x.write("p = Replace(location, \"fixity-" + prj + ".vbs\", \"fixity-" + prj + ".bat\")\n")
	x.write("Set WinScriptHost = CreateObject(\"WScript.Shell\")\n")
	x.write("WinScriptHost.Run p, 0\n")
	x.write("Set WinScriptHost = Nothing")
	x.close()
	startupinfo = subprocess.STARTUPINFO()
	startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	subprocess.call("schtasks /Create /F /TN \"Fixity-" + prj + "\" /SC " + mo + spec + " /ST " + time + " /TR \"" + getcwd() + "\\schedules\\fixity-" + prj + ".vbs\"", startupinfo=startupinfo)