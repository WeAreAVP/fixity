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

class TestHelper(object):

    def __init__(self):
        self.App = Main.Main()
        self.unit_test_folder = self.App.Fixity.Configuration.getUnit_test_folder()

        self.test_file_one = self.unit_test_folder + '1.docx'
        self.test_file_two = self.unit_test_folder + '2.docx'
        self.test_file_three = self.unit_test_folder + '3.docx'
        self.test_file_four = self.unit_test_folder + '4.docx'
        pass


    # Delete Testing Data
    def delete_testing_data(self):

        if os.path.exists(self.unit_test_folder):
            shutil.rmtree(self.unit_test_folder)

        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableProject, '1 = 1')
        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableVersionDetail, '1 = 1')
        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableProjectPath, '1 = 1')

        pass


    # Del File
    def del_file(self, path_to_be_deleted):
        os.remove(path_to_be_deleted)
        pass

    # Rename File
    def rename_file(self, path_to_be_renamed, new_name):
        os.rename(new_name, path_to_be_renamed)
        pass

    # New File
    def new_file(self, path_to_be_created):
        file_obj = open(path_to_be_created, 'w')
        file_obj.write('testing new file' + str(random.randrange(1, 10000)))
        file_obj.close()
        pass

    # Change File
    def change_file(self, path_to_be_changed):
        file_obj = open(path_to_be_changed, 'w')
        file_obj.write('testing new file '+str(random.randrange(1, 10000)))
        file_obj.close()
        pass
