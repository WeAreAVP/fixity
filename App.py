'''
Created on May 14, 2014

@author: Furqan
'''

from Config import Configuration,  Validation, Setup
from GUI import GUILibraries, ProjectGUI
from Core import Debugger, Database, CustomException, SharedApp, ProjectCore

class App(object):
    _instance = None

    @staticmethod
    def getInstance():
        if not isinstance(App._instance, App):
            App._instance = object.__new__(App)
            SharedApp.SharedApp.App = App._instance
            App._instance.setUp()
        return App._instance

    def setUp(self):
        self.ExceptionHandler = CustomException.CustomException()
        self.Configuration = Configuration()

        self.Validation = Validation
        self.Setup = Setup.Setup()
        self.Setup.setupApp()
        self.logger = Debugger.Debugger.getInstance()
        self.Database = Database.Database.getInstance()
        self.Database.connect()
        self.ProjectGUI = ProjectGUI
        self.Setup.createTables()
        email_configuration = self.Database.getConfiguration()

        try:
            self.Configuration.setEmailConfiguration(email_configuration[0])
        except:
            self.Configuration.setEmailConfiguration(email_configuration)
            pass

        self.ProjectsList = {}
        self.loadAllProjects()


    def loadAllProjects(self):
        all_projects = self.Database.getProjectInfo()
        if all_projects is not None:
            if len(all_projects) > 0:
                for single_project in all_projects:
                    project_logic = ProjectCore.ProjectCore()
                    project_logic.setProjectInfo(all_projects[single_project])
                    self.ProjectsList[all_projects[single_project]['title']] = project_logic


    def getProjectList(self):
        information = []
        if len(self.ProjectsList) > 0:
            for project in self.ProjectsList:
                information.append(str(self.ProjectsList[project].getTitle()))
        return information

    def getSingleProject(self, project_name):
        try:
            selected_project_object = self.ProjectsList[project_name]
            return selected_project_object
        except:
            return False

    def removeProject(self, project_name):
        self.ProjectsList.__delitem__(project_name)