# Fixity Scheduler
# Version 0.1, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

import subprocess
from os import getcwd, remove , environ
import sys
import time

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
def schedule(interval, dow, dom, timeSch, project):
        VERSION = 0.2
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
        f.write("\"" + getcwd() + "\\schedules\\AutoFixity.exe\" \"" + prj + "\"\n")
        f.close()
        
        x = open("schedules\\fixity-" + prj + ".vbs", "w")
        x.write("Dim location, p\n")
        x.write("location = WScript.ScriptFullName\n")
        x.write("p = Replace(location, \"fixity-" + prj + ".vbs\", \"fixity-" + prj + ".bat\")\n")
        x.write("Set WinScriptHost = CreateObject(\"WScript.Shell\")\n")
        x.write('WinScriptHost.Run("""" & p & """")')
        x.write("\n")  
        x.write("Set WinScriptHost = Nothing")
        x.close()
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        path = "'\""+ getcwd() + "\\schedules\\fixity-" + prj + ".vbs\"'"
        RegistrationInfo ={}  
        Triggers  ={}
        Principals  ={} 
        Settings  ={} 
        Actions= {}
        
        #TODO Time Zone Handling
        RegistrationInfo['Date'] = time.strftime("%Y-%m-%dT%X") #2005-10-11T13:21:17-08:00
        RegistrationInfo['Author'] = environ.get( "USERNAME" )
        RegistrationInfo['Version'] = VERSION
        RegistrationInfo['Description'] ='Fixity Task Scheduler to Monitor A Folder Activity!'
            
            
        CurrentDate  = time.strftime("%Y-%m-%d")
        EndBoundary  = '2015-12-12'
                        
        Triggers['CalendarTrigger'] ={}
        Triggers['CalendarTrigger']['StartBoundary'] = CurrentDate+'T'+timeSch
        Triggers['CalendarTrigger']['EndBoundary'] =EndBoundary+'T'+timeSch
        Triggers['CalendarTrigger']['Repetition'] = {}
        Triggers['CalendarTrigger']['ScheduleByDay'] = {}
        Triggers['CalendarTrigger']['Repetition']['Interval'] =''
        Triggers['CalendarTrigger']['Repetition']['Duration'] =''
        Triggers['CalendarTrigger']['ScheduleByDay']['DaysInterval'] ='1'
        
        
         
        Principals['Principal'] ={}
        Principals['Principal']['UserId'] ='Administrator'
        Principals['Principal']['LogonType'] = 'InteractiveToken'
        
         
        Settings['Enabled'] ='true'
        Settings['AllowStartOnDemand'] ='true'
        Settings['AllowHardTerminate'] = 'true'
        Settings['DisallowStartIfOnBatteries'] = 'false'
        
        Actions['Exec'] ={}
        Actions['Exec']['Command'] =path
        
        
        XMLFileNameWithDirName = CreateXML(prj , VERSION , RegistrationInfo  , Triggers , Principals , Settings , Actions)
        XMLFilePath ="'\""+ getcwd() + "\\" + XMLFileNameWithDirName + "\"'"
        
        Command ="schtasks /Create /TN \"Fixity-" + prj + "\"  /xml "+XMLFilePath
        print(Command)
        subprocess.call("schtasks /Create /F /TN \"Fixity-" + prj + "\" /SC " + mo + spec + " /ST " + timeSch + " /TR " +path, startupinfo=startupinfo)
        
def CreateXML(ProjectName , Version , RegistrationInfo  , Triggers , Principals , Settings , Actions):
        xmlsch = open("schedules\\fixity-" + ProjectName + "-sch.xml", "w")
        xmlsch.write("<?xml version=\"1.0\" ?>\n")
        xmlsch.write("<Task xmlns=\"http://schemas.microsoft.com/windows/2004/02/mit/task\">\n")
        xmlsch.write("    <RegistrationInfo>\n")
        xmlsch.write("        <Date>"+RegistrationInfo['Date']+"</Date>\n")
        xmlsch.write("        <Author>"+RegistrationInfo['Author']+"</Author>\n")
        xmlsch.write("        <Version>"+RegistrationInfo['Description']+"</Version>\n")
        xmlsch.write("        <Description>"+RegistrationInfo['Description']+"</Description>\n")
        xmlsch.write("    </RegistrationInfo>\n")
        xmlsch.write("    <Triggers>\n")
        xmlsch.write("        <CalendarTrigger>\n")
        xmlsch.write("            <StartBoundary>"+Triggers['CalendarTrigger']['StartBoundary']+"</StartBoundary>\n")
        xmlsch.write("            <EndBoundary>"+Triggers['CalendarTrigger']['EndBoundary']+"</EndBoundary>\n")
#         xmlsch.write("            <Repetition>\n")
#         xmlsch.write("                <Interval>"+Triggers['CalendarTrigger']['Repetition']['Interval']+"</Interval>\n")
#         xmlsch.write("                <Duration>"+Triggers['CalendarTrigger']['Repetition']['Duration']+"</Duration>\n")
#         xmlsch.write("            </Repetition>\n")
        xmlsch.write("            <ScheduleByDay>\n")
        xmlsch.write("                <DaysInterval>"+Triggers['CalendarTrigger']['ScheduleByDay']['DaysInterval']+"</DaysInterval>\n")
        xmlsch.write("            </ScheduleByDay>\n")
        xmlsch.write("        </CalendarTrigger>\n")
        xmlsch.write("    </Triggers>\n")
#         xmlsch.write("    <Principals>\n")
#         xmlsch.write("        <Principal>\n")
#         xmlsch.write("            <UserId>"+ Principals['Principal']['UserId'] +"</UserId>\n")
#         xmlsch.write("            <LogonType>"+ Principals['Principal']['UserId'] +"</LogonType>\n")
#         xmlsch.write("        </Principal>\n")
#         xmlsch.write("    </Principals>\n")
        xmlsch.write("    <Settings>\n")
        xmlsch.write("        <Enabled>"+ Settings['Enabled'] +"</Enabled>\n")
        xmlsch.write("        <AllowStartOnDemand>"+ Settings['AllowStartOnDemand'] +"</AllowStartOnDemand>\n")
        xmlsch.write("        <AllowHardTerminate>"+ Settings['AllowHardTerminate'] +"</AllowHardTerminate>\n")
        xmlsch.write("        <DisallowStartIfOnBatteries>"+ Settings['DisallowStartIfOnBatteries'] +"</DisallowStartIfOnBatteries>\n")
        xmlsch.write("    </Settings>\n")
        xmlsch.write("    <Actions>\n")
        xmlsch.write("        <Exec>\n")
        xmlsch.write("            <Command>"+ Actions['Exec']['Command'] +"</Command>\n")
        xmlsch.write("        </Exec>\n")
        xmlsch.write("      </Actions>\n")
        xmlsch.write("</Task>\n")
        xmlsch.close()
        return "schedules\\fixity-" + ProjectName + "-sch.xml"
        
        
        
        
        
        
        
        
        
        