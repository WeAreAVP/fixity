# Fixity Scheduler
# Version 0.3, 2013-12-16
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
'''
Updated on Feb 4, 2014
@author: Furqan Wasi  <furqan@geekschicago.com>
'''
import os
OS_Info = ''
if os.name == 'posix':
    OS_Info = 'linux'
elif os.name == 'nt':
    OS_Info = 'Windows'
elif os.name == 'os2':
    OS_Info = 'check'

import subprocess
from os import getcwd, remove , environ , path, remove
from os.path import expanduser

import sys
import time

from Debuger import Debuger
from EmailPref import EmailPref
from Database import Database


Debuging = Debuger()

# Deletes the SCHTASK entry and its corresponding files
def deltask(project):
    if OS_Info == 'Windows':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.call("schtasks /Delete /F /TN \"Fixity-" + project.replace(' ', '_') + "\"", startupinfo=startupinfo)


        try:
            remove("schedules\\fixity-" + project + ".bat")
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

            Debuging.tureDebugerOn()
            Debuging.logError('Could Not Remove File Line 22 File FixtyScheduleTask' + "schedules\\fixity-" + project + ".bat", moreInformation)
            pass
        try:
                remove("schedules\\fixity-" + project + ".vbs")
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

            Debuging.tureDebugerOn()
            Debuging.logError('Count not Remove File ,  Line 35 File FixtyScheduleTask' + "schedules\\fixity-" + project + ".vbs", moreInformation)
            pass
#Runs Given Batch File
def RunThisBatchFile(Command):
    if OS_Info == 'Windows':
        subprocess.call(Command, shell=True)

