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

from AllFixture.RequiredsCreationFixture import RequiredsCreationFixture

import ExpectedResults as ExpectedResults
import FailedMessages as FailedMessages

base_path = os.getcwd()
base_path = base_path.replace(r'\test', '')
sys.path.append(base_path+os.sep)
import Main


class RequiredsCreationTestCase(object):


    def __init__(self):
        self.App = Main.Main()
        self.requireds_creation_fixture = RequiredsCreationFixture()
        pass

    def is_report_dir_exists(self):
        """
        Is Report Dir Exists

        @return: @return: List
        """
        print('is report file exists..........!')

        self.requireds_creation_fixture.createDirsAndFiles()

        if os.path.isdir(self.App.Fixity.Configuration.getReportsPath()):
            flag = True
        else:
            flag = False

        self.requireds_creation_fixture.removeDirsAndFiles()
        print("---------------------------------------------------------------------\n")
        return [flag, ExpectedResults.RequiredsCreationTestCaseExpectedResult['all'], FailedMessages.RequiredsCreationTestCaseFailMessages['is_report_dir_exists']]

    def is_history_dir_exists(self):
        """
        Is History Dir Exists

        @return: @return: List
        """
        print('is history file exists..........!')

        self.requireds_creation_fixture.createDirsAndFiles()
        if os.path.isdir(self.App.Fixity.Configuration.getHistoryPath()):
            flag = True
        else:
            flag = False

        self.requireds_creation_fixture.removeDirsAndFiles()
        print("---------------------------------------------------------------------\n")
        return [flag, ExpectedResults.RequiredsCreationTestCaseExpectedResult['all'], FailedMessages.RequiredsCreationTestCaseFailMessages['is_history_dir_exists']]

    def is_schedules_dir_exists(self):
        """
        Is Schedules Dir Exists

        @return: @return: List
        """
        print('is schedules file exists..........!')

        self.requireds_creation_fixture.createDirsAndFiles()
        if os.path.isdir(self.App.Fixity.Configuration.getSchedulesPath()):
            flag = True
        else:
            flag = False

        self.requireds_creation_fixture.removeDirsAndFiles()
        print("---------------------------------------------------------------------\n")
        return [flag, ExpectedResults.RequiredsCreationTestCaseExpectedResult['all'], FailedMessages.RequiredsCreationTestCaseFailMessages['is_schedules_dir_exists']]

    def is_config_file_exists(self):
        """
        Is Config File Exist

        @return: @return: List
        """
        print('is config file exists..........!')

        self.requireds_creation_fixture.createDirsAndFiles()
        if os.path.isfile(self.App.Fixity.Configuration.getConfig_file_path()):
            flag = True
        else:
            flag = False

        self.requireds_creation_fixture.removeDirsAndFiles()
        print("---------------------------------------------------------------------\n")
        return [flag, ExpectedResults.RequiredsCreationTestCaseExpectedResult['all'], FailedMessages.RequiredsCreationTestCaseFailMessages['is_config_file_exists']]

    def is_database_file_exists(self):
        """
        Is Database File Exists

        @return: @return: List
        """
        print('is database file exists..........!')

        self.requireds_creation_fixture.createDirsAndFiles()
        if os.path.isfile(self.App.Fixity.Configuration.getDatabaseFilePath()):
            flag = True
        else:
            flag = False

        self.requireds_creation_fixture.removeDirsAndFiles()
        print("---------------------------------------------------------------------\n")
        return [flag, ExpectedResults.RequiredsCreationTestCaseExpectedResult['all'], FailedMessages.RequiredsCreationTestCaseFailMessages['is_database_file_exists']]

    def is_debug_files_exists(self):
        """
        Is Debug File Exists

        @return: List
        """

        print('is debug file exists..........!')

        self.requireds_creation_fixture.createDirsAndFiles()
        if os.path.isfile(self.App.Fixity.Configuration.getDebugFilePath()):
            flag = True
        else:
            flag = False

        self.requireds_creation_fixture.removeDirsAndFiles()
        print("---------------------------------------------------------------------\n")
        return [flag, ExpectedResults.RequiredsCreationTestCaseExpectedResult['all'], FailedMessages.RequiredsCreationTestCaseFailMessages['is_debug_files_exists']]