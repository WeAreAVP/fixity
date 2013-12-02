# Fixity Scheduler
# Version 0.1, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

import subprocess
from os import getcwd, remove , environ
import sys
import time
from EmailPref import EmailPref
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
def schedule(interval, dow, dom, timeSch, project, ACPowerCheck, StartWhenAvailable,EmailOnlyWhenSomethingChanged):
       
        VERSION = 0.3
        USERNAME = environ.get( "USERNAME" )
        prj = project.replace(' ', '_')
        deltask(prj)
        
        spec = ""
        
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
        path = "\""+ getcwd() + "\\schedules\\fixity-" + prj + ".vbs\""
       
        
        ############################################################################################################################

        #TODO Time Zone Handling
        #TASK SCHEDULER OPTION and ATTRIBUTES
        RegistrationInfo ={}  
        Triggers  ={}
        Principals  ={} 
        Settings  ={} 
        Actions= {}
         
        RegistrationInfo['Date'] = time.strftime("%Y-%m-%dT%X") #2005-10-11T13:21:17-08:00
        RegistrationInfo['Author'] = USERNAME
        RegistrationInfo['Version'] = VERSION
        RegistrationInfo['Description'] ='Fixity Task Scheduler to Monitor A Folder Activity!'

        
        CurrentDate  = time.strftime("%Y-%m-%d")
        EndBoundary  = '2015-12-12'                        
        Triggers['CalendarTrigger'] ={}
        Triggers['CalendarTrigger']['StartBoundary'] = CurrentDate+'T'+timeSch
        Triggers['CalendarTrigger']['EndBoundary'] =EndBoundary+'T'+timeSch
        Triggers['CalendarTrigger']['Repetition'] = {}
        Triggers['CalendarTrigger']['ScheduleByDay'] = {}
        
        Triggers['CalendarTrigger']['ScheduleByMonth'] = {}    
        Triggers['CalendarTrigger']['ScheduleByMonth']['DaysOfMonth']  = {}
        Triggers['CalendarTrigger']['Repetition']['Interval'] =''
        Triggers['CalendarTrigger']['Repetition']['Duration'] =''
        
        
        if interval == 1:
            Triggers['CalendarTrigger']['ScheduleByMonth'] = {}    
            Triggers['CalendarTrigger']['ScheduleByMonth']['DaysOfMonth'] = dom
        if interval == 2:
            daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            Triggers['CalendarTrigger']['ScheduleByWeek'] = {}
            Triggers['CalendarTrigger']['ScheduleByWeek']['DaysOfWeek'] = {}
            Triggers['CalendarTrigger']['ScheduleByWeek']['WeeksInterval'] = '1'
            Triggers['CalendarTrigger']['ScheduleByWeek']['DaysOfWeek'] = daysOfWeek[dow]
        if interval == 3:
            Triggers['CalendarTrigger']['ScheduleByDay']['DaysInterval'] ='1'
        
        Principals['Principal'] = {}
        Principals['Principal']['UserId'] = 'Administrator'
        Principals['Principal']['LogonType'] = 'InteractiveToken'
        
        
        Settings['Enabled'] ='true'
        Settings['AllowStartOnDemand'] = 'true'
        Settings['AllowHardTerminate'] = 'true'
        Settings['WakeToRun'] = 'true'
        
        if StartWhenAvailable == True or StartWhenAvailable == 'True':
            Settings['StartWhenAvailable'] = 'true'
        else:
            Settings['StartWhenAvailable'] = 'false'
            
        if ACPowerCheck == True or ACPowerCheck == 'True':
            Settings['DisallowStartIfOnBatteries'] = 'false'
        else:    
            Settings['DisallowStartIfOnBatteries'] = 'true'

        Actions['Exec'] ={}
        Actions['Exec']['Command'] =path
        list = {}
        alltext = ''
        i = 0
        with open(getcwd()+'\\bin\conf.txt', 'rb') as fconfigread:
            alltext =  fconfigread.read()
        fconfigread.closed
        
        text = ''
        if EmailOnlyWhenSomethingChanged == True or EmailOnlyWhenSomethingChanged == 'True':
            text = 'EOWSC|F'
        else:
            text = 'EOWSC|T'
            
        EP =  EmailPref()
        E_text = EP.EncodeInfo(text)
        list = alltext.split('\n')
        list = filter(None, list)
        list.append(E_text)
        fconfig = open(getcwd()+'\\bin\conf.txt', 'wb')
        for singleValue in list:
            fconfig.write(singleValue +"\n")
            
        fconfig.close()            
        XMLFileNameWithDirName = CreateXML(prj , VERSION , RegistrationInfo  , Triggers , Principals , Settings , Actions,interval)
        ############################################################################################################################
        
        XMLFilePath ="\""+ getcwd() + "\\" + XMLFileNameWithDirName + "\""
        Command ="schtasks /Create /TN \"Fixity-" + prj + "\"  /xml "+XMLFilePath
        subprocess.call(Command, startupinfo=startupinfo)
        
        
        
        
