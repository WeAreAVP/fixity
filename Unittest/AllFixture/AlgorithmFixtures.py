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
        super(AlgorithmFixtures, self).__init__()
        self.new_directory = self.unit_test_folder + 'testing_new_dir' + os.sep
        self.new_file_name_temp = self.unit_test_folder + 'testing1234.docx'
        pass

    def move_file_in_a_directory(self, path_to_be_moved, path_to_be_moved_to):
        """
        Move File In a Directory

        @param path_to_be_changed:string  Path to be change for testing
        @param path_to_be_moved_to:string  Path to be change with
        """

        if not os.path.exists(self.new_directory):
            os.makedirs(self.new_directory)

        shutil.move(path_to_be_moved, path_to_be_moved_to)
        pass

    def create_copy_of_a_file_removed_old_change_name_as_old(self):
        """
        Copy , Paste a File , Then Remove old File also change name of the new file as old one
        """
        shutil.copy(self.test_file_two, self.new_file_name_temp)
        os.remove(self.test_file_two)
        self.rename_file(self.new_file_name_temp, self.test_file_two)

    def create_copy_of_a_file_removed_old_change_name_as_old_change_content(self):
        """
        Copy , Paste a File , Then Remove old File and change
        content of New file also change name of the new file as old one
        """
        shutil.copy(self.test_file_two, self.new_file_name_temp)
        os.remove(self.test_file_two)
        self.rename_file(self.new_file_name_temp, self.test_file_two)
        self.new_file(self.test_file_two,
                      'Copy , Paste a File , Then Remove old File and change content of' +
                      ' New file also change name of the new file as old one, Copy ,' +
                      ' Paste a File , Then Remove old File and change content of New ' +
                      'file also change name of the new file as old one')

    def move_file_in_directory_and_change_hash(self, path_to_be_moved, path_to_be_moved_to):
        """
        Move File In a Directory and Change hash

        @param path_to_be_changed:string  Path to be change for testing
        @param path_to_be_moved_to:string  Path to be change with
        """
        if not os.path.exists(self.new_directory):

            os.makedirs(self.new_directory)

        shutil.move(path_to_be_moved, path_to_be_moved_to)
        self.new_file(path_to_be_moved_to,
                      'Move file with in a directory and change content , ' +
                      'Move file with in a directory and change content.')
        pass

    def change_inode(self, path_to_be_changed):
        """
        Change Inode

        @param path_to_be_changed:string  Path to be change for testing
        """
        self.del_file(path_to_be_changed)
        self.new_file(path_to_be_changed)
        pass

    def change_inode_and_hash(self, path_to_be_changed):
        """
        Changed File

        @param path_to_be_changed:string  Path to be change for testing
        """
        self.del_file(path_to_be_changed)
        self.new_file(path_to_be_changed, 'testing the hash and inode changed')
        pass

    def change_file_changed_hash_and_path(self, path_to_be_changed):
        """
        Change File

        @param path_to_be_changed:string  Path to be change for testing
         """
        file_obj = open(path_to_be_changed.decode('utf-8'), 'w')
        file_obj.write('testing new file ' + str(random.randrange(1, 10000)))
        file_obj.close()

        self.rename_file(path_to_be_changed, path_to_be_changed + '_check')
        pass

    def load_verification_algorithm_data_for_intersect(self, file_path_given_to_be_created, base_path, content):
        """
        Load Verification Algorithm Data For Intersect

        @param file_path_given_to_be_created:string Path to be of file to be created
        @param base_path:string  Base Path of intersect directory
        @param content:string  Content for the created files
        """
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        file_obj1 = open(file_path_given_to_be_created, 'w+')
        file_obj1.write(content)
        file_obj1.close()

        pass

    def change_directory_path(self):
        """
        Changed Directory Path

        @param path_to_be_changed:string  Path to be change for testing
        """
        last_different_paths = self.unit_test_folder + '||-||Fixity-1,||-||Fixity-2,||-||Fixity-3,||-||Fixity-4,||-||Fixity-5,||-||Fixity-6,||-||Fixity-7'
        self.unit_test_folder = self.App.Fixity.Configuration.getBasePath() + 'test2'

        self.test_file_one = self.App.Fixity.Configuration.getBasePath() + 'test2' + os.sep + '1.docx'
        self.test_file_two = self.App.Fixity.Configuration.getBasePath() + 'test2' + os.sep + '2.docx'
        self.test_file_three = self.App.Fixity.Configuration.getBasePath() + 'test2' + os.sep + '3.docx'
        self.test_file_four = self.App.Fixity.Configuration.getBasePath() + 'test2' + os.sep + '4.docx'

        self.load_verification_algorithm_data()

        information = {}
        information['path'] = self.unit_test_folder
        self.App.Fixity.Database.update(self.App.Fixity.Database._tableProjectPath, information, '1 = 1')
        information_update_project = {}
        information_update_project['lastDifPaths'] = last_different_paths
        self.App.Fixity.Database.update(self.App.Fixity.Database._tableProject,
                                        information_update_project, '1 = 1')
        pass

    def change_path_custom(self, new_path):
        """
        Change Project Dirs Base Path Given

        @param new_path:string  Path to be change for testing
        """
        last_different_paths = new_path + '||-||Fixity-1,||-||Fixity-2,||-||Fixity-3,||-||Fixity-4,||-||Fixity-5,||-||Fixity-6,||-||Fixity-7'
        information = {}
        information['path'] = new_path
        self.App.Fixity.Database.update(self.App.Fixity.Database._tableProjectPath
            , information, '1 = 1')

        information_update_project = {}
        information_update_project['lastDifPaths'] = last_different_paths
        self.App.Fixity.Database.update(self.App.Fixity.Database._tableProject,
                                        information_update_project, '1 = 1')

    def rename_file(self, path_to_be_changed, new_path):
        """
        Rename File

        @param path_to_be_changed:string  Path to be change for testing
        @param new_path:string  Path to be changed with for testing
        """

        try:
            os.rename(path_to_be_changed, new_path)
        except:
            try:
                os.rename(path_to_be_changed.decode('utf-8'), new_path.decode('utf-8'))
            except:
                os.rename(path_to_be_changed.encode('utf-8'), new_path.encode('utf-8'))
                pass
            pass
        pass

    def change_file(self, path_to_be_changed):
        """
        Change File

        @param path_to_be_changed:
        @return:
        """

        file_obj = open(path_to_be_changed.decode('utf-8'), 'w')
        file_obj.write('testing new file ' + str(random.randrange(1, 10000)))
        file_obj.close()
        pass

    def del_file(self, path_to_be_deleted):
        """
        Delete File

        @param path_to_be_deleted:
        @return:
        """
        os.remove(path_to_be_deleted.decode('utf-8'))
        pass

    def new_file(self, path_to_be_created, content='4 document'):
        """
        New File

        @param path_to_be_created: Path to be created
        @param content:File Content to be created

        @return:
        """
        try:
            file_obj = open(path_to_be_created.decode('utf-8'), 'w')
            file_obj.write(content)
            file_obj.close()
        except:
            try:
                file_obj = open(path_to_be_created.encode('utf-8'), 'w')
                file_obj.write(content)
                file_obj.close()
            except:
                file_obj = open(path_to_be_created, 'w')
                file_obj.write(content)
                file_obj.close()
                pass
            pass
        pass