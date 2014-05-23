'''
Created on May 14, 2014

@author: Furqan Wasi

'''
import os, logging, datetime
from Core import SharedApp
import xml.etree.cElementTree as XmlHanlder

class Debugger(object):
    _instance = None
    def __init__(self):
        Debugger._instance.setUp()

    @staticmethod
    def getInstance():
        if not isinstance(Debugger._instance, Debugger):
            Debugger._instance = object.__new__(Debugger)
            Debugger._instance.setUp()
        return Debugger._instance

    def selfDestruct(self):
        del self

    def setUp(self):
        self.Fixity = SharedApp.SharedApp.App

        self.debug_file_path = self.Fixity.Configuration.getDebugFilePath()

        self.config_file_path = self.Fixity.Configuration.getBasePath()+'conf.xml'
        self.loger = logging

        # Create debug file
        try:
            self.loger.basicConfig(filename=self.debug_file_path, level=logging.DEBUG)
        except:

                print(self.Fixity.ExceptionHandler.getExceptionDetails())
                print(self.Fixity.ExceptionHandler.getTraceBack())
                pass

        if self.get() == 'true':
            self.is_debugger_on = True
        else:
            self.is_debugger_on = False

    #Function to Log Errors
    #@param msg Message to log
    #@param more_information More information For Logging

    def logError(self,msg,more_information = None):
        try:
            if(self.is_debugger_on):
                self.addTimeStamp()
                self.loger.debug('')
                self.loger.debug(msg)
                if(len(more_information) > 0):

                    for key in more_information:

                        print(key)
                        print(more_information[key])

                        self.loger.debug(str(key) + '::' + str(more_information[key])+"\n")

        except:
                print(Exception.message)
                pass


    #Function to Log Information
    #@param msg Message to log
    #@param more_information More information For Logging

    def logInfo(self,msg ,more_information = None):
        try:
            if(self.is_debugger_on):
                self.addTimeStamp()
                self.loger.info(msg)
                if(more_information):
                    for key in more_information:
                        self.loger.info(key + '::' + more_information[key]+"\n")
        except:
            print(self.Fixity.ExceptionHandler.getExceptionDetails())
            print(self.Fixity.ExceptionHandler.getTraceBack())
            self.is_debugger_on = False

    #Function to Log Warning
    #@param msg Message to log
    #@param more_information More information For Logging

    def logWarning(self,msg,more_information = None):
        try:
            if(self.is_debugger_on):
                self.addTimeStamp()
                self.loger.warning(msg)
                if(more_information):
                    for key in more_information:
                        self.loger.warning(key + '::' + more_information[key]+"\n")

        except:
            print(self.Fixity.ExceptionHandler.getExceptionDetails())
            print(self.Fixity.ExceptionHandler.getTraceBack())
            self.is_debugger_on = False

    def set(self, status):
        os.remove(self.config_file_path)
        fixity = XmlHanlder.Element("Fixity")

        configuration = XmlHanlder.SubElement(fixity, "Configuration")
        debugging = XmlHanlder.SubElement(configuration, "debugging")

        debugging.set("status", status)

        xml_obj = XmlHanlder.ElementTree(fixity)
        if status == 'true':
            self.is_debugger_on = True
        else:
            self.is_debugger_on = False
        return xml_obj.write(self.config_file_path)

    def get(self):
        tree = XmlHanlder.parse(self.config_file_path)
        root = tree.getroot()
        for child in root:
            for child1 in child:
                return child1.attrib['status']

    def getCurrentTime(self):
        return str(datetime.datetime.now()).rpartition('.')[0]

    def addTimeStamp(self):
        self.loger.warning('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        self.loger.warning('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        self.loger.warning(str(self.getCurrentTime()))
        self.loger.warning('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        self.loger.warning('')

    def LogException(self, message=''):


        ExceptionDetail = {}
        try:
            ExceptionDetail = self.Fixity.ExceptionHandler.getExceptionDetails()
        except:
            pass

        print('========================== Exception Message ======================')
        print(ExceptionDetail)
        print('========================== Exception Message ======================')

        try:
            ExceptionDetail['trace_back'] = self.Fixity.ExceptionHandler.getTraceBack()
        except:
            pass

        self.logError(message, ExceptionDetail)