def CreateXML(ProjectName , Version , RegistrationInfo  , Triggers , Principals , Settings , Actions,interval):
        Months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
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
        
        if interval == 1:
            xmlsch.write("            <ScheduleByMonth>\n")
            xmlsch.write("                <DaysOfMonth>\n")
            xmlsch.write("                    <Day>" + str(Triggers['CalendarTrigger']['ScheduleByMonth']['DaysOfMonth']) + "</Day>\n")
            xmlsch.write("                </DaysOfMonth >\n")
            xmlsch.write("                <Months>\n")
            for Month in Months:
                xmlsch.write("                <" + Month + "/>\n")

            xmlsch.write("                </Months>\n")
            xmlsch.write("            </ScheduleByMonth>\n")
        if interval == 2:
            xmlsch.write("            <ScheduleByWeek>\n")
            xmlsch.write("                <WeeksInterval >" + str(Triggers['CalendarTrigger']['ScheduleByWeek']['WeeksInterval']) + "</WeeksInterval >\n")
            xmlsch.write("                <DaysOfWeek>\n")
            xmlsch.write("                    <" + str(Triggers['CalendarTrigger']['ScheduleByWeek']['DaysOfWeek']) + "/>\n");
            xmlsch.write("                </DaysOfWeek >\n")
            xmlsch.write("            </ScheduleByWeek>\n")
        if interval == 3:
            xmlsch.write("            <ScheduleByDay>\n")
            xmlsch.write("                <DaysInterval>"+str(Triggers['CalendarTrigger']['ScheduleByDay']['DaysInterval'])+"</DaysInterval>\n")
            xmlsch.write("            </ScheduleByDay>\n") 
        
        xmlsch.write("        </CalendarTrigger>\n")
        xmlsch.write("    </Triggers>\n")
        xmlsch.write("    <Settings>\n")
        xmlsch.write("        <Enabled>"+ Settings['Enabled'] +"</Enabled>\n")
        xmlsch.write("        <AllowStartOnDemand>"+ Settings['AllowStartOnDemand'] +"</AllowStartOnDemand>\n")
        xmlsch.write("        <AllowHardTerminate>"+ Settings['AllowHardTerminate'] +"</AllowHardTerminate>\n")
        xmlsch.write("        <DisallowStartIfOnBatteries>"+ Settings['DisallowStartIfOnBatteries'] +"</DisallowStartIfOnBatteries>\n")
        xmlsch.write("        <StartWhenAvailable>"+ Settings['StartWhenAvailable'] +"</StartWhenAvailable>\n")
        xmlsch.write("        <WakeToRun>"+ Settings['WakeToRun'] +"</WakeToRun>\n")
         
        xmlsch.write("    </Settings>\n")
        xmlsch.write("    <Actions>\n")
        xmlsch.write("        <Exec>\n")
        xmlsch.write("            <Command>"+ Actions['Exec']['Command'] +"</Command>\n")
        xmlsch.write("        </Exec>\n")
        xmlsch.write("      </Actions>\n")
        xmlsch.write("</Task>\n")
        xmlsch.close()
        
        return "schedules\\fixity-" + ProjectName + "-sch.xml"
        
        
        
        
        
        
        
        
        
        