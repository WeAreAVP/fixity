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
import sys
base_path = os.getcwd()
base_path = base_path.replace(r'\test', '')
base_path = base_path.replace(r'\Fixture', '')
sys.path.append(base_path+os.sep)
import Main
from Fixtures import Fixtures


class EmailFixtures(Fixtures):

    def __init__(self):
        self.App = Main.Main()
        super(EmailFixtures, self).__init__()
        self.information = {}

        self.information['email'] = 'test.bf007@gmail.com'
        self.information['pass'] = 'purelogics'
        self.information['smtp'] = 'smtp.gmail.com'
        self.information['protocol'] = 'ssl'
        self.information['port'] = '465'

        self.recipients = 'furqan@geekschicago.com'
        pass

    def EmailInformation(self):
        return self.information

