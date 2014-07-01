# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''


# built-in libraries
import unittest
import os
import sys

# Custom libraries
base_path = os.getcwd()
base_path = base_path.replace(r'\test', '')
sys.path.append(base_path+os.sep)
import Main
from ProjectFixtures import ProjectFixtures
from Core import ProjectCore

class ProjectTestCase(object):


    def __init__(self):
        self.App = Main.Main()
        self.project_fixtures = ProjectFixtures()

        pass

    # Create New Project
    #
    # @param string:project_name project name to be ran

    def run_project(self, project_name):
        print('Test Run Project.........!')
        self.project_fixtures.load_verification_algorithm_data()
        project_information = self.App.LaunchCLI(project_name, 'test')
        self.project_fixtures.unload_verification_algorithm_data()
        return [4, project_information['created'], 'Failed Run Project Unit Test....!']

    def delete_project(self, project_name):
        print('Test Delete Project.........!')
        project_core = self.App.Fixity.ProjectRepo.getSingleProject(project_name)
        deleted_project_id = project_core.getID()
        deleted_project_Title = project_core.getTitle()

        project_core.Delete()
        project_core_deleted = self.App.Fixity.ProjectRepo.getSingleProject(deleted_project_Title)
        flag = True
        try:
            project_core_deleted.getID()
            project_core_deleted.getTitle()
            flag = False
        except:
            pass

        try:
            project_core_deleted.getID()
            project_core_deleted.getTitle()
            flag = False
        except:
            pass

        result_project = self.App.Fixity.Database.getProjectInfo(deleted_project_Title)
        result_project_detail = self.App.Fixity.Database.getVersionDetailsLast(deleted_project_id)
        if len(result_project) > 0:
            flag = False

        if len(result_project_detail) > 0:
            flag = False

        return [flag, True, "Failed Save Project Unit Test"]


    def change_project_name(self, project_name, new_project):
        flag = True
        print('Test Change Project Name .........!')
        self.project_fixtures.create_new_project(project_name)

        project_core = self.App.Fixity.ProjectRepo.getSingleProject(project_name)
        project_core.changeProjectName(project_name, new_project)
        project_core_new = self.App.Fixity.ProjectRepo.getSingleProject(new_project)

        try:
            project_core_new.getID()
            project_core_new.getTitle()
        except:
            flag = False

        return [flag, True, "Failed Save Project Unit Test"]

    def save_project(self, project_name):
        print('Test Save Project .........!')
        flag = False

        try:
            self.project_fixtures.create_new_project(project_name)
            project_core = self.App.Fixity.ProjectRepo.getSingleProject(project_name)
            project_core.Save()
            flag = True
        except:
            flag = False

        return [flag, True, "Failed Save Project Unit Test."]