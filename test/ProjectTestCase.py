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
from EmailFixtures import EmailFixtures


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


    # Delete Project
    #
    # @param string:project_name project name to be Deleted

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


    # Change Project Name
    #
    # @param string:project_name project name to be Changed
    # @param string:new_project project name to be changed with

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


    # Save Project
    #
    # @param string:project_name project name to be Saved

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


    # Change Algorithm
    #
    # @param string:project_name project name to be Changed Algorithm

    def change_algorithm(self, project_name):
        print('Test Change Project Algorithm .........!')

        algo_value_selected = 'md5'
        flag = True
        self.project_fixtures.load_verification_algorithm_data()
        self.project_fixtures.create_new_project(project_name)

        project_core = self.App.Fixity.ProjectRepo.getSingleProject(project_name)


        result_of_all_file_confirmed = project_core.Run(True)




        if bool(result_of_all_file_confirmed['file_changed_found']):
            email_fixtures = EmailFixtures()
            self.App.Fixity.Configuration.setEmailConfiguration(email_fixtures.EmailInformation())
            flag = False

        update_project_algo = {}
        update_project_algo['selectedAlgo'] = algo_value_selected
        self.App.Fixity.Database.update(self.App.Fixity.Database._tableProject, update_project_algo, "id='" + str(project_core.getID()) + "'")
        project_core.setAlgorithm(algo_value_selected)
        result_of_all_file_confirmed_second = project_core.Run(True, False, True)

        if bool(result_of_all_file_confirmed_second['file_changed_found']):
            flag = False

        return [flag, False, "Failed Algo Change Unit Test."]




    # Filters Files
    #
    # @param string:selected_project project name to be filtered

    def filters_files(self, selected_project):
        print('Test Filters Project .........!')
        self.project_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(selected_project)

        project_core = self.App.Fixity.ProjectRepo.getSingleProject(selected_project)
        project_core.applyFilter('', self.project_fixtures.is_ignore_hidden_files)
        project_core.Run(False, False, False, 'test')

        project_core.applyFilter(self.project_fixtures.filters, self.project_fixtures.is_ignore_hidden_files)
        result_of_run_after_filter = project_core.Run(False, False, False, 'test')

        self.project_fixtures.load_verification_algorithm_data()

        confirmed = result_of_run_after_filter['confirmed']
        missing_file = result_of_run_after_filter['missing_file']
        created = result_of_run_after_filter['created']
        moved = result_of_run_after_filter['moved']
        corrupted_or_changed = result_of_run_after_filter['corrupted_or_changed']

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed}, {0: 3, 1: 1, 2: 0, 3: 0, 4: 0}, 'Failed Filters Project files']

    # Import Project
    #
    # @param string:project_name project name to be import Project

    def import_project(self, project_name):
        print('Test Import Project .........!')
        self.project_fixtures.load_history_file()
        flag = True
        project_core = ProjectCore.ProjectCore()
        response = project_core.ImportProject(self.project_fixtures.test_history_file, project_name, True, False)
        project_core = self.App.Fixity.ProjectRepo.getSingleProject(project_name)

        if not response:
            return False

        try:
            project_core.getID()
            project_core.getTitle()
            flag = True
        except:
            flag = False
            pass

        return [flag, True, "Failed Import Project Unit Test."]
