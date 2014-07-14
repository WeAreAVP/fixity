# -*- coding: UTF-8 -*-
'''
Created on JUNE 30, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''

# built-in libraries
import unittest
import os
import sys

# Custom libraries
from AllFixture.ProjectFixtures import ProjectFixtures
from TestCases.ProjectTestCase import ProjectTestCase
from TestCases.EmailTestCase import EmailTestCase
from TestCases.AlgorithmTestCase import AlgorithmTestCase
from TestCases.RequiredsCreationTestCase import RequiredsCreationTestCase

base_path = os.getcwd()
base_path = base_path.replace(r'\test', '')
sys.path.append(base_path+os.sep)

from AllFixture.Fixtures import Fixtures
import Main
import unittest

class TestSuite(unittest.TestCase):

    def setUp(self):
        print('Start Up')
        self.Fixtures = Fixtures()
        self.ProjectFixtures = ProjectFixtures()

        self.algorithm_test_case = AlgorithmTestCase()
        self.project_test_case = ProjectTestCase()
        self.email_test_case = EmailTestCase()
        self.requireds_creation_test_case = RequiredsCreationTestCase()
        self.App = Main.Main()
        self.App.Fixity.loadAllProjects()
        pass

    # Running Algorithm for Verification Test Cases
    def testARunAlgorithmTestCases(self):

        print('==================================================================')
        print(' Running Algorithm for Verification Test Cases ')
        print('==================================================================')

        # Confirmed  FileExists::YES   ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::NO
        response_test_confirm_file = self.algorithm_test_case.test_confirm_file()
        self.assertEqual(response_test_confirm_file[0], response_test_confirm_file[1], response_test_confirm_file[2])

        #New  FileExists::YES         ||SameHashOfFile::NO     ||SameFilePath::NO     ||SameI-Node::NO
        response_test_new_file = self.algorithm_test_case.test_new_file()
        self.assertEqual(response_test_new_file[0], response_test_new_file[1], response_test_new_file[2])

        # Changed   FileExists::YES    ||SameHashOfFile::NO     ||SameFilePath::YES    ||SameI-Node::YES
        response_test_change_file = self.algorithm_test_case.test_change_file()
        self.assertEqual(response_test_change_file[0], response_test_change_file[1], response_test_change_file[2])

        # Changed  FileExists::YES     ||SameHashOfFile::NO     ||SameFilePath::NO     ||SameI-Node::YES
        response_test_change_file_hp = self.algorithm_test_case.test_change_file_changed_hash_and_path()
        self.assertEqual(response_test_change_file_hp[0], response_test_change_file_hp[1], response_test_change_file_hp[2])

        #Confirmed   FileExists::YES  ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::YES

        response_test_confirm_file_all = self.algorithm_test_case.test_confirm_if_inode_changed_of_file()
        self.assertEqual(response_test_confirm_file_all[0], response_test_confirm_file_all[1], response_test_confirm_file_all[2])

        # Changed  FileExists::YES     ||SameHashOfFile::NO     ||SameFilePath::YES    ||SameI-Node::NO
        response_test_confirm_file_ih = self.algorithm_test_case.test_change_inode_and_hash_file()
        self.assertEqual(response_test_confirm_file_ih[0], response_test_confirm_file_ih[1], response_test_confirm_file_ih[2])

        # Moved   FileExists::YES      ||SameHashOfFile::YES    ||SameFilePath::NO     ||SameI-Node::YES
        response_test_moved_file = self.algorithm_test_case.test_moved_file()
        self.assertEqual(response_test_moved_file[0], response_test_moved_file[1], response_test_moved_file[2])

        #Deleted   FileExists::NO     ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::YES
        response_test_confirm_file_delete = self.algorithm_test_case.test_delete_file()
        self.assertEqual(response_test_confirm_file_delete[0], response_test_confirm_file_delete[1], response_test_confirm_file_delete[2])

        # ================================== Special Character Testing ================================
        # Confirmed  FileExists::YES   ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::NO
        response_test_confirm_file = self.algorithm_test_case.test_confirm_file_is_special_chars()
        self.assertEqual(response_test_confirm_file[0], response_test_confirm_file[1], response_test_confirm_file[2])

        #New  FileExists::YES         ||SameHashOfFile::NO     ||SameFilePath::NO     ||SameI-Node::NO
        response_test_new_file = self.algorithm_test_case.test_new_file_is_special_chars()
        self.assertEqual(response_test_new_file[0], response_test_new_file[1], response_test_new_file[2])

        # Changed   FileExists::YES    ||SameHashOfFile::NO     ||SameFilePath::YES    ||SameI-Node::YES
        response_test_change_file = self.algorithm_test_case.test_change_file_is_special_chars()
        self.assertEqual(response_test_change_file[0], response_test_change_file[1], response_test_change_file[2])

        #Changed  FileExists::YES     ||SameHashOfFile::NO     ||SameFilePath::NO     ||SameI-Node::YES
        response_test_change_file_hp = self.algorithm_test_case.test_change_file_changed_hash_and_path_is_special_chars()
        self.assertEqual(response_test_change_file_hp[0], response_test_change_file_hp[1], response_test_change_file_hp[2])

        # Confirmed   FileExists::YES  ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::YES
        response_test_confirm_file_all = self.algorithm_test_case.test_confirm_if_inode_changed_of_file_is_special_chars()
        self.assertEqual(response_test_confirm_file_all[0], response_test_confirm_file_all[1], response_test_confirm_file_all[2])

        # Changed  FileExists::YES     ||SameHashOfFile::NO     ||SameFilePath::YES    ||SameI-Node::NO
        response_test_confirm_file_ih = self.algorithm_test_case.test_change_inode_and_hash_file_is_special_chars()
        self.assertEqual(response_test_confirm_file_ih[0], response_test_confirm_file_ih[1], response_test_confirm_file_ih[2])
        #
        # Moved   FileExists::YES      ||SameHashOfFile::YES    ||SameFilePath::NO     ||SameI-Node::YES
        response_test_moved_file = self.algorithm_test_case.test_moved_file_is_special_chars()
        self.assertEqual(response_test_moved_file[0], response_test_moved_file[1], response_test_moved_file[2])
        #
        # Deleted   FileExists::NO     ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::YES
        response_test_confirm_file_delete = self.algorithm_test_case.test_delete_file_is_special_chars()
        self.assertEqual(response_test_confirm_file_delete[0], response_test_confirm_file_delete[1], response_test_confirm_file_delete[2])

        # Deleted   FileExists::NO     ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::YES
        response_test_moved_file_to_new_Directory = self.algorithm_test_case.test_moved_file_to_new_directory()
        self.assertEqual(response_test_moved_file_to_new_Directory[0], response_test_moved_file_to_new_Directory[1], response_test_moved_file_to_new_Directory[2])

        # Deleted   FileExists::YES     ||SameHashOfFile::YES    ||SameFilePath::NO    ||SameI-Node::YES
        response_test_moved_file_to_new_Directory = self.algorithm_test_case.test_moved_file_to_new_Directory_change_hash()
        self.assertEqual(response_test_moved_file_to_new_Directory[0], response_test_moved_file_to_new_Directory[1], response_test_moved_file_to_new_Directory[2])

        # Deleted   FileExists::YES     ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::NO
        response_test_moved_new_Directory_change_name = self.algorithm_test_case.test_moved_file_to_new_Directory_change_name_as_old()
        self.assertEqual(response_test_moved_new_Directory_change_name[0], response_test_moved_new_Directory_change_name[1], response_test_moved_new_Directory_change_name[2])
        #
        # Deleted   FileExists::NO     ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::YES
        response_test_moved_new_Directory_change_name_and_hash = self.algorithm_test_case.test_moved_to_new_directory_change_name_as_old_and_content()
        self.assertEqual(response_test_moved_new_Directory_change_name_and_hash[0], response_test_moved_new_Directory_change_name_and_hash[1], response_test_moved_new_Directory_change_name_and_hash[2])

        # Deleted   FileExists::NO     ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::YES
        response_test_change_base_path = self.algorithm_test_case.test_change_base_path()
        self.assertEqual(response_test_change_base_path[0], response_test_change_base_path[1], response_test_change_base_path[2])

        # Deleted   FileExists::NO     ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::YES
        response_test_change_base_path = self.algorithm_test_case.test_intersection_of_dir()
        self.assertEqual(response_test_change_base_path[0], response_test_change_base_path[1], response_test_change_base_path[2])


    # Running Projects Operation Test Cases
    def testBProjectTestCases(self):

        print('==================================================================')
        print(' Running Projects Operation Test Cases')
        print('==================================================================')

        # Project Run Unit test
        response_test_run_project = self.project_test_case.run_project(self.Fixtures.project_name)
        self.assertEqual(response_test_run_project[0], response_test_run_project[1], response_test_run_project[2])

        # Project Run Unit test
        response_test_delete_project = self.project_test_case.delete_project(self.Fixtures.project_name)
        self.assertEqual(response_test_delete_project[0], response_test_delete_project[1], response_test_delete_project[2])

        # Change Project Name Unit test
        response_test_change_project_name = self.project_test_case.change_project_name(self.Fixtures.project_name, 'testing')
        self.assertEqual(response_test_change_project_name[0], response_test_change_project_name[1], response_test_change_project_name[2])

        # Save Project Unit test
        response_test_save_project = self.project_test_case.save_project(self.Fixtures.project_name)
        self.assertEqual(response_test_save_project[0], response_test_save_project[1], response_test_save_project[2])

        # Change Algorithm Unit test
        response_test_change_algorithm = self.project_test_case.change_algorithm(self.Fixtures.project_name)
        self.assertEqual(response_test_change_algorithm[0], response_test_change_algorithm[1], response_test_change_algorithm[2])

        # Filter scanned files Unit test
        response_test_filters_files = self.project_test_case.filters_files(self.Fixtures.project_name)
        self.assertEqual(response_test_filters_files[0], response_test_filters_files[1], response_test_filters_files[2])

        # Import Project Unit test
        response_test_import_project = self.project_test_case.import_project('Testing')
        self.assertEqual(response_test_import_project[0], response_test_import_project[1], response_test_import_project[2])

    # Running Email Notification Test Cases
    def testCEmailNotification(self):

        print('==================================================================')
        print(' Running Email Notification Test Cases')
        print('==================================================================')

        # Testing Email Unit Test
        response_of_email = self.email_test_case.test_testing_email()
        self.assertEqual(response_of_email[0], response_of_email[1], response_of_email[2])

        # Attachment Email Unit Test
        response_of_email_attachment = self.email_test_case.test_attachment_email()
        self.assertEqual(response_of_email_attachment[0], response_of_email_attachment[1], response_of_email_attachment[2])

        # Error Email Unit Test
        response_of_email_error = self.email_test_case.test_Error_email()
        self.assertEqual(response_of_email_error[0], response_of_email_error[1], response_of_email_error[2])
        pass


    def testDRequiredFilesAndDirsCreation(self):

        print('==================================================================')
        print(' Running Required Files And Dirs Creation Test Cases')
        print('==================================================================')

        # Is Config File Exists
        response_of_is_config_file_exists = self.requireds_creation_test_case.is_config_file_exists()

        self.assertEqual(response_of_is_config_file_exists[0], response_of_is_config_file_exists[1], response_of_is_config_file_exists[2])

        # Is Database File Exists
        response_of_is_database_file_exists = self.requireds_creation_test_case.is_database_file_exists()
        self.assertEqual(response_of_is_database_file_exists[0], response_of_is_database_file_exists[1], response_of_is_database_file_exists[2])

        # Is Debug File Exists
        response_of_is_debug_files_exists = self.requireds_creation_test_case.is_debug_files_exists()
        self.assertEqual(response_of_is_debug_files_exists[0], response_of_is_debug_files_exists[1], response_of_is_debug_files_exists[2])

        # Is History Directory Exists
        response_of_is_history_dir_exists = self.requireds_creation_test_case.is_history_dir_exists()
        self.assertEqual(response_of_is_history_dir_exists[0], response_of_is_history_dir_exists[1], response_of_is_history_dir_exists[2])

        # Is Reports Directory Exists
        response_of_is_report_dir_exists = self.requireds_creation_test_case.is_report_dir_exists()
        self.assertEqual(response_of_is_report_dir_exists[0], response_of_is_report_dir_exists[1], response_of_is_report_dir_exists[2])

        # Is Schedulers Directory Exists
        response_of_is_schedules_dir_exists = self.requireds_creation_test_case.is_schedules_dir_exists()
        self.assertEqual(response_of_is_schedules_dir_exists[0], response_of_is_schedules_dir_exists[1], response_of_is_schedules_dir_exists[2])


    def tearDown(self):
        print('Tear Down!')
        self.Fixtures.delete_testing_data()
        print('')
        pass

if __name__ == '__main__':
    unittest.main()

