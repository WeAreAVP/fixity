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

from AlgorithmTestCase import AlgorithmTestCase
from ProjectTestCase import ProjectTestCase
from EmailTestCase import EmailTestCase
import Main
from Fixtures import Fixtures
from ProjectFixtures import ProjectFixtures


class TestSuite(unittest.TestCase):

    def setUp(self):
        print('Start Up')
        self.Fixtures = Fixtures()
        self.ProjectFixtures = ProjectFixtures()

        self.algorithm_test_case = AlgorithmTestCase()
        self.project_test_case = ProjectTestCase()
        self.email_test_case = EmailTestCase()

        self.ProjectFixtures.create_new_project(self.Fixtures.project_name)
        self.App = Main.Main()
        self.App.Fixity.loadAllProjects()
        pass

    def testRunAlgorithmTestCases(self):
        print('==================================================================')
        print(' Running Alogorithm for Verification Test Cases ')
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

        # Confirmed   FileExists::YES  ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::YES
        response_test_confirm_file_all = self.algorithm_test_case.test_confirm_if_inode_changed_of_file()
        self.assertEqual(response_test_confirm_file_all[0], response_test_confirm_file_all[1], response_test_confirm_file_all[2])

        # Changed  FileExists::YES     ||SameHashOfFile::NO     ||SameFilePath::YES    ||SameI-Node::NO
        response_test_confirm_file_ih = self.algorithm_test_case.test_change_inode_and_hash_file()
        self.assertEqual(response_test_confirm_file_ih[0], response_test_confirm_file_ih[1], response_test_confirm_file_ih[2])

        # Moved   FileExists::YES      ||SameHashOfFile::YES    ||SameFilePath::NO     ||SameI-Node::YES
        response_test_moved_file = self.algorithm_test_case.test_moved_file()
        self.assertEqual(response_test_moved_file[0], response_test_moved_file[1], response_test_moved_file[2])

        # Deleted   FileExists::NO     ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::YES
        response_test_confirm_file_delete = self.algorithm_test_case.test_delete_file()
        self.assertEqual(response_test_confirm_file_delete[0], response_test_confirm_file_delete[1], response_test_confirm_file_delete[2])


    def testProjectTestCases(self):
        print('==================================================================')
        print(' Running Projects Operation Test Cases')
        print('==================================================================')

        response_test_run_project = self.project_test_case.run_project(self.Fixtures.project_name)
        self.assertEqual(response_test_run_project[0], response_test_run_project[1], response_test_run_project[2])

        response_test_delete_project = self.project_test_case.delete_project(self.Fixtures.project_name)
        self.assertEqual(response_test_delete_project[0], response_test_delete_project[1], response_test_delete_project[2])

        response_test_change_project_name = self.project_test_case.change_project_name(self.Fixtures.project_name, 'testing')
        self.assertEqual(response_test_change_project_name[0], response_test_change_project_name[1], response_test_change_project_name[2])

        response_test_save_project = self.project_test_case.save_project(self.Fixtures.project_name)
        self.assertEqual(response_test_save_project[0], response_test_save_project[1], response_test_save_project[2])


    def testEmailNotification(self):

        print('==================================================================')
        print(' Running Email Notification Test Cases')
        print('==================================================================')

        response_of_email = self.email_test_case.test_testing_email()
        self.assertEqual(response_of_email, True, 'Failed Testing Email ................. !')

        response_of_email_attachment = self.email_test_case.test_attachment_email()
        self.assertEqual(response_of_email_attachment, True, 'Failed Attachment Email ................. !')

        response_of_email_error = self.email_test_case.test_Error_email()
        self.assertEqual(response_of_email_error, True, 'Failed Error Email ................. !')

        pass
    def tearDown(self):
        print('Tear Down!')
        self.Fixtures.delete_testing_data()
        print('')
        pass

if __name__ == '__main__':
    unittest.main()

