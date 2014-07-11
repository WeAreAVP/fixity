# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''

EmailTestCaseFailMessages = {}
ProjectTestCaseFailMessages = {}
AlgorithmTestCaseFailMessages = {}
RequiredsCreationTestCaseFailMessages = {}

EmailTestCaseFailMessages['testing'] = 'Failed Testing Email ................. !'
EmailTestCaseFailMessages['attachment'] = 'Failed Attachment Email ................. !'
EmailTestCaseFailMessages['error'] = 'Failed Error Email ................. !'

ProjectTestCaseFailMessages['run_project'] = 'Failed Run Project Unit Test ................. !'
ProjectTestCaseFailMessages['delete_project'] = "Failed Delete Project Unit Test ................. !"
ProjectTestCaseFailMessages['change_project_name'] = "Failed Change Project Name Unit Test ................. !"
ProjectTestCaseFailMessages['change_algorithm'] =  "Failed Algo Change Unit Test ................. !"
ProjectTestCaseFailMessages['filters_files'] = 'Failed Filters Project files ................. !'
ProjectTestCaseFailMessages['import_project'] = "Failed Import Project Unit Test ................. !"
ProjectTestCaseFailMessages['save_project'] = "Failed Save Project Unit Test ................. !"

AlgorithmTestCaseFailMessages['test_confirm_file'] = "Failed Confirm File Unit Test ................. !"
AlgorithmTestCaseFailMessages['test_confirm_if_inode_changed_of_file'] = 'Failed Confirm File Unit Test ................. !'
AlgorithmTestCaseFailMessages['test_delete_file'] = 'Failed Delete File Unit Test ................. !'
AlgorithmTestCaseFailMessages['test_change_file'] = 'Failed Change File {( Only Hash Changed )} Unit Test ................. !'
AlgorithmTestCaseFailMessages['test_change_file_changed_hash_and_path'] = 'Failed Change File {( Hash and Path Changed )} Unit Test ................. !'
AlgorithmTestCaseFailMessages['test_change_inode_and_hash_file'] = 'Failed Change File {( I-Node and Hash Changed )} Unit Test ................. !'
AlgorithmTestCaseFailMessages['test_new_file'] = 'Failed New File Unit Test ................. !'
AlgorithmTestCaseFailMessages['test_moved_file'] =  'Failed New File Unit Test ................. !'
AlgorithmTestCaseFailMessages['test_moved_file_to_new_directory'] = 'Failed Moved File into a Directory Unit Test ................. !'
AlgorithmTestCaseFailMessages['test_moved_file_to_new_Directory_change_hash'] =  'Failed Moved into a Directory and Changed Hash of a File Unit Test ................. !'
AlgorithmTestCaseFailMessages['test_moved_file_to_new_Directory_change_name_as_old'] =  'Failed Copy , Paste a File , Then Remove old File also change name of the new file as old one Unit Test ................. !'
AlgorithmTestCaseFailMessages['test_moved_to_new_Directory_change_name_as_old_and_content'] = 'Failed Copy , Paste a File , Then Remove old File also change name of the new file as old one and changed content Unit Test ................. !'
AlgorithmTestCaseFailMessages['test_change_base_path'] = 'Failed Test Change Base Path Unit Test ................. !'
AlgorithmTestCaseFailMessages['test_intersection_of_dir'] = 'Failed Test Intersection Of Dir Unit Test ................. !'

RequiredsCreationTestCaseFailMessages['is_report_dir_exists'] = 'Failed Reports Directory Creation Unit Test ................. !'
RequiredsCreationTestCaseFailMessages['is_history_dir_exists'] = 'Failed History Directory Creation Unit Test ................. !'
RequiredsCreationTestCaseFailMessages['is_schedules_dir_exists'] = 'Failed Scheduler Directory Creation Unit Test ................. !'
RequiredsCreationTestCaseFailMessages['is_config_file_exists'] = 'Failed Configuration Directory Creation Unit Test ................. !'
RequiredsCreationTestCaseFailMessages['is_database_file_exists'] = 'Failed Database Directory Creation Unit Test ................. !'
RequiredsCreationTestCaseFailMessages['is_debug_files_exists'] = 'Failed Debug Directory Creation Unit Test ................. !'



