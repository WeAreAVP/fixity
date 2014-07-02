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
from AlgorithmFixtures import AlgorithmFixtures
import unittest

class AlgorithmTestCase(object):

    def __init__(self):
        super(AlgorithmTestCase,self).__init__()
        self.App = Main.Main()
        self.algorithm_fixtures = AlgorithmFixtures()
        pass

    def test_confirm_file(self, is_special_chars = False):

        print('')
        print('Test Confirm File {( Nothing is Changed )} .........!')

        if is_special_chars:
            self.algorithm_fixtures.load_special_verification_algorithm_data()
        else:
            self.algorithm_fixtures.load_verification_algorithm_data()

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.Fixtures.delete_testing_data()
        return [{0:confirmed, 1:missing_file, 2:created, 3:moved, 4:corrupted_or_changed}, {0:4, 1: 0, 2: 0, 3: 0, 4: 0}, 'Failed Confirm File Unit Test']




    def test_confirm_if_inode_changed_of_file(self, is_special_chars = False):
        print('Test Confirm File {( I-Node is Changed )} .........!')
        if is_special_chars:
            self.algorithm_fixtures.load_special_verification_algorithm_data()
        else:
            self.algorithm_fixtures.load_verification_algorithm_data()

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        if is_special_chars:
            self.algorithm_fixtures.change_inode(self.algorithm_fixtures.test_file_four_special)
        else:
            self.algorithm_fixtures.change_inode(self.algorithm_fixtures.test_file_four)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.Fixtures.delete_testing_data()
        return [{0:confirmed, 1:missing_file, 2:created, 3:moved, 4:corrupted_or_changed}, {0:4, 1: 0, 2: 0, 3: 0, 4: 0}, 'Failed Confirm File Unit Test']



    def test_delete_file(self, is_special_chars = False):
        print('Test Delete File .........!')
        if is_special_chars:
            self.algorithm_fixtures.load_special_verification_algorithm_data()
        else:
            self.algorithm_fixtures.load_verification_algorithm_data()

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        if is_special_chars:
            self.algorithm_fixtures.del_file(self.algorithm_fixtures.test_file_one_special)
        else:
            self.algorithm_fixtures.del_file(self.algorithm_fixtures.test_file_one)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.Fixtures.delete_testing_data()
        return [{0:confirmed, 1:missing_file, 2:created, 3:moved, 4:corrupted_or_changed}, {0:3, 1: 1, 2: 0, 3: 0, 4: 0}, 'Failed Delete File Unit Test']



    def test_change_file(self, is_special_chars = False):
        print('Test Change File {( Only Hash Changed )}.........!')
        if is_special_chars:
            self.algorithm_fixtures.load_special_verification_algorithm_data()
        else:
            self.algorithm_fixtures.load_verification_algorithm_data()

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        if is_special_chars:
            self.algorithm_fixtures.change_file(self.algorithm_fixtures.test_file_one_special)
        else:
            self.algorithm_fixtures.change_file(self.algorithm_fixtures.test_file_one)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.Fixtures.delete_testing_data()
        return [{0:confirmed, 1:missing_file, 2:created, 3:moved, 4:corrupted_or_changed}, {0:3, 1: 0, 2: 0, 3: 0, 4: 1}, 'Failed Change File {( Only Hash Changed )} Unit Test']



    def test_change_file_changed_hash_and_path(self, is_special_chars = False):
        print('Test Change File  {( Hash and Path Changed )} .........!')
        if is_special_chars:
            self.algorithm_fixtures.load_special_verification_algorithm_data()
        else:
            self.algorithm_fixtures.load_verification_algorithm_data()

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        if is_special_chars:
            self.algorithm_fixtures.change_file_changed_hash_and_path(self.algorithm_fixtures.test_file_one_special)
        else:
            self.algorithm_fixtures.change_file_changed_hash_and_path(self.algorithm_fixtures.test_file_one)

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.Fixtures.delete_testing_data()

        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed}, {0: 3, 1: 0, 2: 0, 3: 0, 4: 1}, 'Failed Change File {( Hash and Path Changed )} Unit Test']


    def test_change_inode_and_hash_file(self, is_special_chars = False):
        print('Test Change File  {( I-Node and Hash Changed )} .........!')
        if is_special_chars:
            self.algorithm_fixtures.load_special_verification_algorithm_data()
        else:
            self.algorithm_fixtures.load_verification_algorithm_data()

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        if is_special_chars:
            self.algorithm_fixtures.change_inode_and_hash(self.algorithm_fixtures.test_file_one_special)
        else:
            self.algorithm_fixtures.change_inode_and_hash(self.algorithm_fixtures.test_file_one)


        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.Fixtures.delete_testing_data()
        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed}, {0: 3, 1: 0, 2: 0, 3: 0, 4: 1}, 'Failed Change File {( I-Node and Hash Changed )} Unit Test']



    def test_new_file(self, is_special_chars = False):
        print('Test New File .........!')
        if is_special_chars:
            self.algorithm_fixtures.load_special_verification_algorithm_data()
        else:
            self.algorithm_fixtures.load_verification_algorithm_data()

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')

        if is_special_chars:
            self.algorithm_fixtures.new_file(self.algorithm_fixtures.test_file_one_special+'_new_file')
        else:
            self.algorithm_fixtures.new_file(self.algorithm_fixtures.test_file_one+'_new_file')

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.Fixtures.delete_testing_data()
        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed}, {0: 4, 1: 0, 2: 1, 3: 0, 4: 0}, 'Failed New File Unit Test']


    def test_moved_file(self, is_special_chars = False):
        print('Test Moved File .........!')

        if is_special_chars:
            self.algorithm_fixtures.load_special_verification_algorithm_data()
        else:
            self.algorithm_fixtures.load_verification_algorithm_data()

        self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        if is_special_chars:
            self.algorithm_fixtures.rename_file(self.algorithm_fixtures.test_file_one_special, self.algorithm_fixtures.test_file_one + '_unit_test')
        else:
            self.algorithm_fixtures.rename_file(self.algorithm_fixtures.test_file_one, self.algorithm_fixtures.test_file_one + '_unit_test')

        report_info_two = self.App.LaunchCLI(self.algorithm_fixtures.project_name, 'test')
        self.algorithm_fixtures.unload_verification_algorithm_data()

        confirmed = report_info_two['confirmed']
        missing_file = report_info_two['missing_file']
        created = report_info_two['created']
        moved = report_info_two['moved']
        corrupted_or_changed = report_info_two['corrupted_or_changed']

        self.Fixtures.delete_testing_data()
        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed}, {0: 3, 1: 0, 2: 0, 3: 1, 4: 0}, 'Failed New File Unit Test']



