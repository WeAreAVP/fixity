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
from Fixtures import Fixtures


class EmailFixtures(Fixtures):

    def __init__(self):
        self.App = Main.Main()
        super(EmailFixtures, self).__init__()
        self.information = {}

        self.information['email'] = 'furqan@geekschicago.com'
        self.information['pass'] = 'furqanwasi'
        self.information['smtp'] = 'smtp.gmail.com'
        self.information['protocol'] = 'ssl'
        self.information['port'] = '465'

        self.recipients = 'furqan@geekschicago.com'
        pass

    def EmailInformation(self):
        return self.information

