# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''
import os, datetime, sys, platform, base64
from Core.SharedApp import SharedApp


class Configuration(object):
    def __init__(self):

        # Constructor
        if os.name == 'posix':
            self.OsType = 'linux'
        elif os.name == 'nt':
            self.OsType = 'Windows'
        elif os.name == 'os2':
            self.OsType = 'check'

        self.Fixity = SharedApp.App
        self.application_name = 'Fixity'
        self.application_version = '0.4'
        self.change_file = 'Changed File'
        self.move_or_renamed_file = 'Moved or Renamed File'
        self.confirmed_file = 'Confirmed File'
        self.new_file = 'New File'
        self.user_home_path = os.path.expanduser('~')

        if self.OsType == 'Windows':
            self.base_path = str(os.getcwd())+str(os.sep)
            self.reports_path = r''+(os.path.join(self.base_path, 'reports'+str(os.sep)))
            self.schedules_path = r''+(os.path.join(self.base_path, 'schedules'+str(os.sep)))
            self.history_path = r''+(os.path.join(self.base_path, 'history'+str(os.sep)))
            self.bin_path = r''+(os.path.join(self.base_path, 'bin'+str(os.sep)))
            self.assets_path = r''+(os.path.join(self.base_path, 'assets'+str(os.sep)))
            self.lock_file_path = r''+(os.path.join(self.base_path, 'dblocker.log'))
            self.log_file_path = r''+(os.path.join(self.base_path, 'debug.log'))
            self.database_file_path = r''+(os.path.join(self.base_path,'Fixity.db'))
            self.template_path = r''+(os.path.join(self.assets_path,'template')+str(os.sep))
            self.report_template_path = r''+(os.path.join(self.template_path)+'Report.txt')
            self.history_template_path = r''+(os.path.join(self.template_path)+'History.txt')
            self.report_email_template_path = r''+(os.path.join(self.template_path)+'ReportEmail.txt')
            self.sch_daily_template_path = r''+(os.path.join(self.template_path)+'SchedulerWinDaily.xml')
            self.sch_week_template_path = r''+(os.path.join(self.template_path)+'SchedulerWinWeek.xml')
            self.sch_month_template_path = r''+(os.path.join(self.template_path)+'SchedulerWinMonth.xml')
            self.config_file_path = self.getBasePath()+'conf.xml'
            self.avpreserve_img = os.path.join(sys._MEIPASS, 'assets' + (str(os.sep)) +'avpreserve.png')

        else:
            self.lib_agent_path = str(self.user_home_path)+str(os.sep)+"Library"+str(os.sep)+"LaunchAgents"+str(os.sep)
            self.agent_path = str(self.user_home_path)+str(os.sep)+"Library"
            path_info = str(os.getcwd()).replace(str(os.sep)+'Contents'+str(os.sep)+'Resources', '')
            path_info = str(path_info).replace('Fixity.app'+str(os.sep), '')
            path_info = str(path_info).replace('Fixity.app', '')
            path_info = str(path_info).replace('Main.app', '')

            self.base_path = path_info

            self.fixity_launch_path = str(os.getcwd()).replace(str(os.sep)+'Contents'+str(os.sep)+'Resources','') +str(os.sep)+"Contents"+str(os.sep)+"MacOS"+str(os.sep)+"Fixity"
            self.reports_path = r''+(os.path.join(self.base_path, 'reports'+str(os.sep)))
            self.schedules_path = r''+(os.path.join(os.getcwd(), 'schedules'+str(os.sep)))
            self.config_file_path = r''+(os.path.join(os.getcwd(), 'conf.xml'))
            self.history_path = r''+(os.path.join(self.base_path, 'history'+str(os.sep)))
            self.bin_path = r''+(os.path.join(self.base_path, 'bin'+str(os.sep)))
            self.assets_path = r''+(os.path.join(os.getcwd(), 'assets'+str(os.sep)))
            self.lock_file_path = r''+(os.path.join(os.getcwd(), 'dblocker.log'))

            self.log_file_path = r''+(os.path.join(os.getcwd(), 'debug.log'))

            self.database_file_path = r''+(os.path.join(os.getcwd(),'Fixity.db'))

            self.template_path = r''+(os.path.join(self.assets_path,'template')+str(os.sep))
            self.report_template_path = r''+(os.path.join(self.template_path)+'Report.txt')
            self.history_template_path = r''+(os.path.join(self.template_path)+'History.txt')

            self.report_email_template_path = r''+(os.path.join(self.template_path)+'ReportEmail.txt')
            self.sch_daily_template_path_mac = r''+(os.path.join(self.template_path)+'SchedulerMacDaily.xml')
            self.sch_week_template_path_mac = r''+(os.path.join(self.template_path)+'SchedulerMacWeek.xml')
            self.sch_month_template_path_mac = r''+(os.path.join(self.template_path)+'SchedulerMacMonth.xml')

            self.avpreserve_img = r''+(os.path.join(self.assets_path) + 'avpreserve.png')

        self.unit_test_folder = self.base_path + 'test'+os.sep
        self.unit_test_folder_special = self.base_path + '¿ÀÁÂÃ ÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþ ÿ' + os.sep
        self.check_sum_methods = ['sha256', 'md5']
        self.logo_sign_small = 'logo_sign_small.png'
        self.number_of_path_directories = 7
        self.number_of_path_email = 7
        self.email_configuration = {}
        self.week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.WeekInformation = {"Sunday":0, "Monday":1, "Tuesday":2, "Wednesday":3, "Thursday":4, "Friday":5, "Saturday":6 }
        self.time_format = "HH:mm"
        self.Months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.is_debugging_on = False

    def getSch_daily_template_path(self): return self.sch_daily_template_path

    def getSch_week_template_path(self): return self.sch_week_template_path

    def getSch_month_template_path(self): return self.sch_month_template_path

    def getSch_daily_template_path_mac(self): return self.sch_daily_template_path_mac

    def getSch_week_template_path_mac(self): return self.sch_week_template_path_mac

    def getUnit_test_folder(self): return self.unit_test_folder

    def getUnit_test_folder_special(self): return self.unit_test_folder_special

    def getSch_month_template_path_mac(self): return self.sch_month_template_path_mac

    def getHistoryTemplatePath(self):return self.history_template_path

    def getReportTemplatePath(self):return self.report_template_path

    def getReportEmailTemplatePath(self):return self.report_email_template_path

    def getTemplatePath(self):return self.template_path

    def getLockFilePath(self):return self.lock_file_path

    def getCheck_sum_methods(self):return self.check_sum_methods

    def getMonths(self): return self.Months

    def getWeekInformation(self): return self.WeekInformation

    def getImagesPath(self):return str(self.assets_path)

    def getAvpreserve_img(self):return self.avpreserve_img

    def getBasePath(self):return str(self.base_path)

    def getIs_debugging_on(self):return self.is_debugging_on

    def setIs_debugging_on(self, is_debugging_on):self.is_debugging_on = is_debugging_on

    def getApplicationVersion(self):return str(self.application_version)
    def getConfig_file_path(self):
        return self.config_file_path
    def EncodeInfo(self, string_to_be_encoded):
        string_to_be_encoded = str(string_to_be_encoded).strip()
        return base64.b16encode(base64.b16encode(string_to_be_encoded))

    #def getLogoSignSmall(self):

    def getLogoSignSmall(self):
        if self.getOsType() == 'Windows':
            return os.path.join(sys._MEIPASS, 'assets' + (str(os.sep)) + str(self.logo_sign_small))
        else:
            return str(self.getBasePath()) + str(os.sep) +  'assets' + (str(os.sep)) + str(self.logo_sign_small)

    def getOsType(self):return str(self.OsType)

    def getApplicationName(self): return str(self.application_name)

    def getNumberOfPathDirectories(self):return int(self.number_of_path_directories)

    def getNumberOfEmailField(self):return int(self.number_of_path_email)

    def getWeekDays(self): return self.week_days

    def getTimeFormat(self): return self.time_format

    def getUserHomePath(self): return str(os.path.expanduser('~'))

    def getDebugFilePath(self):return str(self.log_file_path)

    def getDatabaseFilePath(self):return str(self.database_file_path)

    def getReportsPath(self):return str(self.reports_path)

    def getSchedulesPath(self):return str(self.schedules_path)

    def getHistoryPath(self): return str(self.history_path)

    def getBinPath(self): return str(self.bin_path)

    def getAgentPath(self): return self.agent_path

    def getLibAgentPath(self): return self.lib_agent_path

    def getFixityLaunchPath(self): return self.fixity_launch_path

    def getEmailConfiguration(self): return self.email_configuration

    def fetchEmailConfiguration(self):
        emailConfiguration = self.Fixity.Database.select(self.Fixity.Database._tableConfiguration)
        if emailConfiguration is not None and emailConfiguration is not False:
            if len(emailConfiguration) > 0:
                self.setEmailConfiguration(emailConfiguration[0])
            else:
                return {}

    def setEmailConfiguration(self, email_configuration): self.email_configuration = email_configuration

    def saveEmailConfiguration(self, information):

        is_email_config_insert = False
        config_exists = self.Fixity.Database.select(self.Fixity.Database._tableConfiguration, 'id')

        if config_exists is not None and config_exists is not False:
            if len(config_exists) <=0:
                self.Fixity.Database.insert(self.Fixity.Database._tableConfiguration, information )
                self.setEmailConfiguration(information)
                is_email_config_insert = True
            else:
                is_email_config_insert = False

            if is_email_config_insert is False:
                self.Fixity.Database.update(self.Fixity.Database._tableConfiguration, information, 'id = "' + str(config_exists[0]['id']) + '"')
                self.setEmailConfiguration(information)

    def LogHistory(self):
        """ generated source for method LogHistory """
        #  TODO

    def Report(self):
        """ generated source for method Report """
        #  TODO

    def setReportsPath(self, parameter):
        return ""

    def setSchedulesPath(self):
        """ generated source for method setHistoryPath """
        #  TODO implement me
        return ""

    def setHistoryPath(self):
        """ generated source for method setHistoryPath """
        #  TODO implement me
        return ""

    def setBinPath(self):
        """ generated source for method setBinPath """
        #  TODO implement me
        return ""

    def setImagesPath(self):
        """ generated source for method setImagesPath """
        #  TODO implement me
        return ""

    def setAppName(self):
        """ generated source for method setAppName """
        #  TODO implement me
        return ""

    def setVersion(self):
        """ generated source for method setVersion """
        #  TODO implement me
        return ""

    def getCurrentTime(self):
        current_date = str(datetime.datetime.now()).split('.')
        return current_date[0]

    #Gets Detail information of Windows
    #@return: tuple Windows Information

    def getWindowsInformation(self):
        WindowsInformation = {}
        try:
            major,  minor,  build,  platformType,  servicePack = sys.getwindowsversion()
            WindowsInformation['major'] = major
            WindowsInformation['minor'] = minor
            WindowsInformation['build'] = build

            WindowsInformation['platformType'] = platformType
            WindowsInformation['servicePack'] = servicePack
            windowDetailedName = platform.platform()
            WindowsInformation['platform'] = windowDetailedName
            windowDetailedName = str(windowDetailedName).split('-')

            if windowDetailedName[0] is not  None and (str(windowDetailedName[0]) == 'Windows' or str(windowDetailedName[0]) == 'windows'):
                WindowsInformation['isWindows'] =True
            else:
                WindowsInformation['isWindows'] =False

            if windowDetailedName[1] is not None and (str(windowDetailedName[1]) != ''):
                WindowsInformation['WindowsType'] =str(windowDetailedName[1])
            else:
                WindowsInformation['WindowsType'] =None

            WindowsInformation['ProcessorInfo'] = platform.processor()

            try:
                os.environ["PROGRAMFILES(X86)"]
                bits = 64
            except:
                bits = 32
                pass

            WindowsInformation['bitType'] = "Win{0}".format(bits)
        except:

            pass
        return WindowsInformation

    #CleanStringForBreaks
    #@param StringToBeCleaned: String To Be Cleaned
    #
    #@return: CleanString

    def CleanStringForBreaks(self,StringToBeCleaned):
        CleanString = StringToBeCleaned.strip()
        try:
            CleanString = CleanString.replace('\r\n', '')
            CleanString = CleanString.replace('\n', '')
            CleanString = CleanString.replace('\r', '')
        except:
            pass

        return CleanString