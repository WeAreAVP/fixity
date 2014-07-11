# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''


# built-in libraries
import os

from Fixtures import Fixtures
# Custom libraries


import sys
base_path = os.getcwd()
base_path = base_path.replace(r'\test', '')
base_path = base_path.replace(r'\Fixture', '')
sys.path.append(base_path+os.sep)

import Main




class ProjectFixtures(Fixtures):

    def __init__(self):
        self.App = Main.Main()
        super(ProjectFixtures, self).__init__()
        self.unit_test_folder = self.App.Fixity.Configuration.getUnit_test_folder()
        self.filters = '.txt'
        self.is_ignore_hidden_files = True
        pass

    # Del File
    #
    # @param project_name:string  Project Name
    def create_new_project(self, project_name, is_special_chars = False):

        project_information = {}

        project_information['title'] = project_name
        project_information['ignoreHiddenFiles'] = ''
        project_information['selectedAlgo'] = 'sha256'
        project_information['filters'] = ''
        project_information['durationType'] = '2'
        project_information['runTime'] = ''
        project_information['runDayOrMonth'] = '0'
        project_information['runWhenOnBattery'] = '1'
        project_information['ifMissedRunUponRestart'] = '1'
        project_information['versionCurrentID'] = '1'
        project_information['emailOnlyUponWarning'] = '1'

        project_information['emailAddress'] = ''
        project_information['extraConf'] = ''
        project_information['lastRan'] = ''

        project_information['updatedAt'] = self.App.Fixity.Configuration.getCurrentTime()
        project_id = self.App.Fixity.Database.insert(self.App.Fixity.Database._tableProject, project_information)

        dir_information = {}
        if is_special_chars:
            dirs_path = self.unit_test_folder_special
        else:
            dirs_path = self.unit_test_folder

        for n in range(self.App.Fixity.Configuration.number_of_path_directories):

            dir_information['path'] = dirs_path
            dir_information['pathID'] = 'Fixity-'+str((n + 1))
            dir_information['projectID'] = project_id['id']
            dir_information['versionID'] = '1'
            dir_information['updatedAt'] = self.App.Fixity.Configuration.getCurrentTime()
            dir_information['createdAt'] = self.App.Fixity.Configuration.getCurrentTime()

            dir_new_id = self.App.Fixity.Database.insert(self.App.Fixity.Database._tableProjectPath, dir_information)
            dirs_path = ''

        self.App.Fixity.loadAllProjects()
        return dir_new_id
