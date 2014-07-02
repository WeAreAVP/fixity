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
from EmailFixtures import EmailFixtures
from Core import EmailNotification


class EmailTestCase(object):


    def __init__(self):
        self.App = Main.Main()
        self.email_fixtures = EmailFixtures()
        self.email_notification = EmailNotification.EmailNotification()
        pass

    def test_testing_email(self):
        print('Testing Email..........!')
        response = self.email_notification.TestingEmail(self.email_fixtures.recipients, 'Testing the Email', self.email_fixtures.EmailInformation())
        return [response, True, 'Failed Testing Email ................. !']
        pass

    def test_attachment_email(self):
        print('Attachment Email..........!')
        self.email_fixtures.load_attachment()
        response = self.email_notification.ReportEmail(self.email_fixtures.recipients, self.email_fixtures.attachment ,'Testing the Email' ,self.email_fixtures.EmailInformation(), self.email_fixtures.project_name)
        self.email_fixtures.unload_attachment()
        return [response, True, 'Failed Attachment Email ................. !']

    def test_Error_email(self):
        print('Error Email..........!')
        self.email_fixtures.load_attachment()
        response = self.email_notification.ErrorEmail(self.email_fixtures.recipients, self.email_fixtures.attachment ,'Testing the Email' ,self.email_fixtures.EmailInformation(), self.email_fixtures.project_name)
        self.email_fixtures.unload_attachment()
        return [response, True, 'Failed Error Email ................. !']

