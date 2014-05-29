# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi

'''
import os

if os.name == 'nt':
    import win32file, win32con, win32api

import fnmatch, hashlib


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
    def Run(self, project_name,dict, dict_hash, dict_File, filters_array, verified_files, is_from_thread = False ):

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

        directories_inside_details = self.getFilesDetailInformationWithinGivenPath(r''+single_directory, Algorithm)

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
                #try:
                response = []
                response = self.verifyFiles(dict, dict_hash, dict_File, directories_inside_details_single, verified_files)

                if not response or len(response) < 1:
                        continue

                #except:
                #    self.Fixity.logger.LogException(Exception.message)
                #    pass

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

    def verifyFiles (self,dicty ,dict_hash ,dictFile ,line ,verified_files):

        try:
            ''' Check if I-Node related information Exists in the Given Directory  '''
            current_directory = dicty.get(line[2])
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        try:
            for single_verified_files in verified_files:
                if str(single_verified_files) in str(line[1]):
                    return
        except:
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






