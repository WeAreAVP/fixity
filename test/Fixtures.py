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


class Fixtures(object):


    def __init__(self):
        self.App = Main.Main()
        self.unit_test_folder = self.App.Fixity.Configuration.getUnit_test_folder()
        self.project_name = 'New_Project'
        self.test_file_one = self.unit_test_folder + '1.docx'
        self.test_file_two = self.unit_test_folder + '2.docx'
        self.test_file_three = self.unit_test_folder + '3.docx'
        self.test_file_four = self.unit_test_folder + '4.docx'
        self.attachment = self.unit_test_folder + 'attachment.tsv'
        pass



    # Delete Testing Data
    def delete_testing_data(self):

        if os.path.exists(self.unit_test_folder):
            shutil.rmtree(self.unit_test_folder)

        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableProject, '1 = 1')
        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableVersionDetail, '1 = 1')
        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableProjectPath, '1 = 1')

        pass


    # Load Verification Algorithm Data
    def load_verification_algorithm_data(self):

        if os.path.exists(self.unit_test_folder):
            shutil.rmtree(self.unit_test_folder)
        os.makedirs(self.unit_test_folder)

        file_obj1 = open(self.test_file_one, 'w+')
        file_obj1.write('1 document' + str(random.randrange(1, 10000)))
        file_obj1.close()

        file_obj1 = open(self.test_file_two, 'w+')
        file_obj1.write('2 document' + str(random.randrange(1, 10000)))
        file_obj1.close()

        file_obj1 = open(self.test_file_three, 'w+')
        file_obj1.write('3 document' + str(random.randrange(1, 10000)))
        file_obj1.close()

        file_obj1 = open(self.test_file_four, 'w+')
        file_obj1.write('4 document')
        file_obj1.close()

    def load_attachment(self):
        if os.path.exists(self.unit_test_folder):
            shutil.rmtree(self.unit_test_folder)
        os.makedirs(self.unit_test_folder)
        file_obj1 = open(self.attachment, 'w+')
        file_obj1.write('Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment ')
        file_obj1.close()

    def unload_attachment(self):
        if os.path.exists(self.unit_test_folder):
            shutil.rmtree(self.unit_test_folder)

    # Delete Testing Data
    def unload_verification_algorithm_data(self):

        if os.path.exists(self.unit_test_folder):
            shutil.rmtree(self.unit_test_folder)

        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableVersionDetail, '1 = 1')
        pass

