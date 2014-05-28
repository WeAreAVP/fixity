# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi

'''
import os

if os.name == 'nt':
    import win32file, win32con, win32api

import fnmatch, hashlib

from collections import defaultdict
from Core import SharedApp
from Core import Database


class DirsHandler(object):


    def __init__(self,path, path_id, ID):
        super(DirsHandler, self).__init__()
        self.Fixity = SharedApp.SharedApp.App
        self.path = path
        self.path_id= path_id
        self.ID = ID
        self.database = Database.Database()

    def getPath(self):
        return self.path

    def getID(self):
        return self.ID

    def setPath(self):
        return self.path

    def setID(self,ID ):
        self.ID = ID

    def getPathID(self):
        return self.path_id

    def setPathID(self, path_id):
        self.path_id = path_id

    #Updating/Creating Manifest
    #With on the given directory
    #
    #@param file: project Name with path to be scanned
    #@param filters: Filters Will be applied on the given project by the user
    #@param project_name: project Name to be scanned
    #@param check_for_changes: check For Changes
    #
    #@return: removed Message if removed and count of removed file
    def Run(self, project_name):

        global verified_files

        self.database = Database.Database()
        project_core = self.Fixity.ProjectRepo.getSingleProject(project_name)

        project_detail_information = self.database.getVersionDetails(project_core.getID(), project_core.getPreviousVersion(), self.getID(), 'path like "%'+self.getPathID() + '%"', ' id DESC')
        if project_detail_information is False:
            project_detail_information = self.database.getVersionDetailsLast(project_core.getID(), self.getID(),'path like "%' + self.getPathID() + '%"')

        if len(project_detail_information) <= 0:
            project_detail_information = self.database.getVersionDetailsLast(project_core.getID(), self.getID(), 'path like "%' + self.getPathID() + '%"')

        verified_files = list()

        missing_file = ('', '')
        filters_array = {}
        try:
            filters_array = str(project_core.getFilters()).split(',')
        except:
            #print('no filters found')
            pass

        dict = defaultdict(list)
        dict_hash = defaultdict(list)
        dict_File = defaultdict(list)

        confirmed,  moved,  created,  corrupted_or_changed  = 0, 0, 0, 0
        file_changed_list = ""

        #print('writing ::: Stared Worked')
        check = 0
        old_dirs_information = {}
        if project_core.getLast_dif_paths() != 'None' and project_core.getLast_dif_paths() != '' and project_core.getLast_dif_paths() != None:
            last_dif_paths_array = str(project_core.getLast_dif_paths()).split(',')

            for last_dif_paths in last_dif_paths_array:
                single_dir_information = last_dif_paths.split('||-||')
                if single_dir_information[0] != None and single_dir_information[0] != '':
                    old_dirs_information[single_dir_information[1]] = single_dir_information[0]

        for l in project_detail_information:
            try:

                x = self.toTuple(project_detail_information[l])
                if x is not None and x:

                    path_information = str(x[1]).split('||')
                    if path_information:
                        try:
                            base_old_file_path = old_dirs_information[str(self.getPathID())]
                            this_file_path = str(self.Fixity.Configuration.CleanStringForBreaks(str(base_old_file_path)) + self.Fixity.Configuration.CleanStringForBreaks(str(path_information[1])))
                        except:
                            this_file_path = str(self.Fixity.Configuration.CleanStringForBreaks(str(self.getPath())) + self.Fixity.Configuration.CleanStringForBreaks(str(path_information[1])))
                            pass

                        # Parttren [inode:[['path With Out Code', 'Hash' ,'Boolean' ]], ..., ...]
                        dict[self.Fixity.Configuration.CleanStringForBreaks(str(x[2]))].append([this_file_path,self.Fixity.Configuration.CleanStringForBreaks(str(x[0])),False])

                        # Parttren [Hash:[['path With Out Code', 'INode' ,'Boolean' ]], ..., ...]
                        dict_hash[x[0]].append([this_file_path,  self.Fixity.Configuration.CleanStringForBreaks(str(x[2])), False])

                        # Parttren [Path:[['Hash', 'INode' ,'Boolean' ]], ..., ...]
                        dict_File[this_file_path].append([self.Fixity.Configuration.CleanStringForBreaks(str(x[0])), self.Fixity.Configuration.CleanStringForBreaks(str(x[2])), False])

            except:
                self.Fixity.logger.LogException(Exception.message)
                pass
        history_content = ''
        Algorithm = str(project_core.getAlgorithm())

        version_id = project_core.getVersion()

        #Getting all files and directory  in side "single_directory" with detail information (inode, path and file hash)
        single_directory = self.getPath()

        directories_inside_details = self.getFilesDetailInformationWithinGivenPath(r''+single_directory,Algorithm)

        for directories_inside_details_single in directories_inside_details:

            flag = True
            directories_inside_details_single = list(directories_inside_details_single)
            file_path = str(directories_inside_details_single[1]).split('||')
            path_Info = self.getPath()

            directories_inside_details_single[1] = (str(path_Info)+str(file_path[1]))
            for filter in filters_array:
                if filter != '' and directories_inside_details_single[1].find(str(filter).strip()) >= 0:
                    flag = False

            if project_core.getIgnore_hidden_file() == 1 or project_core.getIgnore_hidden_file() == '1' :

                try:
                    path_exploded = str(directories_inside_details_single[1]).split(str(os.sep))
                    lastIndexName = path_exploded[len(path_exploded) - 1]
                    if fnmatch.fnmatch(lastIndexName, '.*'):
                        flag = False
                    if self.isGivenFileHidden(directories_inside_details_single[1]):
                        flag = False
                except:
                    self.Fixity.logger.LogException(Exception.message)
                    pass

                try:
                    path_exploded = str(directories_inside_details_single[1]).split(str(os.sep))
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
                    response = self.verifyFiles(dict, dict_hash, dict_File, directories_inside_details_single)
                    if not response or len(response) < 1:
                            continue

                except:
                    self.Fixity.logger.LogException(Exception.message)
                    pass

                try:
                    file_changed_list += response[1] + "\n"
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
                    new_coded_path = str(response[0][1]).replace(single_directory, path_code+"||")
                except:
                    new_coded_path = ' '
                    self.Fixity.logger.LogException(Exception.message)
                    pass

                try:
                    version_detail_options = {}
                    version_detail_options['hashes'] = str(response[0][0])
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
                    history_content +=str(response[0][0]) + "\t" + str(response[0][1]) + "\t" + str(response[0][2]) + "\n"
                except:
                    self.Fixity.logger.LogException(Exception.message)
                    pass

        try:
            missing_file = self.checkForMissingFiles(dict_hash)
            file_changed_list += str(missing_file[0])
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

        try:
            total += missing_file[1]
        except:
            missing_file = ('', '')
            print('no missing file')
            pass

        information = {}
        information['confirmed'] = confirmed
        information['moved'] = moved
        information['created'] = created
        information['corrupted_or_changed'] = corrupted_or_changed
        information['missing_file'] = missing_file[1]
        information['content'] = file_changed_list
        information['history_content'] = history_content
        information['total'] = total



        return information

    #Verify File Changes when scanning
    #Method to verify a tuple against the dictionary
    #Input: defaultDict (from buildDict), tuple
    #Output: Message based on whether the file was good or not
    #
    #
    #@param dicty: List of all directory with inode,  hash and path information  with indexed using Inode
    #@param dict_hash: List of all directory with inode,  hash and path information with indexed using hash
    #@param dictFile: List of all directory with inode,  hash and path information
    #@param line: lsit of file to be scanned in this run
    #@param fileNamePath: File Path with file name to be scanned in this run
    #@param dctValue: Index of dict to be scanned
    #@param Algorithm: Algo set be the user for this project to be used for file formation to be stored
    #
    #@return: List - list of result of scanning occurred in this file for a single file

    def verifyFiles (self, dicty, dict_hash, dictFile, line,):
        global verified_files
        try:
            ''' Check if I-Node related information Exists in the Given Directory  '''
            current_directory = dicty.get(line[2])
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass
        #print('Verfiy File ::::: '+str(line[1]))
        '''' IF Given File Exists'''
        if os.path.isfile(line[1].decode('utf-8')):
            '''' IF SAME INODE EXISTS '''
            if current_directory is not None :

                current_directory = current_directory[0]

                ''' Check For File Hash Change '''
                isHashSame = (current_directory[1] == line[0])

                ''' Check For File Path Change '''
                isFilePathSame = (current_directory[0] == line[1])



                '''Confirmed   FileExists::YES  ||SameHashOfFile::YES  ||SameFilePath::YES ||SameI-Node::YES  '''
                if isHashSame and isFilePathSame:
                    verified_files.append(line[1])
                    return line, self.Fixity.Configuration.confirmed_file+":\t" + str(line[1])


                '''Moved   FileExists::YES  ||SameHashOfFile::YES  ||SameFilePath::NO ||SameI-Node::YES  '''
                if isHashSame and (not isFilePathSame):
                    verified_files.append(line[1])
                    verified_files.append(current_directory[0])
                    return line, self.Fixity.Configuration.move_or_renamed_file+":\t" + str(current_directory[0]) + "\t changed to\t" + str(line[1])


                '''Changed   FileExists::YES  ||SameHashOfFile::NO  ||SameFilePath::YES ||SameI-Node::YES  '''
                if (not isHashSame) and isFilePathSame:
                    verified_files.append(line[1])
                    return line, self.Fixity.Configuration.change_file+":\t" + str(line[1])

                '''Changed  FileExists::YES  #SameHashOfFile::NO  #SameFilePath::NO #SameI-Node::YES  '''
                if (not isHashSame) and (not isFilePathSame):
                    verified_files.append(line[1])
                    verified_files.append(current_directory[0])
                    return line, self.Fixity.Configuration.change_file+":\t" + str(current_directory[0]) + "\t changed to\t" + str(line[1])
            else :
                for dictionary_single in dict_hash:
                    all_information_hash_related = dict_hash[dictionary_single]
                    for single_infor_hash_related in all_information_hash_related:

                        '''Confirmed  FileExists::YES   #SameHashOfFile::YES   #SameFilePath::YES    #SameI-Node::NO  '''
                        if single_infor_hash_related[0] == line[1] and dictionary_single == line[0]:
                            verified_files.append(line[1])
                            return line, self.Fixity.Configuration.confirmed_file+":\t" + str(line[1])



                            '''Changed  FileExists::YES   #SameHashOfFile::NO   #SameFilePath::YES   #SameI-Node::NO  '''
                        elif single_infor_hash_related[0] == line[1] and dictionary_single != line[0]:
                            verified_files.append(line[1])
                            return line, self.Fixity.Configuration.change_file+":\t" + str(line[1])



                            '''New  FileExists::YES   #SameHashOfFile::YES   #SameFilePath::NO  #SameI-Node::NO  '''
                        elif single_infor_hash_related[0] != line[1] and dictionary_single == line[0]:
                            verified_files.append(line[1])
                            return line, self.Fixity.Configuration.new_file+":\t" + str(line[1])


            '''New  FileExists::YES   #SameHashOfFile::NO    #SameFilePath::NO     #SameI-Node::NO  '''
            verified_files.append(line[1])
            return line,  self.Fixity.Configuration.new_file+":\t" + str(line[1])

    #Method to convert database line into tuple
    #@param line: Information of a single File
    #
    #@return tuple: (hash, abspath, id)

    def toTuple(self, line):
        try:
            return [line['hashes'], str(line['path'].encode('utf-8')).strip(), line['inode']]
        except:
            self.Fixity.logger.LogException(Exception.message)
            return None



    #---------------------------------------------------------------------------------------------------------
    #Logic For Selection of Scheduler time In History or Depreciated Manifest Functionality                  |
    #---------------------------------------------------------------------------------------------------------
    #If Loop is Weekly ---- Time to Run On ---- Day of Loop To Run On ---- If Loop Is Monthly     |  Result
    #(day of week to                                                        (day of month to
    #run on if none 99)                                                     run on if none 99)
    #==========================================================================================================
    #==========================================================================================================
    #     99           ----    00:00:00    ----         99            ----        99              |  Daily    |
    #     1            ----    00:00:00    ----         1             ----        99              |  weekly   |
    #     99           ----    00:00:00    ----         99             ----        2              |  Monthly  |
    #----------------------------------------------------------------------------------------------------------

    #Method to create (hash, path, id) tables from file root
    #
    #@param Input: root, output (boolean), hash algorithm, QApplication
    #@param Output: list of tuples of (hash, path, id)
    #
    #@return:  List - List of scanned Directory


    def getFilesDetailInformationWithinGivenPath(self, directory_path_to_be_scanned, algorithm_used_for_this_project ):
        listOfValues = []
        fls = []
        try:
            for root, sub_folders, files in os.walk(r''+directory_path_to_be_scanned):

                for single_file in files :

                    if self.Fixity.Configuration.getOsType() == 'Windows':
                        single_file = self.specialCharacterHandler(single_file)
                    fls.append(os.path.join(root, single_file))
                    #print('Listing ::::: '+str(os.path.join(root, single_file)))
        except:
                self.Fixity.logger.LogException(Exception.message)
                pass



        try:
            for f in xrange(len(fls)):
                #print('get Details of File ::::: '+str(os.path.abspath(fls[f])))
                path_of_the_file = r''+os.path.abspath(fls[f])
                encoded_base_path = self.getPathID()
                given_path = str(path_of_the_file).replace(directory_path_to_be_scanned, encoded_base_path + '||')
                hash_of_this_file_content = self.getFilesHash(path_of_the_file, algorithm_used_for_this_project )

                if(self.Fixity.Configuration.getOsType() == 'Windows'):
                    inode = self.inodeForWin(path_of_the_file)
                else:
                    inode = self.inodeForMac(path_of_the_file)
                listOfValues.append((hash_of_this_file_content, given_path, inode))
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        return listOfValues




    #Method to handle all special characters
    #@param string_to_be_handled: String To Be Handled
    #@return:  String - Fixed characters String
    def specialCharacterHandler(self, string_to_be_handled):
        try:
            string_to_be_handled = string_to_be_handled.decode('cp1252')
        except:
            #print('specialCharacterHandler :::: cp1252 not helping')
            pass
        try:
            string_to_be_handled = string_to_be_handled.encode('utf8')
        except:
            #print('specialCharacterHandler :::: utf8')
            pass

        return string_to_be_handled





    #Checksum Generation Method.
    #Input: File Path, Algorithm.
    #Output: Hexadecimal Value Of Hashed File.
    def getFilesHash(self, file_path, algorithm):

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
                file_path = str(file_path)
                with open(file_path.decode('utf-8'), 'rb') as target:
                    for piece in iter(lambda: target.read(4096), b''):
                        if algorithm =='md5':
                            fixmd5.update(piece)
                        else:
                            fixsha256.update(piece)

                    target.close()
                    if algorithm =='md5':
                        return fixmd5.hexdigest()
                    else:
                        return fixsha256.hexdigest()



            else:

                with open(file_path, 'rb') as target:
                    for piece in iter(lambda: target.read(4096), b''):
                        if algorithm =='md5':
                            fixmd5.update(piece)
                        else:
                            fixsha256.update(piece)
                    target.close()
                    if algorithm =='md5':
                        return fixmd5.hexdigest()
                    else:
                        return fixsha256.hexdigest()
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass





    #File ID for NTFS
    #Returns the complete file ID as a single long string
    #(volume number, high index, low index)

    def inodeForMac (self, file):
        id_node = ''
        try:
            target = os.open(file,  os.O_RDWR | os.O_CREAT )
            info = os.fstat(target)
            id_node = str(info.st_ino)
            os.close(target)

            return id_node
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass
        return id_node







    #File ID for NTFS
    #Returns the complete file ID as a single long string
    #(volume number, high index, low index)

    def inodeForWin(self, file_path):

        id_node = '';
        try:
            target = open(file_path.decode('utf-8'), 'rb')
        except:
            self.Fixity.logger.LogException(Exception.message)
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






    #Check weather this file is Hidden or Not
    #@param path_of_file: Path Of File or Directory to be checked
    #@return: 0 if hidden and 2 if not in windows and in MAC true if hidden and false if not

    def isGivenFileHidden(self, path_of_file):

        if os.name == 'nt':
            if '\\' in path_of_file:
                '''Windows Condition'''
                path_of_file = repr(path_of_file).strip("'")

                attribute = win32api.GetFileAttributes(path_of_file)
                return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
            return 0
        else:
            '''linux'''
            return path_of_file.startswith('.')






    #Method to find which files are missing in the scanned directory
    #Input: defaultdict (from buildDict)
    #Output: warning messages about missing files (one long string and printing to stdout)
    #
    #@param dict: Directory of all file exists in the scanned folder
    #@param file: List of all directory with inode,  hash and path information  with indexed using Inode
    #
    #@return: removed Messgae if removed and count of removed file
    def checkForMissingFiles(self,dict):

        msg = ""
        count = 0
        global verified_files
        ''' walks through the dict and returns all False flags '''
        for keys in dict:
            for obj in dict[keys]:
                    if not obj[0] in verified_files:
                        verified_files.append(obj[0])
                        msg += "Removed Files\t" + obj[0] +"\n"
                        count = count + 1
        return msg, count