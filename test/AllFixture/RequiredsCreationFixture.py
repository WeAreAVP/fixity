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
import shutil

base_path = os.getcwd()
base_path = base_path.replace(r'\test', '')
base_path = base_path.replace(r'\Fixture', '')
sys.path.append(base_path+os.sep)

import Main


class RequiredsCreationFixture(Fixtures):


    def __init__(self):
        self.App = Main.Main()
        super(RequiredsCreationFixture, self).__init__()
        self.base_folder = self.App.Fixity.Configuration.getBasePath()
        print(self.base_folder)

        pass

    def removeDirsAndFiles(self):

        try:
            os.remove(self.base_folder + 'Fixity.db')
        except:
            pass

        try:
            os.remove(self.base_folder + 'conf.xml')
        except:
            pass

        try:
           os.remove(self.base_folder + 'debug.log')
        except:
            pass

        try:
            shutil.rmtree(self.base_folder + 'reports')
        except:
            pass

        try:
            shutil.rmtree(self.base_folder + 'history')
        except:
            pass

        try:
            shutil.rmtree(self.base_folder + 'schedules')
        except:
            pass

        pass

    def createDirsAndFiles(self):
        self.removeDirsAndFiles()
        self.App = Main.Main()
        self.App.Fixity.Setup.setupApp()
        pass