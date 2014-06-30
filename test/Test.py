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
from Fixtures import Fixtures

class Test(unittest.TestCase):

    def setUp(self):
        self.Fixtures = Fixtures()
        self.project_name = 'New_Project'
        self.Fixtures.create_new_project(self.project_name)
        self.Fixtures.load_verification_algorithm_data()
        self.App = Main.Main()
        self.App.Fixity.loadAllProjects()
        pass


    def test_confirm_file(self):
        try:
            print('id')
        except:
            raise Exception("could not create new project")
            pass
        self.App.LaunchCLI(self.project_name)
        self.Fixtures.del_file()
        self.App.LaunchCLI(self.project_name)


    #def test_delete_file_verification(self):
    #    self.assertEqual(4 * 3, 12)
    #
    #
    #def test_change_file_verification(self):
    #    self.assertEqual(4 * 3, 12)
    #
    #def test_new_file_verification(self):
    #    self.assertEqual(4 * 3, 12)
    #
    #def test_removed_verification(self):
    #    self.assertEqual(4 * 3, 12)


    def tearDown(self):
        print('tera down')
        self.Fixtures.delete_testing_data()
        pass


if __name__ == '__main__':
    unittest.main()