# Writes a task to SCHTASKS and creates necessary VBS/BAT files , ACPowerCheck, StartWhenAvailable,EmailOnlyWhenSomethingChanged
def schedule(interval, dow, dom, timeSch, project, Configurations,SystemInformation,dirInfo = {}):

        EP = EmailPref(None)
        VERSION = EP.getVersion()
        USERNAME = environ.get("USERNAME")
        prj = project.replace(' ', '_')

        deltask(prj)
        mo = ""
        spec = ""
        if Configurations['runDayOrMonth'] == 1:
            mo = "MONTHLY"
        if Configurations['runDayOrMonth'] == 2:
            mo = "WEEKLY"
        if Configurations['runDayOrMonth'] == 3:
            mo = "DAILY"

        if dow != 99:
                days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
                spec = " /D " + days[dow] + " "
        elif dom != 99:
                spec = " /D " + str(dom) + " "
        if OS_Info == 'Windows':
            f = open("schedules\\fixity-" + prj + ".bat", "w")
            try:
                f.write("@ECHO OFF\n")
                f.write("cd /d %~dp0\n")
                f.write("cd ..\n")
                f.write("\"" + getcwd() + "\\schedules\\AutoFixity.exe\" \"" + prj + "\"\n")
            except:
                pass
            f.close()

            x = open("schedules\\fixity-" + prj + ".vbs", "w")
            try:
                x.write("Dim location, p\n")
                x.write("location = WScript.ScriptFullName\n")
                x.write("p = Replace(location, \"fixity-" + prj + ".vbs\", \"fixity-" + prj + ".bat\")\n")
                x.write("Set WinScriptHost = CreateObject(\"WScript.Shell\")\n")
                x.write('WinScriptHost.Run("""" & p & """")')
                x.write("\n")
                x.write("Set WinScriptHost = Nothing")
            except:
                pass
            x.close()
        pathCommand= ''
        if OS_Info == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            pathCommand = "\"" + getcwd() + "\\schedules\\fixity-" + prj + ".vbs\""

        ############################################################################################################################

        # TODO Time Zone Handling
        # TASK SCHEDULER OPTION and ATTRIBUTES
        RegistrationInfo = {}
        Triggers = {}
        Principals = {}
        Settings = {}
        Actions = {}

        RegistrationInfo['Date'] = time.strftime("%Y-%m-%dT%X")  # 2005-10-11T13:21:17-08:00
        RegistrationInfo['Author'] = USERNAME
        RegistrationInfo['Version'] = VERSION
        RegistrationInfo['Description'] = 'Fixity Task Scheduler to Monitor A Folder Activity!'

        CurrentDate = time.strftime("%Y-%m-%d")
        EndBoundary = '2015-12-12'
        Triggers['CalendarTrigger'] = {}
        Triggers['CalendarTrigger']['StartBoundary'] = CurrentDate + 'T' + timeSch
        Triggers['CalendarTrigger']['EndBoundary'] = EndBoundary + 'T' + timeSch
        Triggers['CalendarTrigger']['Repetition'] = {}
        Triggers['CalendarTrigger']['ScheduleByDay'] = {}

        Triggers['CalendarTrigger']['ScheduleByMonth'] = {}
        Triggers['CalendarTrigger']['ScheduleByMonth']['DaysOfMonth'] = {}
        Triggers['CalendarTrigger']['Repetition']['Interval'] = ''
        Triggers['CalendarTrigger']['Repetition']['Duration'] = ''

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
            Triggers['CalendarTrigger']['ScheduleByDay']['DaysInterval'] = '1'

        Principals['Principal'] = {}
        Principals['Principal']['UserId'] = 'Administrator'
        Principals['Principal']['LogonType'] = 'InteractiveToken'

        Settings['Enabled'] = 'true'
        Settings['AllowStartOnDemand'] = 'true'
        Settings['AllowHardTerminate'] = 'true'
        Settings['WakeToRun'] = 'true'

        if Configurations['ifMissedRunUponRestart'] == 1 or Configurations['ifMissedRunUponRestart'] == '1':
            IfMissedRunUponAvailable = 'IMRUA|T'
            Settings['StartWhenAvailable'] = 'true'
        else:
            IfMissedRunUponAvailable = 'IMRUA|F'
            Settings['StartWhenAvailable'] = 'false'

        if Configurations['runWhenOnBattery'] == 1 or Configurations['runWhenOnBattery'] == '1':
            Settings['DisallowStartIfOnBatteries'] = 'false'
            RunWhenOnBatteryPower = 'RWOBP|T'
        else:
            Settings['DisallowStartIfOnBatteries'] = 'true'
            RunWhenOnBatteryPower = 'RWOBP|F'

        RunInitialScan = 'RIS|T'

        Actions['Exec'] = {}
        Actions['Exec']['Command'] = pathCommand
        text = ''
        if Configurations['emailOnlyUponWarning'] == 1 or Configurations['emailOnlyUponWarning'] == '1':
            text = 'EOWSC|F'
        else:
            text = 'EOWSC|T'

        E_text = text

        information = EP.getConfigInfo(prj)

        information['emailUponWarning'] = E_text
        information['ifMissedRunUponRestart'] = IfMissedRunUponAvailable
        information['runWhenOnBattery'] = RunWhenOnBatteryPower
        information['RunInitialScan'] = RunInitialScan
        XMLFileNameWithDirName = ''
        if OS_Info == 'Windows':
            XMLFileNameWithDirName = CreateXML(prj , VERSION , RegistrationInfo  , Triggers , Principals , Settings , Actions, interval)
        else:
            XMLFileNameWithDirName = CreateXMLOfMac(prj , VERSION , RegistrationInfo  , Triggers , Principals , Settings , Actions, interval)
        ############################################################################################################################

        XMLFilePath = "\"" + getcwd() + "\\" + XMLFileNameWithDirName + "\""
        Command = ''
        if OS_Info == 'Windows':
            if(str(SystemInformation['WindowsType']) == '7'):
                Command = "schtasks /Create /TN \"Fixity-" + prj + "\"  /xml " + XMLFilePath
            else:
                Command = "schtasks /Create /tn \"Fixity-" + prj + "\" /SC " + mo + spec + " /ST " + timeSch + " /tr \"" + getcwd() + "\\schedules\\fixity-" + prj + ".vbs\" /RU SYSTEM"

        DB = Database()
        isProjectExists = DB.select(DB._tableProject,'id',"title like '"+str(Configurations['title'])+"'")

        Information = {}
        Information['versionType'] = 'save'
        CurrentDate = time.strftime("%Y-%m-%d")
        Information['name'] = EP.EncodeInfo(str(CurrentDate))

        versionID  = DB.insert(DB._tableVersions, Information)

        projectID = 0
        if (len(isProjectExists) <= 0):
            Configurations['versionCurrentID'] = versionID['id']
            projectID = DB.insert(DB._tableProject, Configurations)
            projectID = projectID['id']
        else:
            projectID = isProjectExists[0]['id']
            Configurations['versionCurrentID'] = versionID['id']
            DB.update(DB._tableProject, Configurations,"id = '" + str(projectID) + "'")

        counter = 1
        for ms in dirInfo:
            if (str(dirInfo[ms]) != ''):
                PathsInfo = {}
                PathsInfo['projectID'] = projectID
                PathsInfo['versionID'] = versionID['id']
                PathsInfo['path'] = str(dirInfo[ms]).strip()
                PathsInfo['pathID'] = 'Fixity-' + str(counter)

                DB.insert(DB._tableProjectPath, PathsInfo)

                counter = counter + 1
        try:
            if OS_Info == 'Windows':
                subprocess.call(Command , startupinfo=startupinfo)
            else:

                try:
                    p = subprocess.Popen(["launchctl", "unload", "-w", XMLFileNameWithDirName], stdout=subprocess.PIPE)
                    output, err = p.communicate()
                except:
                    pass

                try:
                    p = subprocess.Popen(["launchctl", "load", "-w", XMLFileNameWithDirName], stdout=subprocess.PIPE)
                    output, err = p.communicate()
                except:
                    pass

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

            Debuging.tureDebugerOn()
            Debuging.logError('Create scheduler Command could not run Line range 197 File FixitySchtask ', moreInformation)
            pass

