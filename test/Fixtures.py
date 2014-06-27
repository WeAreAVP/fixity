# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''


# built-in libraries
import os
import random
import shutil

# Custom libraries
import Main

class Fixtures(object):


    def __init__(self):
        self.App = Main.Main()
        self.unit_test_folder = self.App.Fixity.Configuration.getUnit_test_folder()
        pass

    # Create New Project
    #
    # @param string:project_name project name to be created
    #
    # @param int: created_directory_id

    def create_new_project(self, project_name):

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
        project_information['emailOnlyUponWarning'] = '1'

        project_information['emailAddress'] = ''
        project_information['extraConf'] = ''
        project_information['lastRan'] = ''

        project_information['updatedAt'] = self.App.Fixity.Configuration.getCurrentTime()
        project_id = self.App.Fixity.Database.insert(self.App.Fixity.Database._tableProject, project_information)

        dir_information = {}
        dirs_path = self.unit_test_folder
        for n in range(self.App.Fixity.Configuration.number_of_path_directories):

            dir_information['path'] = dirs_path
            dir_information['pathID'] = 'Fixity-1'
            dir_information['projectID'] = project_id['id']
            dir_information['versionID'] = '1'
            dir_information['updatedAt'] = self.App.Fixity.Configuration.getCurrentTime()
            dir_information['createdAt'] = self.App.Fixity.Configuration.getCurrentTime()

            dir_new_id = self.App.Fixity.Database.insert(self.App.Fixity.Database._tableProjectPath, dir_information)
            dirs_path = ''

        return dir_new_id

    # Delete Testing Data
    def delete_testing_data(self):

        if os.path.exists(self.unit_test_folder):
            shutil.rmtree(self.unit_test_folder)

        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableProject, '1 = 1')
        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableVersionDetail, '1 = 1')
        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableProjectPath, '1 = 1')

        pass

    # Load Verification Algorithm Data
    def load_verification_algorithm_data(self):

        if os.path.exists(self.unit_test_folder):
            shutil.rmtree(self.unit_test_folder)
        os.makedirs(self.unit_test_folder)

        test_file_one = self.unit_test_folder + '1.docx'
        test_file_two = self.unit_test_folder + '2.docx'
        test_file_three = self.unit_test_folder + '3.docx'
        test_file_four = self.unit_test_folder + '4.docx'

        file_obj1 = open(test_file_one, 'w+')
        file_obj1.write('1 document' + str(random.randrange(1, 10000)))
        file_obj1.close()

        file_obj1 = open(test_file_two, 'w+')
        file_obj1.write('2 document' + str(random.randrange(1, 10000)))
        file_obj1.close()

        file_obj1 = open(test_file_three, 'w+')
        file_obj1.write('3 document' + str(random.randrange(1, 10000)))
        file_obj1.close()

        file_obj1 = open(test_file_four, 'w+')
        file_obj1.write('4 document' + str(random.randrange(1, 10000)))
        file_obj1.close()

    # Del File
    def del_file(self, path_to_be_deleted):
        os.remove(path_to_be_deleted)
        pass

    # Rename File
    def rename_file(self, path_to_be_renamed, new_name):
        os.rename(new_name, path_to_be_renamed)
        pass

    # New File
    def new_file(self, path_to_be_created):
        file_obj = open(path_to_be_created, 'w')
        file_obj.write('testing new file' + str(random.randrange(1, 10000)))
        file_obj.close()
        pass

    # Change File
    def change_file(self, path_to_be_changed):
        file_obj = open(path_to_be_changed, 'w')
        file_obj.write('testing new file '+str(random.randrange(1, 10000)))
        file_obj.close()
        pass
