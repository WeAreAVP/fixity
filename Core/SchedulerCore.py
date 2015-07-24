# -*- coding: UTF-8 -*-
#
#@author: Furqan Wasi <furqan@avpreserve.com>
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

    def delTask(self, project):

        """
        Deletes the SCHTASK entry and its corresponding files
        @param project: project Name

        @return: None
        """

        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

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

            AgentPath = self.Fixity.Configuration.getLibAgentPath()
            launch_agent= AgentPath + "Com.fixity."+str(project) + ".demon.plist"

            try:

                if os.path.isfile(launch_agent):
                    p = subprocess.Popen(["launchctl", "unload", "-w", launch_agent] ,stdout=subprocess.PIPE)
                    output, err = p.communicate()
            except:
                self.Fixity.logger.LogException(Exception.message)
                pass

            try:
                os.remove(launch_agent)
            except:
                self.Fixity.logger.LogException()
                pass

    def isUserAdmin(self):
        if os.name == 'nt':
            import ctypes
            # WARNING: requires Windows XP SP2 or higher!
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        elif os.name == 'posix':
            # Check for root on Posix
            return os.getuid() == 0
        else:
            raise RuntimeError, "Unsupported operating system for this module: %s" % (os.name,)

    def schedule(self, title):
        """

        Writes a task to SCHTASKS and creates necessary VBS/BAT files,  ACPowerCheck, StartWhenAvailable,EmailOnlyWhenSomethingChanged

        @param title: Project Name

        @return: None
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass
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
            spec = " /D " + days[int(self.getRun_day_or_month())] + " "
        elif self.getDurationType() == 1:
            spec = " /D " + str(self.getRun_day_or_month()) + " "

        if self.Fixity.Configuration.getOsType() == 'Windows':
            f = open("schedules"+str(os.sep)+"fixity-" + project_name + ".bat", "w")
            try:

                f.write("@ECHO OFF\n")
                f.write("cd /d %~dp0\n")
                f.write("cd ..\n")
                f.write("\"" + os.getcwd()+str(os.sep) + "Fixity.exe\" \"-a=" + project_name + "\"\n")

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
            triggers['CalendarTrigger']['ScheduleByWeek']['DaysOfWeek'] = daysOfWeek[int(self.getRun_day_or_month())]
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
        xml_file_name_with_dir_name = ''
        if self.Fixity.Configuration.getOsType() == 'Windows':
            xml_file_name_with_dir_name = self.CreateXML(project_name,  version,  registration_info, triggers,
                                                         principals,  settings,  actions, self.getDurationType())
        else:
            xml_file_name_with_dir_name = self.CreateXMLOfMac(project_name,  version,  registration_info, triggers,
                                                              principals,  settings,  actions, self.getDurationType())

        xml_file_path = "\"" + xml_file_name_with_dir_name + "\""

        command = ''
        if self.Fixity.Configuration.getOsType() == 'Windows':
            SystemInformation = self.Fixity.Configuration.getWindowsInformation()

            if str(SystemInformation['WindowsType']) == '7':
                command = "schtasks /Create /TN \"Fixity-" + project_name + "\"  /xml " + xml_file_path
            else:
                command = "schtasks /Create /tn \"Fixity-" + project_name + "\" /SC " + mo + spec + " /ST " + timeSch + ' /tr \\""' + os.getcwd() + "\\schedules\\fixity-" + project_name + '.vbs\\"" /RU SYSTEM'

        information = {}
        information['versionType'] = 'save'
        current_date = time.strftime("%Y-%m-%d")
        information['name'] = self.Fixity.Configuration.EncodeInfo(str(current_date))

        if self.Fixity.Configuration.getOsType() == 'Windows':
            try:
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                response = subprocess.call(command, startupinfo=si)
                return {0:response, 1:command}


            except:
                self.Fixity.logger.LogException(Exception.message)
                pass
        else:
            try:
                if os.path.isfile(xml_file_name_with_dir_name):
                    subprocess.Popen(["launchctl", "unload", "-w", xml_file_name_with_dir_name] ,shell=True , stdout=subprocess.PIPE)
            except:
                self.Fixity.logger.LogException(Exception.message)
                pass

            try:
                os.system("launchctl load -w " + xml_file_name_with_dir_name)

            except:
                self.Fixity.logger.LogException(Exception.message)
                pass

        return 1

    def CreateXML(self, project_name,  version,  registration_info,   triggers,  principals,  settings,  actions, interval):
        """
        Create XML for Window 7 task schedules

        Input: information of all scheduler information wit project information
        Output : XML for Window 7 scheduler
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        schedule_path = self.Fixity.Configuration.getSchedulesPath()+"fixity-" + project_name + "-sch.xml"
        xmlsch = open(schedule_path, "w")
        scheduler_xml_text = ''
        scheduler_xml_template_lines = []
        # Months

        if interval == 1:
            if self.isUserAdmin():
                template_monthly_file = open(self.Fixity.Configuration.getSch_month_template_path_admin(), "r")
            else:
                template_monthly_file = open(self.Fixity.Configuration.getSch_month_template_path(), "r")

            scheduler_xml_template_lines = template_monthly_file.readlines()
            template_monthly_file.close()

        # Weeks
        elif interval == 2:
            if self.isUserAdmin():
                template_week_file = open(self.Fixity.Configuration.getSch_week_template_path_admin(), "r")
            else:
                template_week_file = open(self.Fixity.Configuration.getSch_week_template_path(), "r")

            scheduler_xml_template_lines = template_week_file.readlines()
            template_week_file.close()

        # Days
        elif interval == 3:
            if self.isUserAdmin():
                template_days_file = open(self.Fixity.Configuration.getSch_daily_template_path_admin(), "r")
            else:
                print(self.Fixity.Configuration.getSch_daily_template_path())
                template_days_file = open(self.Fixity.Configuration.getSch_daily_template_path(), "r")

            scheduler_xml_template_lines = template_days_file.readlines()
            template_days_file.close()

        for scheduler_xml_template_single_line in scheduler_xml_template_lines:
            scheduler_xml_template_single_line = self.Fixity.Configuration.CleanStringForBreaks(str(scheduler_xml_template_single_line))
            response = False
            response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{current_data_time}}', registration_info['Date'])
            # Attributes Available in only Daily Template
            if interval == 3:
                if response is False:
                    response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{days_interval}}', str(triggers['CalendarTrigger']['ScheduleByDay']['DaysInterval']))

            # Attributes Available in only Weekly Template
            if interval == 2:
                    if response is False:
                        response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{weeks_interval}}', str(triggers['CalendarTrigger']['ScheduleByWeek']['WeeksInterval']))

                    if response is False:
                        response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{day_of_week}}', str(triggers['CalendarTrigger']['ScheduleByWeek']['DaysOfWeek']))

            # Attributes Available in only monthly Template
            if interval == 1:
                if response is False:
                    response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{days_of_month}}', str(triggers['CalendarTrigger']['ScheduleByMonth']['DaysOfMonth']))

            # Attributes Available in all XML Templates
            if response is False:
                response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{user}}', str(registration_info['Author']))

            if response is False:
                response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{version}}', str(self.Fixity.Configuration.getApplicationVersion()))

            if response is False:
                response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{start_boundary}}', str(triggers['CalendarTrigger']['StartBoundary']))

            if response is False:
                response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{enabled}}', settings['Enabled'])

            if response is False:
                response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{allow_start_on_demand}}', settings['AllowStartOnDemand'])

            if response is False:
                response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{allow_hard_terminate}}', settings['AllowHardTerminate'])

            if response is False:

                if settings['DisallowStartIfOnBatteries'] == 'true' or settings['DisallowStartIfOnBatteries'] == True:
                    response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{disallow_start_if_on_batteries}}', 'false')
                else:
                    response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{disallow_start_if_on_batteries}}', 'true')

            if response is False:
                response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{start_when_available}}', settings['StartWhenAvailable'])

            if response is False:
                response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{day_of_week}}', settings['StartWhenAvailable'])

            if response is False:
                response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{wake_to_run}}', settings['WakeToRun'])

            if response is False:
                response = self.setValuesForScheduler(scheduler_xml_template_single_line, '{{command}}', actions['Exec']['Command'])

            if response is False:
                # if no value found to replace
                scheduler_xml_text += str(scheduler_xml_template_single_line)
            else:
                scheduler_xml_text += response

        try:
            xmlsch.write(scheduler_xml_text)
        except:
            pass
        xmlsch.close()

        return schedule_path

    def CreateXMLOfMac(self, project_name,  version,  registration_info,   triggers,  principals,  settings,  actions, interval):
        """
        Create XML for Mac launchd process

        Input: information of all scheduler information with project information
        Output : XML for Mac launhd scheduling
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        try:
            launch_agent= str(self.Fixity.Configuration.getLibAgentPath())+ "Com.fixity."+str(project_name) + ".demon.plist"
            scheduler_xml_text = ''

            xmlsch = open(u''+launch_agent, "w")
            try:
                xmlsch.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
                xmlsch.write("<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n")
                xmlsch.write("    <plist version=\"1.0\">\n")
                xmlsch.write("        <dict>\n")

                xmlsch.write("            <key>Program</key>\n")
                xmlsch.write("                <string>" + str(self.Fixity.Configuration.getFixityLaunchPath()) +"</string>\n")
                # xmlsch.write("                <string>/Applications/TextEdit.app/Contents/MacOS/TextEdit</string>\n")

                xmlsch.write("            <key>Label</key>\n")
                xmlsch.write("            <string>Com.fixity."+str(project_name)+".demon</string>\n")
                xmlsch.write("            <key>ProgramArguments</key>\n")

                xmlsch.write("            <array>\n")
                xmlsch.write("                <string>"+str(self.Fixity.Configuration.getFixityLaunchPath())+"</string>\n")
                # xmlsch.write("                <string>/Applications/TextEdit.app/Contents/MacOS/TextEdit</string>\n")
                xmlsch.write("                <string>-a="+str(project_name)+"</string>\n")
                xmlsch.write("            </array>\n")

                xmlsch.write("            <key>StandardOutPath</key>\n")
                xmlsch.write("            <string>"+str(self.Fixity.Configuration.getDebugFilePath())+"</string>\n")
                xmlsch.write("            <key>StandardErrorPath</key>\n")
                xmlsch.write("            <string>"+str(self.Fixity.Configuration.getDebugFilePath())+"</string>\n")
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
                    week_information = {"Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6}

                    xmlsch.write("            <key>Minute</key>\n")
                    xmlsch.write("            <integer>" + str(trigger_information[1]) + "</integer>\n")
                    xmlsch.write("            <key>Hour</key>\n")
                    xmlsch.write("            <integer>" + str(trigger_information[0]) + "</integer>\n")
                    xmlsch.write("            <key>Weekday</key>\n")
                    xmlsch.write("            <integer>" + str(week_information[triggers['CalendarTrigger']['ScheduleByWeek']['DaysOfWeek']]) + "</integer>\n")

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
            return launch_agent
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

    def setRunTime(self, runTime):self.runTime = runTime

    def getRunTime(self ): return self.runTime

    def setDurationType(self, duration_type):self.duration_type = duration_type

    def getDurationType(self ): return self.duration_type

    def setRun_day_or_month(self, run_day_or_month): self.run_day_or_month = run_day_or_month

    def setRun_when_on_battery(self, run_when_on_battery): self.run_when_on_battery = run_when_on_battery

    def getRun_when_on_battery(self): return self.run_when_on_battery

    def getRun_day_or_month(self ): return self.run_day_or_month

    def setIf_missed_run_upon_restart(self, if_missed_run_upon_restart):self.if_missed_run_upon_restart = if_missed_run_upon_restart

    def getIf_missed_run_upon_restart(self): return self.if_missed_run_upon_restart

    def setEmail_only_upon_warning(self, email_only_upon_warning):self.email_only_upon_warning = email_only_upon_warning

    def getEmail_only_upon_warning(self): return self.email_only_upon_warning

    def setValuesForScheduler(self, string, find_string, replace_with_string):

        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        string = str(string)
        find_string = str(find_string)
        replace_with_string = str(replace_with_string)
        if find_string in string:
            return str(string).replace(find_string, replace_with_string) + '\n'
        return False