#Create XML for Window 7 task schedules
def CreateXML(ProjectName , Version , RegistrationInfo  , Triggers , Principals , Settings , Actions, interval):
        Months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        xmlsch = open("schedules\\fixity-" + ProjectName + "-sch.xml", "w")
        try:
            xmlsch.write("<?xml version=\"1.0\" ?>\n")
            xmlsch.write("<Task xmlns=\"http://schemas.microsoft.com/windows/2004/02/mit/task\">\n")
            xmlsch.write("    <RegistrationInfo>\n")
            xmlsch.write("        <Date>" + RegistrationInfo['Date'] + "</Date>\n")
            xmlsch.write("        <Author>" + RegistrationInfo['Author'] + "</Author>\n")
            xmlsch.write("        <Version>" + RegistrationInfo['Description'] + "</Version>\n")
            xmlsch.write("        <Description>" + RegistrationInfo['Description'] + "</Description>\n")
            xmlsch.write("    </RegistrationInfo>\n")
            xmlsch.write("    <Triggers>\n")
            xmlsch.write("        <CalendarTrigger>\n")
            xmlsch.write("            <StartBoundary>" + Triggers['CalendarTrigger']['StartBoundary'] + "</StartBoundary>\n")

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
                xmlsch.write("                <DaysInterval>" + str(Triggers['CalendarTrigger']['ScheduleByDay']['DaysInterval']) + "</DaysInterval>\n")
                xmlsch.write("            </ScheduleByDay>\n")

            xmlsch.write("        </CalendarTrigger>\n")
            xmlsch.write("    </Triggers>\n")
            xmlsch.write("    <Settings>\n")
            xmlsch.write("        <Enabled>" + Settings['Enabled'] + "</Enabled>\n")
            xmlsch.write("        <AllowStartOnDemand>" + Settings['AllowStartOnDemand'] + "</AllowStartOnDemand>\n")
            xmlsch.write("        <AllowHardTerminate>" + Settings['AllowHardTerminate'] + "</AllowHardTerminate>\n")
            xmlsch.write("        <DisallowStartIfOnBatteries>" + Settings['DisallowStartIfOnBatteries'] + "</DisallowStartIfOnBatteries>\n")
            xmlsch.write("        <StartWhenAvailable>" + Settings['StartWhenAvailable'] + "</StartWhenAvailable>\n")
            xmlsch.write("        <WakeToRun>" + Settings['WakeToRun'] + "</WakeToRun>\n")

            xmlsch.write("    </Settings>\n")
            xmlsch.write("    <Actions>\n")
            xmlsch.write("        <Exec>\n")
            xmlsch.write("            <Command>" + Actions['Exec']['Command'] + "</Command>\n")
            xmlsch.write("        </Exec>\n")
            xmlsch.write("      </Actions>\n")
            xmlsch.write("</Task>\n")
        except:
            pass
        xmlsch.close()

        return "schedules\\fixity-" + ProjectName + "-sch.xml"

