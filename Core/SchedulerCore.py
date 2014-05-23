import os, subprocess, time
from Core import SharedApp


class SchedulerCore(object):

    def __init__(self):
        self.run_day_or_month = None
        self.if_missed_run_upon_restart = None
        self.email_only_upon_warning = None
        self.run_when_on_battery = None
        self.duration_type = None
        self.Fixity = SharedApp.SharedApp.App


    #Deletes the SCHTASK entry and its corresponding files
    #@param project: project Name
    #
    #@return: None
    def delTask(self, project):
        if self.Fixity.Configuration.getOsType() == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.call("schtasks /Delete /F /TN \"Fixity-" + project.replace(' ', '_') + "\"", startupinfo=startupinfo)

            try:
                os.remove(str(self.Fixity.Configuration.getSchedulesPath()) + str(os.sep) + "fixity-" + project + ".bat")
            except:
                pass


            try:
                os.remove(str(self.Fixity.Configuration.getSchedulesPath()) + "fixity-" + project + ".bat")
            except:
                pass


            try:
                os.remove(str(self.Fixity.Configuration.getSchedulesPath()) + "fixity-" + project + "-sch.xml")
            except:
                pass

            try:
                os.remove(str(self.Fixity.Configuration.getSchedulesPath()) + "fixity-" + project + ".vbs")
            except:
                pass
        else:
            try:
                AgentPath = self.Fixity.Configuration.getAgentPath()
                lunch_agent= AgentPath +str(os.sep)+ "Com.fixity."+str(project) + ".demon.plist"
            except:
                self.Fixity.logger.LogException(Exception.message)

            try:
                p = subprocess.Popen(["launchctl", "unload", "-w", lunch_agent], stdout=subprocess.PIPE)
                output, err = p.communicate()
            except:
                self.Fixity.logger.LogException(Exception.message)
                pass

            try:
                os.remove(lunch_agent)
            except:
                self.Fixity.logger.LogException()
                pass

    #Writes a task to SCHTASKS and creates necessary VBS/BAT files,  ACPowerCheck, StartWhenAvailable,EmailOnlyWhenSomethingChanged
    #
    #@param interval: Interval
    #@param dow: List of all Directory
    #@param dom: List of all Email's
    #@param timeSch: time of Scheduler
    #@param project: Project
    #@param Configurations:  Configurations
    #@param SystemInformation: System Information
    #@param dirInfo: Directory Information
    #@return: None

    def schedule(self, title):

        timeSch = self.getRunTime()
        version = self.Fixity.Configuration.getApplicationVersion()

        username = os.environ.get("USERNAME")
        project_name = title

        mo = ""
        spec = ""

        if self.getDurationType() == 1:
            mo = "MONTHLY"

        if self.getDurationType() == 2:
            mo = "WEEKLY"

        if self.getDurationType() == 3:
            mo = "DAILY"

        if self.getDurationType() == 2:
                days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
                spec = " /D " + days[self.getRun_day_or_month()] + " "
        elif self.getDurationType() == 1:
                spec = " /D " + str(self.getRun_day_or_month()) + " "

        if self.Fixity.Configuration.getOsType() == 'Windows':
            f = open("schedules"+str(os.sep)+"fixity-" + project_name + ".bat", "w")
            try:

                f.write("@ECHO OFF\n")
                f.write("cd /d %~dp0\n")
                f.write("cd ..\n")
                f.write("\"" + os.getcwd()+str(os.sep) + "main.exe\" \"-a=" + project_name + "\"\n")

            except:
                self.Fixity.logger.LogException(Exception.message)
            f.close()

            x = open("schedules\\fixity-" + project_name + ".vbs", "w")
            try:

                x.write("Dim location, p\n")
                x.write("location = WScript.ScriptFullName\n")
                x.write("p = Replace(location, \"fixity-" + project_name + ".vbs\", \"fixity-" + project_name + ".bat\")\n")
                x.write("Set WinScriptHost = CreateObject(\"WScript.Shell\")\n")
                x.write('WinScriptHost.Run("""" & p & """")')
                x.write("\n")
                x.write("Set WinScriptHost = Nothing")

            except:
                self.Fixity.logger.LogException(Exception.message)
            x.close()

        pathCommand= ''

        if self.Fixity.Configuration.getOsType() == 'Windows':

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            pathCommand = "\"" + self.Fixity.Configuration.getSchedulesPath()+"fixity-" + project_name + ".vbs\""

        # TASK SCHEDULER OPTION and ATTRIBUTES
        registration_info = {}
        triggers = {}
        principals = {}
        settings = {}
        actions = {}

        registration_info['Date'] = time.strftime("%Y-%m-%dT%X")  # 2005-10-11T13:21:17-08:00
        registration_info['Author'] = username
        registration_info['Version'] = version
        registration_info['Description'] = 'Fixity Task Scheduler to Monitor A Folder Activity!'

        current_date = time.strftime("%Y-%m-%d")
        end_boundary = '2200-12-12'

        triggers['CalendarTrigger'] = {}
        triggers['CalendarTrigger']['StartBoundary'] = current_date + 'T' + timeSch
        triggers['CalendarTrigger']['end_boundary'] = end_boundary + 'T' + timeSch
        triggers['CalendarTrigger']['Repetition'] = {}
        triggers['CalendarTrigger']['ScheduleByDay'] = {}

        triggers['CalendarTrigger']['ScheduleByMonth'] = {}
        triggers['CalendarTrigger']['ScheduleByMonth']['DaysOfMonth'] = {}
        triggers['CalendarTrigger']['Repetition']['Interval'] = ''
        triggers['CalendarTrigger']['Repetition']['Duration'] = ''

        if self.getDurationType() == 1:

            triggers['CalendarTrigger']['ScheduleByMonth'] = {}
            triggers['CalendarTrigger']['ScheduleByMonth']['DaysOfMonth'] = self.getRun_day_or_month()

        if self.getDurationType() == 2:

            daysOfWeek = self.Fixity.Configuration.getWeekDays()
            triggers['CalendarTrigger']['ScheduleByWeek'] = {}
            triggers['CalendarTrigger']['ScheduleByWeek']['DaysOfWeek'] = {}
            triggers['CalendarTrigger']['ScheduleByWeek']['WeeksInterval'] = '1'
            triggers['CalendarTrigger']['ScheduleByWeek']['DaysOfWeek'] = daysOfWeek[self.getRun_day_or_month()]
        if self.getDurationType() == 3:
            triggers['CalendarTrigger']['ScheduleByDay']['DaysInterval'] = '1'


        principals['Principal'] = {}
        principals['Principal']['UserId'] = 'Administrator'
        principals['Principal']['LogonType'] = 'InteractiveToken'

        settings['Enabled'] = 'true'
        settings['AllowStartOnDemand'] = 'true'
        settings['AllowHardTerminate'] = 'true'
        settings['WakeToRun'] = 'true'
        settings['DisallowStartIfOnBatteries'] = 'true'

        if self.getRun_when_on_battery() == 1:
            settings['DisallowStartIfOnBatteries'] = 'true'
        else:
            settings['DisallowStartIfOnBatteries'] = 'false'

        if self.getIf_missed_run_upon_restart() == 1:
            settings['StartWhenAvailable'] = 'true'
        else:
            settings['StartWhenAvailable'] = 'false'

        actions['Exec'] = {}
        actions['Exec']['Command'] = pathCommand

        information = self.Fixity.Configuration.getEmailConfiguration()
        information['emailUponWarning'] = self.getEmail_only_upon_warning()
        information['ifMissedRunUponRestart'] = self.getIf_missed_run_upon_restart()
        information['runWhenOnBattery'] = self.getRun_when_on_battery()
        information['RunInitialScan'] = 0
        
        

        if self.Fixity.Configuration.getOsType() == 'Windows':
            xml_file_name_with_dir_name = self.CreateXML(project_name,  version,  registration_info, triggers,  principals,  settings,  actions, self.getDurationType())
        else:
            xml_file_name_with_dir_name = self.CreateXMLOfMac(project_name,  version,  registration_info, triggers,  principals,  settings,  actions, self.getDurationType())

        xml_file_path = "\"" + os.getcwd() + "\\" + xml_file_name_with_dir_name + "\""

        command = ''
        if self.Fixity.Configuration.getOsType() == 'Windows':
            SystemInformation = self.Fixity.Configuration.getWindowsInformation()
            if(str(SystemInformation['WindowsType']) == '7'):
                command = "schtasks /Create /TN \"Fixity-" + project_name + "\"  /xml " + xml_file_path
            else:
                command = "schtasks /Create /tn \"Fixity-" + project_name + "\" /SC " + mo + spec + " /ST " + timeSch + " /tr \"" + os.getcwd() + "\\schedules\\fixity-" + project_name + ".vbs\" /RU SYSTEM"

        Information = {}
        Information['versionType'] = 'save'
        current_date = time.strftime("%Y-%m-%d")
        Information['name'] = self.Fixity.Configuration.EncodeInfo(str(current_date))

        if self.Fixity.Configuration.getOsType() == 'Windows':
            try:
                p = subprocess.call(command, startupinfo=startupinfo)
            except:
                self.Fixity.logger.LogException(Exception.message)
                pass
        else:
            try:
                p = subprocess.Popen(["launchctl", "unload", "-w", xml_file_name_with_dir_name], stdout=subprocess.PIPE)
            except:
                self.Fixity.logger.LogException(Exception.message)
                pass
            try:
                p = subprocess.Popen(["launchctl", "load", "-w", xml_file_name_with_dir_name], stdout=subprocess.PIPE)
            except:
                self.Fixity.logger.LogException(Exception.message)
                pass


    #Create XML for Window 7 task schedules
    #
    #Input: Information of all scheduler information wit project information
    #Output : XML for Window 7 scheduler
    def CreateXML(self, project_name,  version,  registration_info,   triggers,  principals,  settings,  actions, interval):

        Months = self.Fixity.Configuration.getMonths()
        xmlsch = open("schedules\\fixity-" + project_name + "-sch.xml", "w")
        try:
            xmlsch.write("<?xml version=\"1.0\" ?>\n")
            xmlsch.write("<Task xmlns=\"http://schemas.microsoft.com/windows/2004/02/mit/task\">\n")
            xmlsch.write("    <RegistrationInfo>\n")
            xmlsch.write("        <Date>" + registration_info['Date'] + "</Date>\n")
            xmlsch.write("        <Author>" + registration_info['Author'] + "</Author>\n")
            xmlsch.write("        <Version>" + registration_info['Description'] + "</Version>\n")
            xmlsch.write("        <Description>" + registration_info['Description'] + "</Description>\n")
            xmlsch.write("    </RegistrationInfo>\n")
            xmlsch.write("    <Triggers>\n")
            xmlsch.write("        <CalendarTrigger>\n")
            xmlsch.write("            <StartBoundary>" + triggers['CalendarTrigger']['StartBoundary'] + "</StartBoundary>\n")
            if interval == 1:
                xmlsch.write("            <ScheduleByMonth>\n")
                xmlsch.write("                <DaysOfMonth>\n")
                xmlsch.write("                    <Day>" + str(triggers['CalendarTrigger']['ScheduleByMonth']['DaysOfMonth']) + "</Day>\n")
                xmlsch.write("                </DaysOfMonth >\n")
                xmlsch.write("                <Months>\n")
                for Month in Months:
                    xmlsch.write("                <" + Month + "/>\n")
                xmlsch.write("                </Months>\n")
                xmlsch.write("            </ScheduleByMonth>\n")
            if interval == 2:
                xmlsch.write("            <ScheduleByWeek>\n")
                xmlsch.write("                <WeeksInterval >" + str(triggers['CalendarTrigger']['ScheduleByWeek']['WeeksInterval']) + "</WeeksInterval >\n")
                xmlsch.write("                <DaysOfWeek>\n")
                xmlsch.write("                    <" + str(triggers['CalendarTrigger']['ScheduleByWeek']['DaysOfWeek']) + "/>\n")
                xmlsch.write("                </DaysOfWeek >\n")
                xmlsch.write("            </ScheduleByWeek>\n")
            if interval == 3:
                xmlsch.write("            <ScheduleByDay>\n")
                xmlsch.write("                <DaysInterval>" + str(triggers['CalendarTrigger']['ScheduleByDay']['DaysInterval']) + "</DaysInterval>\n")
                xmlsch.write("            </ScheduleByDay>\n")

            xmlsch.write("        </CalendarTrigger>\n")
            xmlsch.write("    </Triggers>\n")
            xmlsch.write("    <Settings>\n")
            xmlsch.write("        <Enabled>" + settings['Enabled'] + "</Enabled>\n")
            xmlsch.write("        <AllowStartOnDemand>" + settings['AllowStartOnDemand'] + "</AllowStartOnDemand>\n")
            xmlsch.write("        <AllowHardTerminate>" + settings['AllowHardTerminate'] + "</AllowHardTerminate>\n")
            xmlsch.write("        <DisallowStartIfOnBatteries>" + settings['DisallowStartIfOnBatteries'] + "</DisallowStartIfOnBatteries>\n")
            xmlsch.write("        <StartWhenAvailable>" + settings['StartWhenAvailable'] + "</StartWhenAvailable>\n")
            xmlsch.write("        <WakeToRun>" + settings['WakeToRun'] + "</WakeToRun>\n")

            xmlsch.write("    </Settings>\n")
            xmlsch.write("    <Actions>\n")
            xmlsch.write("        <Exec>\n")
            xmlsch.write("            <Command>" + actions['Exec']['Command'] + "</Command>\n")
            xmlsch.write("        </Exec>\n")
            xmlsch.write("      </Actions>\n")
            xmlsch.write("</Task>\n")
        except:
            pass
        xmlsch.close()

        return "schedules"+str(os.sep)+"fixity-" + project_name + "-sch.xml"


    #Create XML for Mac launchd process
    #
    #Input: Information of all scheduler information with project information
    #Output : XML for Mac launhd scheduling
    def CreateXMLOfMac(self, project_name,  version,  registration_info,   triggers,  principals,  settings,  actions, interval):

        agent_path = self.Fixity.Configuration.getAgentPath()

        pathInfo = str(os.getcwd()).replace(str(os.sep)+'Contents'+str(os.sep)+'Resources','') +str(os.sep)+"Contents"+str(os.sep)+"MacOS"+str(os.sep)+"Fixity"
        lunch_agent= agent_path +str(os.sep)+ "Com.fixity."+str(project_name) + ".demon.plist"

        lunch_agent =str(lunch_agent).replace(' ','\\ ')
        pathInfo =str(pathInfo).replace(' ','\\ ')

        xmlsch = open(u''+lunch_agent, "w")
        try:
            xmlsch.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            xmlsch.write("<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n")
            xmlsch.write("    <plist version=\"1.0\">\n")
            xmlsch.write("        <dict>\n")

            xmlsch.write("            <key>Program</key>\n")
            xmlsch.write("                <string>" + str(pathInfo) +"</string>\n")
            xmlsch.write("            <key>Label</key>\n")
            xmlsch.write("            <string>Com.fixity."+str(project_name)+".demon</string>\n")
            xmlsch.write("            <key>ProgramArguments</key>\n")

            xmlsch.write("            <array>\n")
            xmlsch.write("                <string>"+pathInfo+"</string>\n")
            xmlsch.write("                <string>-a="+str(project_name)+"</string>\n")
            xmlsch.write("            </array>\n")

            xmlsch.write("            <key>StandardOutPath</key>\n")
            xmlsch.write("            <string>"+str(os.getcwd())+"/debug/debug.log</string>\n")
            xmlsch.write("            <key>StandardErrorPath</key>\n")
            xmlsch.write("            <string>"+str(os.getcwd())+"/debug/debug.log</string>\n")
            xmlsch.write("            <key>StartCalendarInterval</key>\n")
            xmlsch.write("            <dict>\n")

            infoTrigger = str(triggers['CalendarTrigger']['StartBoundary']).split('T')
            trigger_information = str(infoTrigger[1]).split(':')
            if interval == 1:
                xmlsch.write("            <key>Minute</key>\n")
                xmlsch.write("            <integer>" + str(trigger_information[1]) + "</integer>\n")
                xmlsch.write("            <key>Hour</key>\n")
                xmlsch.write("            <integer>" + str(trigger_information[0]) + "</integer>\n")
                xmlsch.write("            <key>Day</key>\n")
                xmlsch.write("            <integer>" + str(triggers['CalendarTrigger']['ScheduleByMonth']['DaysOfMonth']) + "</integer>\n")
            if interval == 2:
                WeekInformation = self.Fixity.Configuration.getWeekInformation()
                xmlsch.write("            <key>Minute</key>\n")
                xmlsch.write("            <integer>" + str(trigger_information[1]) + "</integer>\n")
                xmlsch.write("            <key>Hour</key>\n")
                xmlsch.write("            <integer>" + str(trigger_information[0]) + "</integer>\n")
                xmlsch.write("            <key>Weekday</key>\n")
                xmlsch.write("            <integer>" + str(WeekInformation[triggers['CalendarTrigger']['ScheduleByWeek']['DaysOfWeek']]) + "</integer>\n")
            if interval == 3:
                xmlsch.write("            <key>Minute</key>\n")
                xmlsch.write("            <integer>" + str(trigger_information[1]) + "</integer>\n")
                xmlsch.write("            <key>Hour</key>\n")
                xmlsch.write("            <integer>" + str(trigger_information[0]) + "</integer>\n")
            xmlsch.write("            </dict>\n")
            xmlsch.write("        </dict>\n")
            xmlsch.write("    </plist>\n")
        except:
            pass
        xmlsch.close()
        return lunch_agent

    def setRunTime(self, runTime):self.runTime = runTime
    def getRunTime(self ):return self.runTime
    def setDurationType(self, duration_type):self.duration_type = duration_type
    def getDurationType(self ):return self.duration_type
    def setRun_day_or_month(self, run_day_or_month):self.run_day_or_month = run_day_or_month
    def setRun_when_on_battery(self, run_when_on_battery):self.run_when_on_battery = run_when_on_battery
    def getRun_when_on_battery(self):return self.run_when_on_battery
    def getRun_day_or_month(self ):return self.run_day_or_month
    def setIf_missed_run_upon_restart(self, if_missed_run_upon_restart):self.if_missed_run_upon_restart = if_missed_run_upon_restart
    def getIf_missed_run_upon_restart(self):return self.if_missed_run_upon_restart
    def setEmail_only_upon_warning(self, email_only_upon_warning):self.email_only_upon_warning = email_only_upon_warning
    def getEmail_only_upon_warning(self):return self.email_only_upon_warning