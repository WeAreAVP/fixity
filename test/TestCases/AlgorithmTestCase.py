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

from AllFixture.AlgorithmFixtures import AlgorithmFixtures
from AllFixture.ProjectFixtures import ProjectFixtures

import ExpectedResults as ExpectedResults
import FailedMessages as FailedMessages

class AlgorithmTestCase(object):

    def __init__(self):
        super(AlgorithmTestCase,self).__init__()
        self.App = Main.Main()
        self.algorithm_fixtures = AlgorithmFixtures()
        self.project_fixtures = ProjectFixtures()

        pass

    def test_confirm_file(self):

        print('Test Confirm File {( Nothing is Changed )} .........!')

        self.algorithm_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()
        print("---------------------------------------------------------------------\n")
        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_confirm_file'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_confirm_file']]

    def test_confirm_file_is_special_chars(self):

        print('Test Confirm File {( Nothing is Changed )} .........!')

        print('With Special Characters')
        self.algorithm_fixtures.load_special_verification_algorithm_data()

        is_special_chars = True
        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name, is_special_chars)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.unload_verification_algorithm_data_special()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()
        print("---------------------------------------------------------------------\n")
        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_confirm_file'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_confirm_file']]

    def test_confirm_if_inode_changed_of_file(self):

        print('Test Confirm File {( I-Node is Changed )} .........!')

        self.algorithm_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.change_inode(self.algorithm_fixtures.test_file_four)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3:moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_confirm_if_inode_changed_of_file'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_confirm_if_inode_changed_of_file']]

    def test_confirm_if_inode_changed_of_file_is_special_chars(self):

        print('Test Confirm File {( I-Node is Changed )} .........!')
        print('With Special Characters')
        self.algorithm_fixtures.load_special_verification_algorithm_data()

        is_special_chars = True
        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name, is_special_chars)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.change_inode(self.algorithm_fixtures.test_file_four_special)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.unload_verification_algorithm_data_special()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()
        print("---------------------------------------------------------------------\n")
        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_confirm_if_inode_changed_of_file'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_confirm_if_inode_changed_of_file']]

    def test_delete_file(self):

        print('Test Delete File .........!')

        self.algorithm_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.del_file(self.algorithm_fixtures.test_file_one)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_delete_file'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_delete_file']]

    def test_delete_file_is_special_chars(self):

        print('Test Delete File .........!')

        print('With Special Characters')
        self.algorithm_fixtures.load_special_verification_algorithm_data()

        is_special_chars = True
        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name, is_special_chars)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.del_file(self.algorithm_fixtures.test_file_one_special)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data_special()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_delete_file'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_delete_file']]

    def test_change_file(self):
        print('Test Change File {( Only Hash Changed )}.........!')

        self.algorithm_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.change_file(self.algorithm_fixtures.test_file_one)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_change_file'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_change_file']]

    def test_change_file_is_special_chars(self):
        print('Test Change File {( Only Hash Changed )}.........!')

        print('With Special Characters')
        self.algorithm_fixtures.load_special_verification_algorithm_data()

        is_special_chars = True
        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name, is_special_chars)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.change_file(self.algorithm_fixtures.test_file_one_special)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data_special()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_change_file'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_change_file']]

    def test_change_file_changed_hash_and_path(self):
        print('Test Change File  {( Hash and Path Changed )} .........!')

        self.algorithm_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.change_file_changed_hash_and_path(self.algorithm_fixtures.test_file_one)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_change_file_changed_hash_and_path'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_change_file_changed_hash_and_path']]

    def test_change_file_changed_hash_and_path_is_special_chars(self):
        print('Test Change File  {( Hash and Path Changed )} .........!')

        print('With Special Characters')
        self.algorithm_fixtures.load_special_verification_algorithm_data()

        is_special_chars = True

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name, is_special_chars)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.change_file_changed_hash_and_path(self.algorithm_fixtures.test_file_one_special)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data_special()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_change_file_changed_hash_and_path'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_change_file_changed_hash_and_path']]

    def test_change_inode_and_hash_file(self):
        print('Test Change File  {( I-Node and Hash Changed )} .........!')

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name)

        self.algorithm_fixtures.load_verification_algorithm_data()

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.change_inode_and_hash(self.algorithm_fixtures.test_file_one)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_change_inode_and_hash_file'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_change_inode_and_hash_file']]

    def test_change_inode_and_hash_file_is_special_chars(self):
        print('Test Change File  {( I-Node and Hash Changed )} .........!')
        print('With Special Characters')
        is_special_chars = True
        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name, is_special_chars)

        self.algorithm_fixtures.load_special_verification_algorithm_data()

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.change_inode_and_hash(self.algorithm_fixtures.test_file_one_special)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data_special()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_change_inode_and_hash_file'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_change_inode_and_hash_file']]

    def test_new_file(self):
        print('Test New File .........!')

        self.algorithm_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')


        self.algorithm_fixtures.new_file(self.algorithm_fixtures.test_file_one+'_new_file')

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_new_file'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_new_file']]

    def test_new_file_is_special_chars(self):
        print('Test New File .........!')
        print('With Special Characters')
        is_special_chars = True

        self.algorithm_fixtures.load_special_verification_algorithm_data()

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name, is_special_chars)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.new_file(self.algorithm_fixtures.test_file_one_special+'_new_file')

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data_special()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_new_file'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_new_file']]

    def test_moved_file(self):
        print('Test Moved File .........!')

        self.algorithm_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.rename_file(self.algorithm_fixtures.test_file_one,
                                            self.algorithm_fixtures.test_file_one + '_unit_test')

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_moved_file'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_moved_file']]

    def test_moved_file_to_new_directory(self):
        print('Test Moved File to New Directory .........!')

        self.algorithm_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.move_file_in_a_directory(self.algorithm_fixtures.test_file_three, self.algorithm_fixtures.new_directory + '3.docx')

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_moved_file_to_new_directory'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_moved_file_to_new_directory']]

    def test_moved_file_to_new_Directory_change_hash(self):
        print('Test Moved File to New Directory and changed hash .........!')

        self.algorithm_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.move_file_in_directory_and_change_hash(self.algorithm_fixtures.test_file_three,
                                                                       self.algorithm_fixtures.new_directory + '3.docx')

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_moved_file_to_new_Directory_change_hash'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_moved_file_to_new_Directory_change_hash']]

    def test_moved_file_to_new_Directory_change_name_as_old(self):

        print('Test created new file New Directory and changed name as old .........!')

        self.algorithm_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.create_copy_of_a_file_removed_old_change_name_as_old()

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_moved_file_to_new_Directory_change_name_as_old'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_moved_file_to_new_Directory_change_name_as_old']]

    def test_moved_to_new_directory_change_name_as_old_and_content(self):
        print('Test created new file New Directory and changed name as old changed hash .........!')

        self.algorithm_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.create_copy_of_a_file_removed_old_change_name_as_old_change_content()

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_moved_to_new_Directory_change_name_as_old_and_content'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_moved_to_new_Directory_change_name_as_old_and_content']]

    def test_moved_file_is_special_chars(self):
        print('Test Moved File .........!')
        is_special_chars= True
        print('With Special Characters')
        self.algorithm_fixtures.load_special_verification_algorithm_data()

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name, is_special_chars)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.rename_file(self.algorithm_fixtures.test_file_one_special, self.algorithm_fixtures.test_file_one_special + '_unit_test')

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.unload_verification_algorithm_data_special()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_moved_file'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_moved_file']]

    def test_change_base_path(self):
        print('Test Changed bath Path .........!')

        self.algorithm_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name)

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.change_directory_path()

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_change_base_path'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_change_base_path']]

    def test_intersection_of_dir(self):

        print('test intersection of File .........!')
        base_path_of_unitest  = self.App.Fixity.Configuration.getBasePath()

        file_path_given_to_be_created1 = base_path_of_unitest+'test3' + os.sep + '1.docx'
        file_path_given_to_be_created2 = base_path_of_unitest+'test3' + os.sep + '2.docx'
        file_path_given_to_be_created3 = base_path_of_unitest+'test3' + os.sep + '3.docx'
        file_path_given_to_be_created4 = base_path_of_unitest+'test3' + os.sep + '4.txt'


        self.algorithm_fixtures.load_verification_algorithm_data()
        base_path = base_path_of_unitest+'test3'

        self.algorithm_fixtures.load_verification_algorithm_data_for_intersect(file_path_given_to_be_created1, base_path, '1 document')
        self.algorithm_fixtures.load_verification_algorithm_data_for_intersect(file_path_given_to_be_created2, base_path, '2 document')
        self.algorithm_fixtures.load_verification_algorithm_data_for_intersect(file_path_given_to_be_created3, base_path, '3 document')
        self.algorithm_fixtures.load_verification_algorithm_data_for_intersect(file_path_given_to_be_created4, base_path, '4 document')

        self.project_fixtures.create_new_project(self.algorithm_fixtures.project_name)
        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        self.algorithm_fixtures.change_path_custom(base_path)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test', base_path)

        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.algorithm_fixtures.delete_testing_data()

        print("---------------------------------------------------------------------\n")

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed},
                ExpectedResults.AlgorithmTestCaseExpectedResult['test_intersection_of_dir'],
                FailedMessages.AlgorithmTestCaseFailMessages['test_intersection_of_dir']]