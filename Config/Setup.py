'''
Created on May 14, 2014

@author: Furqan
'''
import os, traceback
from Core import SharedApp
import xml.etree.cElementTree as XmlHanlder

class Setup(object):

    def __init__(self):
        self.Fixity = SharedApp.SharedApp.App
        self.is_debugger_on = True
        self.debug_file_path = self.Fixity.Configuration.getDebugFilePath()

        self.config_file_path = self.Fixity.Configuration.getConfig_file_path()

    def setupApp(self):
        self.createDirsAndFiles()

    def createDirsAndFiles(self):
        # Create Config file
        if not os.path.isfile(self.config_file_path):
            try:
                status = 'false'
                fixity = XmlHanlder.Element("Fixity")

                configuration = XmlHanlder.SubElement(fixity, "Configuration")
                debugging = XmlHanlder.SubElement(configuration, "debugging")

                debugging.set("status", status)

                xml_obj = XmlHanlder.ElementTree(fixity)
                if status == 'true':
                    self.is_debugger_on = True
                else:
                    self.is_debugger_on = False
                xml_obj.write(self.config_file_path)


            except:
                traceback.print_stack()
                pass

        if self.Fixity.Configuration.getOsType() == 'linux':
            if(not os.path.isdir(self.Fixity.Configuration.getAgentPath())):
                os.makedirs(self.Fixity.Configuration.getAgentPath())
        print(self.Fixity.Configuration.getDatabaseFilePath())
        # create Database file
        if not os.path.isfile(self.Fixity.Configuration.getDatabaseFilePath()):
            try:
                DatabaseFile = open(str(self.Fixity.Configuration.getDatabaseFilePath()), 'w+')
                DatabaseFile.close()
            except:
                traceback.print_stack()
                pass

        print(self.Fixity.Configuration.getHistoryPath())
        # Create History directory
        if not os.path.isdir(self.Fixity.Configuration.getHistoryPath()):
            try:
                os.mkdir(self.Fixity.Configuration.getHistoryPath())
            except:
                traceback.print_stack()
                pass
        print(self.Fixity.Configuration.getSchedulesPath())
        # Create Schedules directory
        if not os.path.isdir(self.Fixity.Configuration.getSchedulesPath()):
            try:
                os.mkdir(self.Fixity.Configuration.getSchedulesPath())
            except:
                traceback.print_stack()
                pass
        print(self.Fixity.Configuration.getReportsPath())
        # Create Reports directory
        if not os.path.isdir(self.Fixity.Configuration.getReportsPath()):
            try:
                os.mkdir(self.Fixity.Configuration.getReportsPath())
            except:
                traceback.print_stack()
                pass

    def createTables(self):

        if not self.checkIfTableExistsInDatabase('configuration'):
            ''' Create Configuration Table'''
            try:

                self.Fixity.Database.sqlQuery('CREATE TABLE "configuration" ( id INTEGER NOT NULL,  smtp TEXT,  email TEXT,  pass TEXT,  port INTEGER,  protocol TEXT,  debugger SMALLINT,  "updatedAt" DATETIME,  "createdAt" DATETIME,  PRIMARY KEY (id) );')

            except:
                traceback.print_stack()
                pass

        if not self.checkIfTableExistsInDatabase('project'):
            ''' Create Project Table'''
            try:
                self.Fixity.Database.sqlQuery('CREATE TABLE "project" (id INTEGER PRIMARY KEY, versionCurrentID INTEGER, projectRanBefore SMALLINT DEFAULT 0, title VARCHAR(255), durationType INTEGER, runTime TEXT(10), lastDifPaths TEXT NULL DEFAULT  NULL,   runDayOrMonth VARCHAR(12),selectedAlgo VARCHAR(8),filters TEXT, runWhenOnBattery SMALLINT, ifMissedRunUponRestart SMALLINT, ignoreHiddenFiles NUMERIC,  emailOnlyUponWarning SMALLINT, emailAddress TEXT,extraConf TEXT, lastRan DATETIME, updatedAt DATETIME, createdAt DATETIME);')
            except:
                traceback.print_stack()
                pass

        if not self.checkIfTableExistsInDatabase('projectPath'):
            ''' Create ProjectPath Table'''
            try:
                self.Fixity.Database.sqlQuery('CREATE TABLE "projectPath" ( id INTEGER NOT NULL,  "projectID" INTEGER NOT NULL,  "versionID" INTEGER,  path TEXT NOT NULL, "pathID" VARCHAR(15) NOT NULL,  "updatedAt" DATETIME,"createdAt"DATETIME, PRIMARY KEY (id), FOREIGN KEY("projectID") REFERENCES project (id), FOREIGN KEY("versionID") REFERENCES versions (id));')
            except:
                traceback.print_stack()
                pass

        if not self.checkIfTableExistsInDatabase('versionDetail'):
            ''' Create VersionDetail Table'''
            try:
                self.Fixity.Database.sqlQuery('CREATE TABLE "versionDetail" (id INTEGER NOT NULL, "versionID" INTEGER NOT NULL, "projectID" INTEGER NOT NULL, "projectPathID" INTEGER NOT NULL, "hashes" TEXT NOT NULL,  "path" TEXT NOT NULL, inode TEXT NOT NULL, "updatedAt" DATETIME, "createdAt" DATETIME, PRIMARY KEY (id), FOREIGN KEY("versionID") REFERENCES versions (id), FOREIGN KEY("projectID") REFERENCES project (id), FOREIGN KEY("projectPathID") REFERENCES "projectPath" (id));')
            except:
                traceback.print_stack()
                pass


        if not self.checkIfTableExistsInDatabase('versions'):
            ''' Create Versions Table'''
            try:
                self.Fixity.Database.sqlQuery('CREATE TABLE "versions" (id INTEGER NOT NULL,  "versionID" INTEGER NOT NULL, "projectID" INTEGER NOT NULL, "versionType" VARCHAR(10) NOT NULL, name VARCHAR(255) NOT NULL, "updatedAt" DATETIME, "createdAt" DATETIME, PRIMARY KEY (id));')
            except:
                traceback.print_stack()
                pass

    def checkIfTableExistsInDatabase(self, tableName):
            return self.Fixity.Database.getOne("SELECT * FROM sqlite_master WHERE name ='" + tableName + "'");