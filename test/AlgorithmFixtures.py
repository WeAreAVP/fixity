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
        pass

    # Del File
    #
    # @param path_to_be_changed:string  Path to be change for testing
    def del_file(self, path_to_be_deleted):
        os.remove(path_to_be_deleted)
        pass

    # Rename File
    #
    # @param path_to_be_changed:string  Path to be change for testing
    def rename_file(self, path_to_be_renamed, new_name):
        os.rename(new_name, path_to_be_renamed)
        pass

    # New File
    #
    # @param path_to_be_changed:string  Path to be change for testing
    def new_file(self, path_to_be_created, content = '4 document'):
        file_obj = open(path_to_be_created, 'w')
        file_obj.write(content)
        file_obj.close()
        pass

    def change_inode(self, path_to_be_changed):
        self.del_file(path_to_be_changed)
        self.new_file(path_to_be_changed)
        pass

    def change_inode_and_hash(self, path_to_be_changed):
        self.del_file(path_to_be_changed)
        self.new_file(path_to_be_changed,'testing the hash and inode changed')
        pass

    # Change File
    #
    # @param path_to_be_changed:string  Path to be change for testing
    def change_file(self, path_to_be_changed):
        file_obj = open(path_to_be_changed, 'w')
        file_obj.write('testing new file '+str(random.randrange(1, 10000)))
        file_obj.close()
        pass

    def change_file_changed_hash_and_path(self, path_to_be_changed):
        file_obj = open(path_to_be_changed, 'w')
        file_obj.write('testing new file '+str(random.randrange(1, 10000)))
        file_obj.close()

        self.rename_file(path_to_be_changed, path_to_be_changed + '_check')
        pass


    # Rename File
    #
    # @param path_to_be_changed:string  Path to be change for testing
    # @param new_path:string  Path to be changed with for testing
    def rename_file(self, path_to_be_changed , new_path):
        os.rename(path_to_be_changed, new_path)
        pass