#Create XML for Mac launchd process
def CreateXMLOfMac(ProjectName , Version , RegistrationInfo  , Triggers , Principals , Settings , Actions, interval):

        Months = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
        homePath = expanduser("~")
        LibPath = homePath+str(os.sep)+"Library"
        AgentPath = homePath+str(os.sep)+"Library"+str(os.sep)+"LaunchAgents"+str(os.sep)

        if(not os.path.isdir(LibPath)) or (not os.path.isdir(AgentPath)):
                os.makedirs(AgentPath)

        pathInfo = str(getcwd()).replace(str(os.sep)+'Contents'+str(os.sep)+'Resources','') +str(os.sep)+"Contents"+str(os.sep)+"MacOS"+str(os.sep)+"Fixity"
        lunchAject= AgentPath +str(os.sep)+ "Com.fixity."+str(ProjectName) + ".demon.plist"

        lunchAject =str(lunchAject).replace(' ','\\ ')
        pathInfo =str(pathInfo).replace(' ','\\ ')

        xmlsch = open(u''+lunchAject, "w")
        try:
            xmlsch.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            xmlsch.write("<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n")
            xmlsch.write("    <plist version=\"1.0\">\n")
            xmlsch.write("        <dict>\n")
            xmlsch.write("            <key>Program</key>\n")
            xmlsch.write("                <string>" + str(pathInfo) +"</string>\n")
            xmlsch.write("            <key>Label</key>\n")
            xmlsch.write("            <string>Com.fixity."+str(ProjectName)+".demon</string>\n")
            xmlsch.write("            <key>ProgramArguments</key>\n")
            xmlsch.write("            <array>\n")
            xmlsch.write("                <string>"+pathInfo+"</string>\n")
            xmlsch.write("                <string>-a="+str(ProjectName)+"</string>\n")
            xmlsch.write("            </array>\n")
            xmlsch.write("            <key>StandardOutPath</key>\n")
            xmlsch.write("            <string>"+str(getcwd())+"/debug/debug.log</string>\n")
            xmlsch.write("            <key>StandardErrorPath</key>\n")
            xmlsch.write("            <string>"+str(getcwd())+"/debug/debug.log</string>\n")
            xmlsch.write("            <key>StartCalendarInterval</key>\n")
            xmlsch.write("            <dict>\n")

            infoTrigger = str(Triggers['CalendarTrigger']['StartBoundary']).split('T')
            TriggerInformation = str(infoTrigger[1]).split(':')

            if interval == 1:
                xmlsch.write("            <key>Minute</key>\n")
                xmlsch.write("            <integer>" + str(TriggerInformation[1]) + "</integer>\n")
                xmlsch.write("            <key>Hour</key>\n")
                xmlsch.write("            <integer>" + str(TriggerInformation[0]) + "</integer>\n")
                xmlsch.write("            <key>Day</key>\n")
                xmlsch.write("            <integer>" + str(Triggers['CalendarTrigger']['ScheduleByMonth']['DaysOfMonth']) + "</integer>\n")

            if interval == 2:
                xmlsch.write("            <key>Minute</key>\n")
                xmlsch.write("            <integer>" + str(TriggerInformation[1]) + "</integer>\n")
                xmlsch.write("            <key>Hour</key>\n")
                xmlsch.write("            <integer>" + str(TriggerInformation[0]) + "</integer>\n")
                xmlsch.write("            <key>Weekday</key>\n")
                xmlsch.write("            <integer>" + str(Triggers['CalendarTrigger']['ScheduleByWeek']['WeeksInterval']) + "</integer>\n")

            if interval == 3:
                xmlsch.write("            <key>Minute</key>\n")
                xmlsch.write("            <integer>" + str(TriggerInformation[1]) + "</integer>\n")
                xmlsch.write("            <key>Hour</key>\n")
                xmlsch.write("            <integer>" + str(TriggerInformation[0]) + "</integer>\n")

            xmlsch.write("            </dict>\n")
            xmlsch.write("        </dict>\n")
            xmlsch.write("    </plist>\n")
        except:
            pass

        xmlsch.close()
        return lunchAject