# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi

'''
import os, fnmatch

if os.name == 'nt':
    import win32file, win32con, win32api

import hashlib

from Core import SharedApp
from Core import Database

class DirsHandler(object):

    def __init__(self,path, path_id, ID):
        super(DirsHandler, self).__init__()
        self.Fixity = SharedApp.SharedApp.App

        self.path = path
        self.path_id = path_id
        self.ID = ID
        self.database = Database.Database()

    def getPath(self):

        return self.path

    def getID(self):
        return self.ID

    def setPath(self, path):
        self.path = path

    def setID(self,ID ):
        self.ID = ID

    def getPathID(self):
        return self.path_id

    def setPathID(self, path_id):
        self.path_id = path_id

    def Run(self, project_name,dict, dict_hash, dict_File, filters_array, verified_files, is_from_thread = False, is_path_change = False, mark_all_confirmed = False, scanner=None):
        """
        Updating/Creating Manifest With on the given directory

        @param project_name: project Name to be scanned
        @param dict: Directories its according to inodes
        @param dict_hash: Directories its according to Hash
        @param dict_File: Directories its according to File Path
        @param filters_array: Filters Will be applied on the given project by the user
        @param verified_files: files verified
        @param is_from_thread:
        @param is_path_change:
        @param mark_all_confirmed:
        @return: removed Message if removed and count of removed file
        """

        if is_from_thread:
            self.database = Database.Database()
        else:
            self.database = self.Fixity.Database

        project_core = self.Fixity.ProjectRepo.getSingleProject(project_name)

        file_changed_list = ""
        history_content = ''
        check, created, confirmed, moved, corrupted_or_changed = 0, 0, 0, 0, 0
        Algorithm = str(project_core.getAlgorithm())

        version_id = project_core.getVersion()

        #Getting all files and directory  in side "single_directory" with detail information (inode, path and file hash)
        single_directory = self.getPath()

        directories_inside_details = self.getFilesDetailInformationWithinGivenPath(single_directory, Algorithm, scanner)
        try:
            scanner.AddText('\n Preparing Data for scanning.')
        except:
            pass
        for directories_inside_details_single in directories_inside_details:

            flag = True
            directories_inside_details_single = list(directories_inside_details_single)

            if self.Fixity.Configuration.getOsType() == 'Windows':
                try:
                    file_path = directories_inside_details_single[1].split('||')
                except:
                    file_path = directories_inside_details_single[1].split('||')
                    pass
            else:
                file_path = directories_inside_details_single[1].split('||')

            path_Info = self.getPath()

            if self.Fixity.Configuration.getOsType() == 'Windows':
                try:
                    directories_inside_details_single[1] = path_Info + file_path[1]
                except:
                    try:
                        directories_inside_details_single[1] = path_Info.encode('utf-8') + file_path[1]
                    except:
                        try:
                            directories_inside_details_single[1] = path_Info.decode('utf-8') + file_path[1]
                        except:
                            pass
                        pass
                    pass
            else:
                directories_inside_details_single[1] = path_Info + file_path[1]

            for filter in filters_array:
                try:
                    if filter != '' and directories_inside_details_single[1].find(filter.strip()) >= 0:
                        flag = False
                except:
                    try:
                        if filter != '' and directories_inside_details_single[1].find(filter.encode('utf-8').strip()) >= 0:
                            flag = False
                    except:
                        try:
                            if filter != '' and directories_inside_details_single[1].find(filter.encode('utf-8').strip()) >= 0:
                                flag = False
                        except:
                            pass
                        pass
                    pass

            if project_core.getIgnore_hidden_file() == 1 or project_core.getIgnore_hidden_file() == '1':

                try:
                    if self.Fixity.Configuration.getOsType() == 'Windows':
                        try:
                            path_exploded = str(directories_inside_details_single[1]).split(str(os.sep))
                        except:
                            try:
                                path_exploded = directories_inside_details_single[1].split(str(os.sep))
                            except:
                                try:
                                    path_exploded = directories_inside_details_single[1].encode('utf-8').split(str(os.sep))
                                except:
                                    path_exploded = directories_inside_details_single[1].decode('utf-8').split(str(os.sep))
                                    pass
                    else:
                        path_exploded = directories_inside_details_single[1].split(str(os.sep))

                    lastIndexName = path_exploded[len(path_exploded) - 1]
                    if fnmatch.fnmatch(lastIndexName, '.*'):
                        flag = False
                    if self.isGivenFileHidden(directories_inside_details_single[1]):
                        flag = False
                except:
                    self.Fixity.logger.LogException(Exception.message)
                    pass

                try:
                    if self.Fixity.Configuration.getOsType() == 'Windows':
                        try:
                            path_exploded = str(directories_inside_details_single[1]).split(str(os.sep))
                        except:
                            try:
                                path_exploded = directories_inside_details_single[1].split(str(os.sep))
                            except:
                                try:
                                    path_exploded = directories_inside_details_single[1].encode('utf-8').split(str(os.sep))
                                except:
                                    path_exploded = directories_inside_details_single[1].decode('utf-8').split(str(os.sep))
                                    pass
                    else:
                        path_exploded = directories_inside_details_single[1].split(str(os.sep))
                    for single_directory_hidden in path_exploded:
                        if fnmatch.fnmatch(single_directory_hidden, '.*'):
                            flag = False

                        if self.isGivenFileHidden(single_directory_hidden):
                            flag = False
                except:
                    self.Fixity.logger.LogException(Exception.message)
                    pass

            if flag:
                check += 1
                try:
                    response = []

                    try:
                        scanner.AddText('Scanning File '+ str(directories_inside_details_single[1]) + "  .\n ")
                    except:
                        pass
                    response = self.verifyFiles(dict, dict_hash, dict_File, directories_inside_details_single, verified_files, single_directory, is_path_change, mark_all_confirmed)

                    if not response or len(response) < 1 or len(response) <= 0:
                        continue

                    try:
                        response[0][1]
                        response[1]
                    except:
                        continue
                except:
                     self.Fixity.logger.LogException(Exception.message)
                     pass
                try:
                    try:
                        file_changed_list += response[1] + "\n"
                    except:
                        file_changed_list += response[1].decode('utf-8') + "\n"
                        pass

                    if response[1].startswith('Confirmed'):
                        confirmed += 1
                    elif response[1].startswith('Moved'):
                        moved += 1
                    elif response[1].startswith('New'):
                        created += 1
                    else:
                        corrupted_or_changed += 1
                except:
                    self.Fixity.logger.LogException(Exception.message)
                    pass

                path_code = self.getPathID()

                try:
                    if self.Fixity.Configuration.getOsType() == 'Windows':

                        try:
                            new_coded_path = response[0][1].replace(single_directory, path_code + "||")
                        except:
                            try:
                                new_coded_path = response[0][1].replace(single_directory.encode('utf-8'), path_code + "||")
                            except:
                                new_coded_path = response[0][1].replace(single_directory.decode('utf-8'), path_code + "||")
                                pass
                            pass
                    else:
                        new_coded_path = response[0][1].replace(single_directory, path_code+"||")
                except:
                    new_coded_path = ' '
                    self.Fixity.logger.LogException(Exception.message)
                    pass

                try:
                    version_detail_options = {}
                    if self.Fixity.Configuration.getOsType() == 'Windows':
                        version_detail_options['hashes'] = str(response[0][0])
                    else:
                        version_detail_options['hashes'] = response[0][0]
                    version_detail_options['path'] = ''
                    if self.Fixity.Configuration.getOsType() == 'Windows':
                        version_detail_options['path'] = new_coded_path
                    else:
                        version_detail_options['path'] = new_coded_path

                    version_detail_options['inode'] = str(response[0][2])
                    version_detail_options['versionID'] = str(version_id)
                    version_detail_options['projectID'] = project_core.getID()
                    version_detail_options['projectPathID'] = self.getID()

                    self.database.insert(self.database._tableVersionDetail, version_detail_options)
                except:
                    self.Fixity.logger.LogException(Exception.message)
                    pass

                try:
                    history_content += response[0][0] + "\t" + response[0][1] + "\t" + response[0][2] + "\n"
                except:
                    self.Fixity.logger.LogException(Exception.message)
                    pass

        information_to_update = {}
        information_to_update['versionCurrentID'] = version_id
        self.database.update(self.database._tableProject, information_to_update, " id= '" + str(project_core.getID()) + "'")

        total = confirmed
        total += moved
        total += created
        total += corrupted_or_changed

        information = {}

        information['confirmed'] = confirmed
        information['moved'] = moved
        information['created'] = created
        information['corrupted_or_changed'] = corrupted_or_changed

        information['content'] = file_changed_list
        information['history_content'] = history_content
        information['total'] = total
        information['verified_files'] = verified_files

        return information

    def verifyFiles(self, dicty ,dict_hash ,dictFile ,line ,verified_files, single_directory, is_path_change = False, mark_all_confirmed = False):
        """

        Verify File Changes when scanning
        Method to verify a tuple against the dictionary
        Input: defaultDict (from buildDict), tuple
        Output: Message based on whether the file was good or not

        @param dicty: List of all directory with inode,  hash and path information  with indexed using Inode
        @param dict_hash: List of all directory with inode,  hash and path information with indexed using hash
        @param dictFile: List of all directory with inode,  hash and path information
        @param line: lsit of file to be scanned in this run
        @param fileNamePath: File Path with file name to be scanned in this run
        @param dctValue: Index of dict to be scanned
        @param Algorithm: Algo set be the user for this project to be used for file formation to be stored

        @return: List - list of result of scanning occurred in this file for a single file
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        try:
            ''' Check if I-Node related information Exists in the Given Directory  '''
            current_directory = dicty.get(line[2])
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass
        try:
            for single_verified_files in verified_files:
                if verified_files[single_verified_files] in line[1]:
                    return
        except:
            pass

        if self.Fixity.Configuration.getOsType() == 'Windows':
            try:
                path_info = os.path.isfile(line[1])
            except:
                try:
                    path_info = os.path.isfile(line[1].decode('utf-8'))
                except:
                    try:
                        path_info = os.path.isfile(line[1].encode('utf-8'))
                    except:
                        pass
                    pass
        else:
            path_info = os.path.isfile(line[1])

        '''' IF Given File Exists'''
        if path_info:
            '''' IF SAME INODE EXISTS '''
            if current_directory is not None:
                current_directory = current_directory[0]

                ''' Check For File Hash Change '''
                is_hash_same = (current_directory[1] == line[0])
                is_file_path_same = False

                if is_path_change:
                    try:
                        new_file_path = line[1].replace(single_directory, '')
                    except:
                        try:
                            new_file_path = line[1].replace(single_directory.encode('utf-8'), '')
                        except:
                            new_file_path = line[1].replace(single_directory.decode('utf-8'), '')
                        pass
                    old_file_path = current_directory[0].replace(current_directory[3], '')

                    try:
                        is_file_path_same = old_file_path == new_file_path
                    except:
                        try:
                            is_file_path_same = old_file_path.encode('utf-8') == new_file_path
                        except:
                            is_file_path_same = old_file_path.decode('utf-8') == new_file_path
                            pass
                        pass
                else:
                    try:
                        is_file_path_same = (current_directory[0] == line[1])
                    except:
                        try:
                            is_file_path_same = (current_directory[0].encode("utf-8") == line[1])
                        except:

                            is_file_path_same = (current_directory[0].decode('utf-8') == line[1])
                            pass
                        pass

                '''Confirmed   FileExists::YES  ||SameHashOfFile::YES  ||SameFilePath::YES ||SameI-Node::YES  '''
                if (is_hash_same and is_file_path_same) or mark_all_confirmed:
                    verified_files.append(line[1])
                    verified_files.append(current_directory[0])
                    try:
                        return line, self.Fixity.Configuration.confirmed_file + ":\t" + line[1]
                    except:
                        try:
                            return line, self.Fixity.Configuration.confirmed_file + ":\t" + line[1].decode('utf-8')
                        except:
                            try:
                                return line, self.Fixity.Configuration.confirmed_file + ":\t" + line[1].encode('utf-8')
                            except:
                                pass
                            pass
                        pass

                '''Moved   FileExists::YES  ||SameHashOfFile::YES  ||SameFilePath::NO ||SameI-Node::YES  '''
                if is_hash_same and (not is_file_path_same):

                    verified_files.append(line[1])
                    saved_path_info = dictFile[current_directory[0]]
                    dir_path_info = dictFile[line[1]]
                    try:
                        if dir_path_info[0][1] == saved_path_info[0][1]:
                            verified_files.append(current_directory[0])
                    except:
                        verified_files.append(current_directory[0])
                        pass

                    try:
                        return line, self.Fixity.Configuration.move_or_renamed_file + ":\t" + current_directory[0] + "\t changed to\t" + line[1]
                    except:
                        try:
                            return line, self.Fixity.Configuration.move_or_renamed_file + ":\t" + current_directory[0] + "\t changed to\t" + line[1].encode('utf-8')
                        except:

                            return line, self.Fixity.Configuration.move_or_renamed_file + ":\t" + current_directory[0] + "\t changed to\t" + line[1].decode('utf-8')

                            pass
                        pass

                '''Changed   FileExists::YES  ||SameHashOfFile::NO  ||SameFilePath::YES ||SameI-Node::YES  '''
                if (not is_hash_same) and is_file_path_same:

                    verified_files.append(line[1])

                    try:
                        return line, self.Fixity.Configuration.change_file+":\t" + line[1]
                    except:
                        try:
                            return line, self.Fixity.Configuration.change_file+":\t" + line[1].encode('utf-8')
                        except:

                            return line, self.Fixity.Configuration.change_file+":\t" + line[1].decode('utf-8')

                        pass

                '''Changed  FileExists::YES  #SameHashOfFile::NO  #SameFilePath::NO #SameI-Node::YES  '''
                if (not is_hash_same) and (not is_file_path_same):

                    verified_files.append(line[1])
                    verified_files.append(current_directory[0])
                    try:

                        return line, self.Fixity.Configuration.change_file+":\t" + (current_directory[0]) + "\t changed to\t" + line[1].encode('utf-8')
                    except:
                        try:
                            return line, self.Fixity.Configuration.change_file+":\t" + (current_directory[0].encode("utf-8")) + "\t changed to\t" + line[1].encode("utf-8")
                        except:
                            return line, self.Fixity.Configuration.change_file+":\t" + (current_directory[0].decode("utf-8")) + "\t changed to\t" + line[1].decode('utf-8')
                            pass
                        pass

            else:

                for dictionary_single in dict_hash:

                    all_information_hash_related = dict_hash[dictionary_single]
                    is_same_file_path = False
                    new_file_path = ''
                    old_file_path = ''
                    for single_infor_hash_related in all_information_hash_related:

                        if is_path_change:
                            try:
                                new_file_path = line[1].replace(single_directory, '')
                            except:
                                try:
                                    new_file_path = line[1].replace(single_directory.encode('utf-8'), '')
                                except:
                                    try:
                                        new_file_path = line[1].replace(single_directory.decode('utf-8'), '')
                                    except:
                                        pass
                                    pass
                                pass

                            old_file_path = single_infor_hash_related[0].replace(single_infor_hash_related[3], '')

                            try:
                                is_same_file_path = old_file_path == new_file_path
                            except:
                                try:
                                    is_same_file_path = old_file_path.encode('utf-8') == new_file_path
                                except:
                                    try:
                                        is_same_file_path = old_file_path.decode('utf-8') == new_file_path
                                    except:
                                        pass
                                    pass
                                pass
                        else:
                            try:
                                is_same_file_path = single_infor_hash_related[0] == line[1]
                            except:
                                try:
                                    is_same_file_path = single_infor_hash_related[0].encode('utf-8') == line[1]
                                except:
                                    pass
                                pass
                        if is_same_file_path:
                            break

                    ''' Confirmed  FileExists::YES #SameHashOfFile::YES #SameFilePath::YES #SameI-Node::NO  '''
                    if (is_same_file_path and dictionary_single == line[0]) or mark_all_confirmed:

                        verified_files.append(line[1])
                        verified_files.append(single_infor_hash_related[0])
                        try:
                            return line, self.Fixity.Configuration.confirmed_file + ":\t" + line[1]
                        except:
                            try:
                                return line, self.Fixity.Configuration.confirmed_file + ":\t" + line[1].decode('utf-8')
                            except:
                                return line, self.Fixity.Configuration.confirmed_file + ":\t" + line[1].encode('utf-8')
                            pass

                        ''' Changed  FileExists::YES   #SameHashOfFile::NO   #SameFilePath::YES   #SameI-Node::NO '''
                    elif is_same_file_path and dictionary_single != line[0]:

                        verified_files.append(line[1])
                        verified_files.append(single_infor_hash_related[0])
                        try:
                            return line, self.Fixity.Configuration.change_file + ":\t" + line[1]
                        except:
                            try:
                                return line, self.Fixity.Configuration.change_file + ":\t" + line[1].decode('utf-8')
                            except:
                                return line, self.Fixity.Configuration.change_file + ":\t" + line[1].encode('utf-8')
                                pass
                            pass

                        ''' New  File Exists::YES   #SameHashOfFile::YES   #SameFilePath::NO  #SameI-Node::NO '''
                    elif (not is_same_file_path) and dictionary_single == line[0]:

                        verified_files.append(line[1])
                        try:
                            return line, self.Fixity.Configuration.new_file + ":\t" + line[1]
                        except:
                            try:
                                return line, self.Fixity.Configuration.new_file + ":\t" + line[1].decode('utf-8')
                            except:
                                return line, self.Fixity.Configuration.new_file + ":\t" + line[1].encode('utf-8')
                            pass

            '''New  FileExists::YES   #SameHashOfFile::NO    #SameFilePath::NO     #SameI-Node::NO  '''

            verified_files.append(line[1])
            try:
                return line, self.Fixity.Configuration.new_file + ":\t" + line[1]
            except:
                try:
                    return line, self.Fixity.Configuration.new_file + ":\t" + line[1].decode('utf-8')
                except:
                    return line, self.Fixity.Configuration.new_file + ":\t" + line[1].encode('utf-8')
                pass

    def getFilesDetailInformationWithinGivenPath(self, directory_path_to_be_scanned, algorithm_used_for_this_project ,scanner=None):
        """
        ------------------------------------------------------------------------------- --------------------------
        Logic For Selection of Scheduler time In History or Depreciated Manifest  Functi onality                  |
        ------------------------------------------------------------------------------- --------------------------|
        If Loop is Weekly ---- Time to Run On ---- Day of Loop To Run On ---- If Loop Is Monthly      |  Result   |
        (day of week to                                                         (day of month to      |           |
        run on if none 99)                                                      run on if none 99)    |           |
        ================================================================================ =========================|
        ================================================================================ =========================|
             99           ----    00:00:00    ----         99            ----        99               |  Daily    |
             1            ----    00:00:00    ----         1             ----        99               |  weekly   |
             99           ----    00:00:00    ----         99             ----        2               |  Monthly  |
        ----------------------------------------------------------------------------------------------------------

        Method to create (hash, path, id) tables from file root

        @param Input: root, output (boolean), hash algorithm, QApplication
        @param Output: list of tuples of (hash, path, id)

        @return:  List - List of scanned Directory
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        list_of_values = []
        fls = []
        try:
            scanner.AddText('Getting Directories Details .')
        except:
            pass
        try:
            for root, sub_folders, files in os.walk(directory_path_to_be_scanned):
                for single_file in files:
                    try:
                        scanner.AddText(single_file + '.' + "\n")
                    except:
                        pass

                    if self.Fixity.Configuration.getOsType() == 'Windows':
                        try:
                            fls.append(root + str(os.sep) + single_file)
                        except:
                            try:
                                single_file = self.specialCharacterHandler(single_file)
                                root = self.specialCharacterHandler(root)
                                fls.append(root + str(os.sep) + single_file)
                            except:
                                fls.append(root + str(os.sep) + single_file)
                                pass
                            pass

                    else:
                        fls.append(root + str(os.sep) + single_file)

        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        try:
            scanner.AddText('\nListing Files .')
        except:
            pass

        try:
            for f in xrange(len(fls)):
                path_of_the_file = fls[f]

                encoded_base_path = self.getPathID()
                try:
                    scanner.AddText(path_of_the_file + '.' + "\n")
                except:
                    pass
                if self.Fixity.Configuration.getOsType() == 'Windows':
                    try:
                        given_path = path_of_the_file. replace(directory_path_to_be_scanned, encoded_base_path + '||')
                    except:
                        try:
                            given_path = path_of_the_file. replace(directory_path_to_be_scanned.decode('utf-8'), encoded_base_path.encode('utf-8') + '||')
                        except:
                            try:
                                given_path = path_of_the_file. replace(directory_path_to_be_scanned.encode('utf-8'), encoded_base_path.encode('utf-8') + '||')
                            except:
                                pass
                            pass
                        pass
                else:
                    given_path = path_of_the_file.replace(directory_path_to_be_scanned, encoded_base_path + '||')

                hash_of_this_file_content = self.getFilesHash(path_of_the_file, algorithm_used_for_this_project)

                if self.Fixity.Configuration.getOsType() == 'Windows':
                    inode = self.inodeForWin(path_of_the_file)
                else:
                    inode = self.inodeForMac(path_of_the_file)
                if self.Fixity.Configuration.getOsType() == 'Windows':
                    list_of_values.append((hash_of_this_file_content, given_path, inode))
                else:
                    list_of_values.append((hash_of_this_file_content, given_path, inode))
        except:
             self.Fixity.logger.LogException(Exception.message)
             pass

        return list_of_values

    def specialCharacterHandler(self, string_to_be_handled):
        """
        Method to handle all special characters

        @param string_to_be_handled: String To Be Handled

        @return:  String - Fixed characters String
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass
        try:
            string_to_be_handled = string_to_be_handled.decode('cp1252')
        except:
            pass

        try:
            string_to_be_handled = string_to_be_handled.encode('utf8')
        except:
            pass

        return string_to_be_handled

    def getFilesHash(self, file_path, algorithm):
        """
        Checksum Generation Method.
        Input: File Path, Algorithm.
        Output: Hexadecimal Value Of Hashed File.

        @param file_path: File Path
        @param algorithm: Algorithm Selected

        @return: None
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass
        try:
            if algorithm =='md5':
                fixmd5 = hashlib.md5()
            else:
                fixsha256 = hashlib.sha256()

        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        try:
            if self.Fixity.Configuration.getOsType() == 'Windows':
                try:
                    with open(file_path.decode('utf-8'), 'rb') as target:
                        for piece in iter(lambda: target.read(4096), b''):
                            if algorithm == 'md5':
                                fixmd5.update(piece)
                            else:
                                fixsha256.update(piece)

                        target.close()
                        if algorithm == 'md5':
                            return fixmd5.hexdigest()
                        else:
                            return fixsha256.hexdigest()
                except:
                    with open(file_path, 'rb') as target:
                        for piece in iter(lambda: target.read(4096), b''):
                            if algorithm == 'md5':
                                fixmd5.update(piece)
                            else:
                                fixsha256.update(piece)

                        target.close()
                        if algorithm == 'md5':
                            return fixmd5.hexdigest()
                        else:
                            return fixsha256.hexdigest()

            else:

                with open(file_path, 'rb') as target:
                    for piece in iter(lambda: target.read(4096), b''):
                        if algorithm == 'md5':
                            fixmd5.update(piece)
                        else:
                            fixsha256.update(piece)
                    target.close()
                    if algorithm == 'md5':
                        return fixmd5.hexdigest()
                    else:
                        return fixsha256.hexdigest()
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

    def inodeForMac(self, file):
        """
        File ID for NTFS
        Returns the complete file ID as a single long string
        (volume number, high index, low index)
        @param file:

        @return: None
        """

        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        id_node = ''

        try:
            try:

                target = os.open(file, os.O_RDWR | os.O_CREAT )
            except:
                try:
                    target = os.open(file, os.O_RDONLY)
                except:
                    try:
                        target = os.open(file.decode('utf-8'), os.O_RDONLY)
                    except:
                        try:
                            target = os.open(file.encode('utf-8'), os.O_RDONLY)
                        except:
                            pass
                        pass
                    pass
                pass

            info = os.fstat(target)
            id_node = str(info.st_ino)
            os.close(target)

            return id_node
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass
        return id_node

    def inodeForWin(self, file_path):
        """
        File ID for NTFS
        Returns the complete file ID as a single long string
        (volume number, high index, low index)

        @param file_path: File Path

        @return:
        """

        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        id_node = ''

        try:
            target = open(file_path, 'rb')
        except:
            try:
                target = open(file_path.decode('utf-8'), 'rb')
            except:
                self.Fixity.logger.LogException(Exception.message)
                pass
            pass

        try:
            id_node = str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[4]) + \
                str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[8]) + \
                str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[9])
            return id_node
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        return id_node

    def isGivenFileHidden(self, path_of_file):
        """
        Check weather this file is Hidden or Not

        @param path_of_file: Path Of File or Directory to be checked

        @return: 0 if hidden and 2 if not in windows and in MAC true if hidden and false if not

        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass
        if os.name == 'nt':
            if '\\' in path_of_file:
                '''Windows Condition'''
                try:
                    path_of_file = path_of_file.strip("'")
                except:
                    try:
                        path_of_file = path_of_file.encode('utf-8').strip("'")
                    except:
                        path_of_file = path_of_file.decode('utf-8').strip("'")
                        pass
                    pass

                attribute = win32api.GetFileAttributes(path_of_file)
                return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
            return 0
        else:
            '''linux'''
            return path_of_file.startswith('.')