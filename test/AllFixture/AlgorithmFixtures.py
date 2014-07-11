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


class AlgorithmFixtures(Fixtures):

    def __init__(self):
        self.App = Main.Main()
        super(AlgorithmFixtures,self).__init__()
        self.new_directory = self.unit_test_folder+'testing_new_dir'
        self.new_file_name_temp = self.unit_test_folder+'testing1234.docx'
        pass

    # Del File
    #
    # @param path_to_be_changed:string  Path to be change for testing
    def del_file(self, path_to_be_deleted):
        os.remove(path_to_be_deleted.decode('utf-8'))
        pass

    # Rename File
    #
    # @param path_to_be_changed:string  Path to be change for testing

    def rename_file(self, path_to_be_renamed, new_name):
        os.rename(new_name, path_to_be_renamed)
        pass


    # Move File In a Directory
    #
    # @param path_to_be_changed:string  Path to be change for testing
    # @param path_to_be_moved_to:string  Path to be change with
    def move_file_in_a_directory(self, path_to_be_moved, path_to_be_moved_to):
        if not os.path.exists(self.new_directory):
            os.makedirs(self.new_directory)

        shutil.move(path_to_be_moved, path_to_be_moved_to)
        pass


    # Copy , Paste a File , Then Remove old File also change name of the new file as old one
    def create_copy_of_a_file_removed_old_change_name_as_old(self):
        shutil.copy(self.test_file_two, self.new_file_name_temp)
        os.remove(self.test_file_two)
        self.rename_file(self.new_file_name_temp, self.test_file_two)


    # Copy , Paste a File , Then Remove old File and change content of New file also change name of the new file as old one
    def create_copy_of_a_file_removed_old_change_name_as_old_change_content(self):
        shutil.copy(self.test_file_two, self.new_file_name_temp)
        os.remove(self.test_file_two)
        self.rename_file(self.new_file_name_temp, self.test_file_two)
        self.new_file(self.test_file_two, 'Copy , Paste a File , Then Remove old File and change content of New file also change name of the new file as old one, Copy , Paste a File , Then Remove old File and change content of New file also change name of the new file as old one')


    # Move File In a Directory and Change hash
    #
    # @param path_to_be_changed:string  Path to be change for testing
    # @param path_to_be_moved_to:string  Path to be change with
    def move_file_in_directory_and_change_hash(self, path_to_be_moved, path_to_be_moved_to):

        if not os.path.exists(self.new_directory):
            print(self.new_directory)
            os.makedirs(self.new_directory)

        shutil.move(path_to_be_moved, path_to_be_moved_to)
        self.new_file(path_to_be_moved_to, 'Move file with in a directory and change content , Move file with in a directory and change content ')
        pass


    # New File
    #
    # @param path_to_be_changed:string  Path to be change for testing
    def new_file(self, path_to_be_created, content = '4 document'):
        file_obj = open(path_to_be_created.decode('utf-8'), 'w')
        file_obj.write(content)
        file_obj.close()
        pass

    # Confirm File
    #
    # @param path_to_be_changed:string  Path to be change for testing
    def change_inode(self, path_to_be_changed):
        self.del_file(path_to_be_changed)
        self.new_file(path_to_be_changed)
        pass

    # Changed File
    #
    # @param path_to_be_changed:string  Path to be change for testing
    def change_inode_and_hash(self, path_to_be_changed):
        self.del_file(path_to_be_changed)
        self.new_file(path_to_be_changed,'testing the hash and inode changed')
        pass

    # Change File
    #
    # @param path_to_be_changed:string  Path to be change for testing
    def change_file(self, path_to_be_changed):
        file_obj = open(path_to_be_changed.decode('utf-8'), 'w')
        file_obj.write('testing new file '+str(random.randrange(1, 10000)))
        file_obj.close()
        pass

    # Changed File
    #
    # @param path_to_be_changed:string  Path to be change for testing
    def change_file_changed_hash_and_path(self, path_to_be_changed):
        file_obj = open(path_to_be_changed.decode('utf-8'), 'w')
        file_obj.write('testing new file '+str(random.randrange(1, 10000)))
        file_obj.close()

        self.rename_file(path_to_be_changed, path_to_be_changed + '_check')
        pass


    # Changed Directory Path
    #
    # @param path_to_be_changed:string  Path to be change for testing
    def change_directory_path(self):
        last_different_paths = self.unit_test_folder+'||-||Fixity-1,||-||Fixity-2,||-||Fixity-3,||-||Fixity-4,||-||Fixity-5,||-||Fixity-6,||-||Fixity-7'
        self.unit_test_folder = self.App.Fixity.Configuration.getBasePath()+'test2'

        self.test_file_one = self.App.Fixity.Configuration.getBasePath()+'test2'+os.sep+ '1.docx'
        self.test_file_two = self.App.Fixity.Configuration.getBasePath()+'test2'+os.sep+ '2.docx'
        self.test_file_three = self.App.Fixity.Configuration.getBasePath()+'test2'+os.sep+ '3.docx'
        self.test_file_four = self.App.Fixity.Configuration.getBasePath()+'test2'+os.sep+ '4.docx'

        self.load_verification_algorithm_data()

        information = {}
        information['path'] = self.unit_test_folder
        self.App.Fixity.Database.update(self.App.Fixity.Database._tableProjectPath, information, '1 = 1')
        information_update_project = {}
        information_update_project['lastDifPaths'] = last_different_paths
        self.App.Fixity.Database.update(self.App.Fixity.Database._tableProject, information_update_project, '1 = 1')

        pass

    # Rename File
    #
    # @param path_to_be_changed:string  Path to be change for testing
    # @param new_path:string  Path to be changed with for testing
    def rename_file(self, path_to_be_changed , new_path):

        os.rename(path_to_be_changed.decode('utf-8'), new_path.decode('utf-8'))
        pass


