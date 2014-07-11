# -*- coding: UTF-8 -*-
'''
Created on July 10, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''

EmailTestCaseExpectedResult = {}
EmailTestCaseExpectedResult['testing'] = True
EmailTestCaseExpectedResult['attachment'] = True
EmailTestCaseExpectedResult['error'] = True

RequiredsCreationTestCaseExpectedResult = {}
RequiredsCreationTestCaseExpectedResult['all'] = True

ProjectTestCaseExpectedResult = {}
ProjectTestCaseExpectedResult['run_project'] = 4
ProjectTestCaseExpectedResult['delete_project'] = True
ProjectTestCaseExpectedResult['change_project_name'] = True
ProjectTestCaseExpectedResult['change_algorithm'] = False
ProjectTestCaseExpectedResult['import_project'] = True
ProjectTestCaseExpectedResult['save_project'] = True

# 0 = Confirmed
# 1 = Missing File
# 2 = Created
# 3 = Moved
# 4 = Corrupted Or Changed

ProjectTestCaseExpectedResult['filters_files'] = {0: 3, 1: 1, 2: 0, 3: 0, 4: 0}

AlgorithmTestCaseExpectedResult = {}
AlgorithmTestCaseExpectedResult['test_confirm_file'] = {0: 4, 1: 0, 2: 0, 3: 0, 4: 0}
AlgorithmTestCaseExpectedResult['test_confirm_if_inode_changed_of_file'] = {0: 4, 1: 0, 2: 0, 3: 0, 4: 0}
AlgorithmTestCaseExpectedResult['test_delete_file'] = {0: 3, 1: 1, 2: 0, 3: 0, 4: 0}
AlgorithmTestCaseExpectedResult['test_change_file'] = {0: 3, 1: 0, 2: 0, 3: 0, 4: 1}
AlgorithmTestCaseExpectedResult['test_change_file_changed_hash_and_path'] = {0: 3, 1: 0, 2: 0, 3: 0, 4: 1}
AlgorithmTestCaseExpectedResult['test_change_inode_and_hash_file'] = {0: 3, 1: 0, 2: 0, 3: 0, 4: 1}
AlgorithmTestCaseExpectedResult['test_new_file'] = {0: 4, 1: 0, 2: 1, 3: 0, 4: 0}
AlgorithmTestCaseExpectedResult['test_moved_file'] = {0: 3, 1: 0, 2: 0, 3: 1, 4: 0}
AlgorithmTestCaseExpectedResult['test_moved_file_to_new_directory'] = {0: 3, 1: 0, 2: 0, 3: 1, 4: 0}
AlgorithmTestCaseExpectedResult['test_moved_file_to_new_Directory_change_hash'] = {0: 3, 1: 0, 2: 0, 3: 0, 4: 1}
AlgorithmTestCaseExpectedResult['test_moved_file_to_new_Directory_change_name_as_old'] = {0: 3, 1: 0, 2: 0, 3: 0, 4: 1}
AlgorithmTestCaseExpectedResult['test_moved_to_new_Directory_change_name_as_old_and_content'] = {0: 3, 1: 0, 2: 0, 3: 0, 4: 1}
AlgorithmTestCaseExpectedResult['test_change_base_path'] = {0: 4, 1: 0, 2: 0, 3: 0, 4: 0}

