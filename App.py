# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''

from Config import Configuration,  Validation, Setup
from GUI import GUILibraries, ProjectGUI
from Core import Debugger, Database, CustomException, SharedApp, ProjectCore, ProjectRepository
from Queue import Queue

class App(object):
    _instance = None
    def __init__(self):
        self.setUp()

    def selfDestruct(self):
        del self

    @staticmethod
    def getInstance():
        if not isinstance(App._instance, App):
            App._instance = object.__new__(App)
            SharedApp.SharedApp.App = App._instance
            App._instance.setUp()
        return App._instance

    def setUp(self):
        self.ExceptionHandler = CustomException.CustomException.getInstance()
        self.Configuration = Configuration()
        self.Validation = Validation
        self.Setup = Setup.Setup()
        self.Setup.setupApp()
        self.logger = Debugger.Debugger.getInstance()
        self.Database = Database.Database.getInstance()
        self.Database.connect()
        self.ProjectGUI = ProjectGUI
        self.Setup.createTables()
        self.ProjectRepo = ProjectRepository.ProjectRepository()

        email_configuration = self.Database.getConfiguration()

        try:
            self.Configuration.setEmailConfiguration(email_configuration[0])
        except:
            self.Configuration.setEmailConfiguration(email_configuration)
            pass

        self.ProjectsList = {}
        self.queue = Queue()

        self.loadAllProjects()


    def loadAllProjects(self):
        all_projects = self.ProjectRepo.getAll()

        if all_projects is not None and all_projects is not False:
            if len(all_projects) > 0:
                for single_project in all_projects:
                    project_logic = ProjectCore.ProjectCore()
                    project_logic.setProjectInfo(all_projects[single_project])
                    self.ProjectsList[all_projects[single_project]['title']] = project_logic

    def getSingleThreadToQueue(self, thread_id):
        return self.queue.get(thread_id)

    def addSingleThreadToQueue(self, thread_id, thread_object):
        return self.queue.put(thread_object)

    def getProjectList(self):
        information = []
        if self.ProjectsList is not None and self.ProjectsList is not False:
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