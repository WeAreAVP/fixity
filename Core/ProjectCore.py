#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#@author: Furqan Wasi <furqan@avpreserve.com>

from Core import DirsHandler
from Core import SharedApp, SchedulerCore, EmailNotification, Database, DatabaseLockHandler
import datetime
import re
import os
import threading
import time
from collections import defaultdict

global verified_files


class ProjectCore(object):


    def __init__(self):
        super(ProjectCore, self).__init__()
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        self.ID = ''
        self.title = ''
        self.version = {}
        self.ignore_hidden_file = False
        self.directories = {}
        self.scheduler = SchedulerCore.SchedulerCore()
        self.algorithm = 'sha256'
        self.filters = None
        self.project_ran_before = None
        self.last_dif_paths = None
        self.email_address = None
        self.extra_conf = None
        self.last_ran = None
        self.updated_at = None
        self.created_at = None
        self.previous_version = None
        self.is_inserted = False
        self.is_saved = False

    def setDirectories(self, directories):
        try: self.Fixity = SharedApp.SharedApp.App
        except:pass

        for n in directories:
            try:self.directories[(n)] = DirsHandler.DirsHandler(directories[n]['path'], directories[n]['pathID'], directories[n]['id'])
            except:
                self.directories[(n)] = DirsHandler.DirsHandler(directories[n]['path'], directories[n]['pathID'], '')
                pass

    def setID(self, ID): self.ID = ID

    def getID(self ):return self.ID

    def setTitle(self, title):self.title = title

    def getTitle(self ):return self.title

    def setVersion(self, version):self.version = version

    def getVersion(self ):return self.version

    def setIgnore_hidden_file(self, ignore_hidden_file):self.ignore_hidden_file = ignore_hidden_file

    def getIgnore_hidden_file(self ):return self.ignore_hidden_file

    def getDirectories(self ):return self.directories

    def setFilters(self, filters): self.filters = filters

    def getScheduler(self):return self.scheduler

    def setAlgorithm(self, algorithm):self.algorithm = algorithm

    def getAlgorithm(self ):return self.algorithm

    def getFilters(self ):
        if self.filters: return self.filters
        else:return ''

    def setProject_ran_before(self, project_ran_before):self.project_ran_before = project_ran_before

    def getProject_ran_before(self ):return self.project_ran_before

    def setLast_dif_paths(self, last_dif_paths):self.last_dif_paths = last_dif_paths

    def getLast_dif_paths(self ):return self.last_dif_paths

    def setEmail_address(self, email_address):self.email_address = email_address

    def getEmail_address(self):return self.email_address

    def setExtra_conf(self, extra_conf):self.extra_conf = extra_conf

    def getExtra_conf(self):return self.extra_conf

    def setLast_ran(self, last_ran):self.last_ran = last_ran

    def getLast_ran(self):return self.last_ran

    def setUpdated_at(self, updated_at):self.updated_at = updated_at

    def getUpdated_at(self):return self.updated_at

    def setCreated_at(self, created_at):self.created_at = created_at

    def getCreated_at(self):return self.created_at

    def getPreviousVersion(self): return self.previous_version

    def setPreviousVersion(self, previous_version): self.previous_version = previous_version

    def createNewVersion(self, project_id, version_type):

        """
        Creates New Version

        @param project_id: Project ID
        @param version_type: Version is created For

        @return Version ID Created
        """

        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        get_old_version = self.Fixity.Database.select(self.Fixity.Database._tableVersions, '*', 'projectID="'+ str(project_id) + '"', 'versionID DESC ')

        version_id = 1
        if get_old_version is not None and get_old_version is not False:
            if len(get_old_version) > 0:
                version_id = int(get_old_version[0]['versionID'])
                version_id += 1

        information = {}
        current_date = str(datetime.datetime.now()).split('.')
        information['projectID'] = project_id
        information['versionID'] = version_id
        information['name'] = self.Fixity.Configuration.EncodeInfo(str(current_date[0]))
        information['versionType'] = version_type
        information['updatedAt'] = self.Fixity.Configuration.getCurrentTime()
        information['createdAt'] = self.Fixity.Configuration.getCurrentTime()

        return self.Fixity.Database.insert(self.Fixity.Database._tableVersions, information)

    def Save(self, save_schedule = True, came_from = False):

        """
        Save Project

        @return Project ID Created
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        project_information = {}

        project_information['title'] = self.getTitle()
        project_information['ignoreHiddenFiles'] = self.getIgnore_hidden_file()

        project_information['selectedAlgo'] = self.getAlgorithm()
        project_information['filters'] = self.getFilters()
        project_information['durationType'] = self.scheduler.getDurationType()
        project_information['runTime'] = self.scheduler.getRunTime()
        project_information['runDayOrMonth'] = self.scheduler.getRun_day_or_month()
        project_information['runWhenOnBattery'] = self.scheduler.getRun_when_on_battery()
        project_information['ifMissedRunUponRestart'] = self.scheduler.getIf_missed_run_upon_restart()
        project_information['emailOnlyUponWarning'] = self.scheduler.getEmail_only_upon_warning()

        project_information['emailAddress'] = self.getEmail_address()
        project_information['extraConf'] = self.getExtra_conf()
        project_information['lastRan'] = self.getLast_ran()

        project_information['updatedAt'] = self.Fixity.Configuration.getCurrentTime()

        project_id = {}
        project_exists = self.Fixity.Database.select(self.Fixity.Database._tableProject,'*',
                                                     'title like "' + str(self.getTitle()) + '"')
        if len(project_exists) <= 0:
            # Insert Project
            project_information['createdAt'] = self.Fixity.Configuration.getCurrentTime()
            project_id = self.Fixity.Database.insert(self.Fixity.Database._tableProject, project_information)
            self.setPreviousVersion('')
        else:
            # Update Project
            project_information['updatedAt'] = self.Fixity.Configuration.getCurrentTime()
            self.Fixity.Database.update(self.Fixity.Database._tableProject, project_information,
                                        'id ="' + str(project_exists[0]['id']) + '"')
            project_id['id'] = project_exists[0]['id']
            self.setID(project_id['id'])
            self.setPreviousVersion(project_exists[0]['versionCurrentID'])

        self.setID(project_id['id'])
        version_id = self.createNewVersion(project_id['id'], 'project')

        try:
            self.setVersion(version_id['id'])
        except:
            pass

        try:
            # Update version
            update_version = {}
            update_version['versionCurrentID'] = version_id['id']
            self.setVersion(update_version['versionCurrentID'])
        except:
             pass

        for dirs_objects in self.directories:
            dir_information = {}
            dir_information['path'] = self.directories[dirs_objects].getPath()
            dir_information['pathID'] = self.directories[dirs_objects].getPathID()
            dir_information['projectID'] = project_id['id']
            dir_information['versionID'] = version_id['id']
            dir_information['updatedAt'] = self.Fixity.Configuration.getCurrentTime()
            dir_information['createdAt'] = self.Fixity.Configuration.getCurrentTime()

            dir_path_id = self.Fixity.Database.insert(self.Fixity.Database._tableProjectPath, dir_information)

            self.directories[dirs_objects].setID(dir_path_id['id'])

        self.Fixity.Database.update(self.Fixity.Database._tableProject, update_version, 'id ="' + str(project_id['id']) + '"')

        if save_schedule:
            response = self.SaveSchedule()
            if came_from:
                if project_id['id']:
                    self.Fixity.ProjectsList[self.getTitle()] = self
                    SharedApp.SharedApp.App = self.Fixity

                return response

        if project_id['id']:
            self.Fixity.ProjectsList[self.getTitle()] = self

        SharedApp.SharedApp.App = self.Fixity
        return project_id['id']

    def Delete(self):

        """
        Delete this project

        @return Bool
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        self.scheduler.delTask(self.getTitle())
        self.Fixity.Database.delete(self.Fixity.Database._tableProjectPath, 'projectID="' + str(self.getID()) + '"')
        self.Fixity.Database.delete(self.Fixity.Database._tableVersionDetail, 'projectID="' + str(self.getID()) + '"')
        self.Fixity.Database.delete(self.Fixity.Database._tableProject, 'id ="' + str(self.getID()) + '"')

        self.Fixity.removeProject(str(self.getTitle()))
        return True

    def ImportProject(self, file_path, project_name, flag_is_a_tsv_file, flag_is_a_fxy_file):
        """

        Import New project
        @param file_path: file Path of imported File
        @param project_name: Project Name
        @param flag_is_a_tsv_file: is File .tsv
        @param flag_is_a_fxy_file: is File .fxy

        @return Bool
        """

        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        flag_project_contain_detail = False
        file_to_import_info_of = open(file_path,'rb')

        project_paths = file_to_import_info_of.readline()

        email_address = str(file_to_import_info_of.readline())

        project_configuration = str(file_to_import_info_of.readline())
        last_ran = str(file_to_import_info_of.readline())
        filters = {}
        algorithm_selected = ''
        if flag_is_a_tsv_file:
            filters  = str(self.Fixity.Configuration.CleanStringForBreaks(file_to_import_info_of.readline()))
            algorithm_selected = str(self.Fixity.Configuration.CleanStringForBreaks(file_to_import_info_of.readline()))
            filters = filters.split('||-||')
        all_content = file_to_import_info_of.readlines()

        if project_paths and project_configuration:
            try:
                config = {}
                run_say_or_month = ''
                duration_type = 0

                config['title'] = str(project_name)

                information = project_configuration.split(' ')

                is_month, is_week = 99, 99
                run_time = str(information[1])
                is_week = information[2]
                is_month = str(self.Fixity.Configuration.CleanStringForBreaks(information[3]))

                # 0 = Monthly, 1 = Weekly, 2 = Daily
                if int(is_month) == 99 and int(is_week) == 99:
                    duration_type = 3
                    run_say_or_month = '-'
                elif int(is_month) == 99 and int(is_week) != 99:
                    duration_type = 2
                    run_say_or_month = is_week
                elif int(is_month) != 99 and int(is_week) == 99:
                    duration_type = 1
                    run_say_or_month = is_month

                if algorithm_selected == '' or algorithm_selected is None:
                    algorithm_selected = self.checkForAlgoUsed(all_content)

                if algorithm_selected == '' or algorithm_selected is None:
                    algorithm_selected = 'sha256'

                config['lastRan'] = str(last_ran)

                if flag_is_a_tsv_file:
                    config['filters'] = filters[0]
                    config['ignoreHiddenFiles'] = filters[1]
                    config['selectedAlgo'] = algorithm_selected
                else:
                    config['filters'] = ''
                    config['ignoreHiddenFiles'] = 0
                    config['selectedAlgo'] = algorithm_selected

                config['runTime'] = run_time
                config['durationType'] = duration_type
                config['runDayOrMonth'] = run_say_or_month
                config['emailOnlyUponWarning'] = 0
                config['ifMissedRunUponRestart'] = 0
                config['emailOnlyUponWarning'] = 0
                config['runWhenOnBattery'] = 1
                config['extraConf'] = ''
                config['lastDifPaths'] = ''
                config['projectRanBefore'] = 0
                config['emailAddress'] = self.Fixity.Configuration.CleanStringForBreaks(str(email_address).replace(';',''))

                project_id = self.Fixity.Database.insert(self.Fixity.Database._tableProject, config)
                version_id = self.createNewVersion(project_id['id'], 'project')
                config['versionCurrentID'] = version_id['id']
                information_project_update = {}
                information_project_update['versionCurrentID'] = version_id['id']

                self.Fixity.Database.update(self.Fixity.Database._tableProject,
                                            information_project_update,'id = "' + str(project_id['id']) +'"')

                all_project_paths = []
                path_info = project_paths.split(';')

                if '|-|-|' in file_to_import_info_of:
                    for single_path in path_info:
                        single_path_detail = single_path.split('|-|-|')

                        if len(single_path_detail) > 1:
                            listing = []
                            listing.append(single_path_detail[0])
                            listing.append(single_path_detail[1])
                            all_project_paths.append(listing)
                else:
                    counter = 1
                    for single_path in path_info:
                        if single_path != '' and single_path is not None:
                            listing = []
                            listing.append(single_path)
                            listing.append('Fixity-'+str(counter))
                            all_project_paths.append(listing)
                            counter += 1

                if project_id:
                    for inform_path in all_project_paths:

                        information_project_path = {}
                        information_project_path['projectID'] = project_id['id']
                        information_project_path['versionID'] = version_id['id']
                        information_project_path['path'] = inform_path[0]
                        information_project_path['pathID'] = inform_path[1]

                        self.Fixity.Database.insert(self.Fixity.Database._tableProjectPath, information_project_path)

                self.setID(project_id['id'])
                self.setProjectInfo(config)
                self.setVersion(information_project_update['versionCurrentID'])

                if project_id and len(all_content) > 0:
                    flag_project_contain_detail = True

                    for single_content in all_content:
                        fix_info = re.split(r'\t+', single_content)

                        if fix_info is not None:
                            if len(fix_info) > 2:
                                if len(fix_info[0]) == 32:
                                    hashes = fix_info[0]
                                else:
                                    hashes = fix_info[0]
                                information_of_path_id = {}
                                if '||' in fix_info[1]:
                                    information_of_path_id = fix_info[1].split('||')
                                else:
                                    for inform_path in all_project_paths:
                                        if inform_path[0] in fix_info[1]:
                                            information_of_path_id[0] = inform_path[1]
                                            fix_info[1] = fix_info[1].replace(inform_path[0], inform_path[1] + '||')

                                information_version_detail = {}
                                information_version_detail['projectID'] = project_id['id']
                                information_version_detail['versionID'] = version_id['id']
                                information_version_detail['projectPathID'] = information_of_path_id[0]
                                information_version_detail['hashes'] = self.Fixity.Configuration.CleanStringForBreaks(hashes)
                                information_version_detail['path'] = self.Fixity.Configuration.CleanStringForBreaks(fix_info[1])
                                information_version_detail['inode'] = self.Fixity.Configuration.CleanStringForBreaks(fix_info[2])
                                self.Fixity.Database.insert(self.Fixity.Database._tableVersionDetail, information_version_detail)

                if flag_project_contain_detail:
                    if project_id:
                        information_to_upate = {}
                        information_to_upate['projectRanBefore'] = 1
                        self.setProject_ran_before('1')
                        self.Fixity.Database.update(self.Fixity.Database._tableProject, information_to_upate,
                                                    "id='" + str(project_id['id']) + "'")
                self.Fixity.ProjectsList[self.getTitle()] = self
                try:
                    file_to_import_info_of.close()
                except:
                    pass
                return True
            except:
                self.Fixity.logger.LogException(Exception.message)
                return False
                pass

    def checkForAlgoUsed(self,content):
        """

        Check For Algorithm Used
        @param content: Content line containing Algorithm

        @return: Algorithm Used
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass
        algo = 'sha256'
        for single_content in content:
            fix_info = re.split(r'\t+', single_content)
            if fix_info is not None:
                if len(fix_info) > 2:
                    if len(str(fix_info[0])) == 32:
                        algo = 'md5'
                    else:
                        algo = 'sha256'
                    return algo
        return algo

    def ChangeTitle(self, new_title):
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass
        information = {}
        information['title'] = new_title
        self.Fixity.Database.update(self.Fixity.Database._tableProject,
                                    information, 'id="' + str(self.getID()) + '"')
        return False

    def changeProjectName(self, selected_project, new_name):
        """
        Change Project Name logic

        @param selected_project:string project name to be changed
        @param new_name:string project name changed with
        """
        try:
            project_exists = self.Fixity.ProjectsList[str(new_name)]
            project_exists.getID()
            project_exists.getTitle()
            return False
        except:
            pass

        is_project_name_valid = self.Fixity.Validation.ValidateProjectName(new_name)
        if is_project_name_valid is False:
            return is_project_name_valid

        self.ChangeTitle(new_name)
        self.setTitle(new_name)

        self.scheduler.delTask(selected_project)
        schedule_update = 1
        schedule_update = self.scheduler.schedule(new_name)

        self.Fixity.ProjectsList[new_name] = self
        self.Fixity.removeProject(selected_project)
        SharedApp.SharedApp.App = self.Fixity
        return schedule_update

    def launchThread(self, scanner):

        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        self.Fixity = SharedApp.SharedApp.App
        self.Fixity.Database = Database.Database()
        if self.Fixity.Configuration.getOsType() == 'Windows':
            t1 = threading.Thread(target=self.Run, args= (False, True, False, 'CLI', scanner))
            t1.start()
        else:
            self.Run(False, True, False, 'CLI', scanner)
            try:
                print('\nScanning Completed. \n')
            except:
                pass

            time.sleep(6)

            try:
                print('\nClosing Console. \n')
            except:
                pass

            time.sleep(2)
            scanner.Cancel()
        # run_thread = thread.start_new_thread(self.launchRun, tuple())
        # self.Fixity.queue[len(self.Fixity.queue)] = run_thread

    def launchRun(self):

        self.Fixity = SharedApp.SharedApp.App
        self.Fixity.Database = Database.Database()
        self.Run(False, True)

    def Run(self, check_for_changes=False, is_from_thread = False, mark_all_confirmed=False, called_from='CLI', scanner=None):
        """
        Run This project
        @param check_for_changes: if only want to know is all file confirmed or not

        @return array
        """
        start_time = datetime.datetime.now()


        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        self.Fixity.Database = Database.Database()

        if is_from_thread:
            self.database = Database.Database()
        else:
            self.database = self.Fixity.Database
        time.sleep(1.5)
        missing_file = ('', '')
        global verified_files
        verified_files = list()
        report_content = ''
        history_content = ''

        confirmed = 0
        moved = 0
        created = 0
        corrupted_or_changed = 0
        missing_file = 0
        total = 0
        all_paths = ''
        number_of_path = 0

        #Get process id of this Fixity process
        try:
            process_id = os.getpid()
        except:
            process_id = None
            pass

        # Get File Locker and check for dead lock
        try:
            lock = DatabaseLockHandler.DatabaseLockHandler(self.Fixity.Configuration.getLockFilePath(),process_id, timeout=20)

            is_dead_lock = lock.isProcessLockFileIsDead()
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        try:
            if is_dead_lock:
                lock.is_locked = True
                lock.release()
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        try:
            lock.acquire()
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        try:
            reports_file = open(self.Fixity.Configuration.getHistoryTemplatePath(), 'r')
            history_lines = reports_file.readlines()
            reports_file.close()
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        for index in self.directories:
            if self.directories[index].getPath() != '':
                try:
                    all_paths += self.directories[index].getPath() + ';'
                except:
                    all_paths += str(self.directories[index].getPath()) + ';'
                    pass
            number_of_path += 1

        keep_time = ''
        # 1 = Monthly  - 2 = Week  - 3 = Daily
        if int(self.getScheduler().getDurationType()) == 3:
            keep_time += '99 ' + self.Fixity.Configuration.CleanStringForBreaks(str(self.getScheduler().getRunTime())) + ' 99 99'
        elif int(self.getScheduler().getDurationType()) == 2:
            keep_time += '99 ' + self.Fixity.Configuration.CleanStringForBreaks(str(self.getScheduler().getRunTime())) + ' ' + self.Fixity.Configuration.CleanStringForBreaks(str(self.getScheduler().getRun_day_or_month())) + ' 99'
        elif int(self.getScheduler().getDurationType()) == 1:
            keep_time += '99 ' + self.Fixity.Configuration.CleanStringForBreaks(str(self.getScheduler().getRunTime())) + ' 99 '+ self.Fixity.Configuration.CleanStringForBreaks(str(self.getScheduler().getRun_day_or_month()))

        history_content = ''

        project_detail_information_array = self.database.getVersionDetails(self.getID(), self.getPreviousVersion(), ' id DESC')

        if project_detail_information_array is False:
            project_detail_information_array = self.database.getVersionDetailsLast(self.getID())

        if len(project_detail_information_array) <= 0:
            project_detail_information_array = self.database.getVersionDetailsLast(self.getID())

        try:
            project_detail_information = project_detail_information_array['response']
        except:
            project_detail_information = {}
            pass

        if len(project_detail_information) <= 0:
            project_path_information = self.database.getProjectPathInfo(self.getID(),self.getVersion())
        else:
            version_id_this = project_detail_information_array['version_id']
            project_path_information = self.database.getProjectPathInfo(self.getID(),version_id_this)

        base_path_information = {}

        for path_info in project_path_information:

            Id_info = str(project_path_information[path_info]['pathID']).split('-')
            try:
                index_path_in_for = project_path_information[path_info]['path']
            except:
                index_path_in_for = r''+str(str(project_path_information[path_info]['path']).strip())

            base_path_information[str(project_path_information[path_info]['pathID'])] = {'path': index_path_in_for,
                                                                                        'code': str(project_path_information[path_info]['pathID']) ,
                                                                                        'number': str(Id_info[1]),'id':project_path_information[path_info]['id']}

        filters_array = {}
        try:
            filters_array = self.getFilters().split(',')
        except:
            try:
                filters_array = self.getFilters().encode('utf-8').split(',')
            except:
                filters_array = self.getFilters().decode('utf-8').split(',')
                pass
            pass

        dict = defaultdict(list)
        dict_hash = defaultdict(list)
        dict_File = defaultdict(list)

        old_dirs_information = {}
        try:
            id = self.getID()
        except:
            id = 0
            pass
        last_dif_paths_info = self.database.select(self.database._tableProject, '*', "`id` = '" + str(id) + "' OR `title` like '" + self.getTitle() + "'")
        try:
            self.setLast_dif_paths(str(last_dif_paths_info[0]['lastDifPaths']))
            self.setFilters(str(last_dif_paths_info[0]['filters']))
            self.setAlgorithm(str(last_dif_paths_info[0]['selectedAlgo']))
            self.setProject_ran_before(str(last_dif_paths_info[0]['projectRanBefore']))
            self.scheduler.setEmail_only_upon_warning(str(last_dif_paths_info[0]['emailOnlyUponWarning']))
        except:
            pass

        is_path_change = False

        if self.getLast_dif_paths() != 'None' and self.getLast_dif_paths() != '' and self.getLast_dif_paths() is not None:
            try:
                last_dif_paths_array = self.getLast_dif_paths().encode('utf-8').split(',')
            except:
                last_dif_paths_array = str(self.getLast_dif_paths()).split(',')
                pass

            is_path_change = True
            for last_dif_paths in last_dif_paths_array:
                single_dir_information = last_dif_paths.split('||-||')
                if single_dir_information[0] is not None and single_dir_information[0] != '':
                    old_dirs_information[single_dir_information[1]] = single_dir_information[0]

        if len(project_detail_information) > 0:
            for l in project_detail_information:

                try:
                    x = self.toTuple(project_detail_information[l])

                    if x is not None and x:

                        path_information = str(x[1]).split('||')

                        if path_information:
                            try:

                                base_old_file_path = old_dirs_information[str(path_information[0])]

                                this_file_path = str(self.Fixity.Configuration.CleanStringForBreaks(str(base_old_file_path)) +
                                                     self.Fixity.Configuration.CleanStringForBreaks(str(path_information[1])))
                                base_path = base_old_file_path

                            except:

                                this_file_path = self.Fixity.Configuration.CleanStringForBreaks(base_path_information[str(path_information[0])]['path'] + self.Fixity.Configuration.CleanStringForBreaks(path_information[1].decode('utf-8')))

                                base_path = base_path_information[str(path_information[0])]['path']

                                pass

                            # Pattern [inode:[['path With Out Code', 'Hash' ,'Boolean' ]], ..., ...]
                            dict[self.Fixity.Configuration.CleanStringForBreaks(str(x[2]))].append([this_file_path, self.Fixity.Configuration.CleanStringForBreaks(str(x[0])), False, base_path])

                            # Pattern [Hash:[['path With Out Code', 'INode' ,'Boolean' ]], ..., ...]
                            dict_hash[x[0]].append([this_file_path,  self.Fixity.Configuration.CleanStringForBreaks(str(x[2])), False, base_path])

                            # Pattern [Path:[['Hash', 'INode' ,'Boolean' ]], ..., ...]
                            dict_File[this_file_path].append([self.Fixity.Configuration.CleanStringForBreaks(str(x[0])), self.Fixity.Configuration.CleanStringForBreaks(str(x[2])), False, base_path])

                except:
                    self.Fixity.logger.LogException(Exception.message)
                    pass

        for index in self.directories:

            if self.directories[index].getPath() != '' and self.directories[index].getPath() is not None:
                try:
                    print('\nScanning Directory '+ self.directories[index].getPath() + "::\n\n")
                except:
                    pass

                result_score = self.directories[index].Run(self.getTitle(), dict, dict_hash, dict_File, filters_array, verified_files, is_from_thread, is_path_change, mark_all_confirmed, scanner)

                verified_files = result_score['verified_files']

                try:
                    confirmed += int(result_score['confirmed'])
                except:
                    pass

                try:
                    moved += int(result_score['moved'])
                except:
                    pass

                try:
                    created += int(result_score['created'])
                except:
                    pass

                try:
                    corrupted_or_changed += int(result_score['corrupted_or_changed'])
                except:
                    pass

                try:
                    missing_file += int(result_score['missing_file'])
                except:
                    pass

                try:
                    report_content += result_score['content']
                except:
                    pass

                try:
                    history_content += result_score['history_content']
                except:
                    pass

                try:
                    total += int(result_score['total'])
                except:
                    pass

        data = str(datetime.datetime.now()).split('.')
        self.database.update(self.database._tableProject, {'lastDifPaths': '', 'projectRanBefore': '1', 'lastRan': str(data[0])}, "`id` = '" + str(self.getID()) + "'")
        self.setLast_dif_paths('')
        self.setProject_ran_before('1')

        missing_files_total = 0
        try:
            missing_file_ = ('', '')
            missing_file = self.checkForMissingFiles(dict_hash)
            try:
                report_content += missing_file[0].encode('utf-8')
            except:
                try:
                    report_content += missing_file[0].decode('utf-8')
                except:
                    report_content += missing_file[0]
                    pass
                pass

            try:
                if missing_file[1] > 0:
                    missing_files_total = int(missing_file[1])
            except:
                pass

        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        try:
            total = int(total) + int(missing_files_total)
        except:
            pass

        history_text = ''
        try:
            for history_line_single in history_lines:
                history_line_single = str(history_line_single).replace('\n', '')
                if '{{base_directory}}' in history_line_single:
                    history_text += history_line_single.encode('utf-8').replace('{{base_directory}}', self.Fixity.Configuration.CleanStringForBreaks(all_paths.encode('utf-8')))+"\n"

                if '{{email_address}}' in history_line_single:
                    history_text += history_line_single.replace('{{email_address}}', self.Fixity.Configuration.CleanStringForBreaks(str(self.getEmail_address())))+"\n"

                if '{{schedule}}' in history_line_single:
                    history_text += history_line_single.replace('{{schedule}}', self.Fixity.Configuration.CleanStringForBreaks(keep_time))+"\n"

                if '{{last_ran}}' in history_line_single:
                    history_text += history_line_single.replace('{{last_ran}}', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"\n"

                if '{{filters}}' in history_line_single:
                    try:
                        history_text += history_line_single.replace('{{filters}}', self.getFilters()+'||-||'+str(self.getIgnore_hidden_file())) + "\n"
                    except:
                        try:
                            history_text += history_line_single.replace('{{filters}}', self.getFilters().encode('utf-8')+'||-||'+str(self.getIgnore_hidden_file())) + "\n"
                        except:
                            history_text += history_line_single.replace('{{filters}}', self.getFilters().decode('utf-8')+'||-||'+str(self.getIgnore_hidden_file())) + "\n"
                            pass
                        pass

                if '{{algo}}' in history_line_single:
                    history_text += history_line_single.replace('{{algo}}', str(self.getAlgorithm()))+"\n"

                if '{{content}}' in history_line_single:

                    try:
                        history_text += history_line_single.encode('utf-8').replace('{{content}}', history_content)+"\n"
                    except:
                        try:
                            history_text += history_line_single.encode('utf-8').replace('{{content}}', history_content.encode('utf-8'))+"\n"
                        except:
                            try:
                                history_text += history_line_single.encode('utf-8').replace('{{content}}', history_content.decode('utf-8'))+"\n"
                            except:
                                pass
                            pass
                        pass

        except:
             self.Fixity.logger.LogException(Exception.message)
             pass

        information_for_report = {}
        information_for_report['missing_file'] = missing_files_total
        information_for_report['corrupted_or_changed'] = corrupted_or_changed
        information_for_report['created'] = created
        information_for_report['confirmed'] = confirmed
        information_for_report['moved'] = moved
        information_for_report['total'] = total

        send_email_new = False

        if created > 0 or missing_files_total > 0 or corrupted_or_changed > 0 or moved > 0:
            send_email_new = True

        created_report_info = self.writerReportFile(information_for_report, report_content, start_time)

        self.writerHistoryFile(history_text)

        try:
            lock.release()
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        try:
            print('\nScanning Completed. \n')
        except:
            pass

        time.sleep(6)

        try:
            print('\nClosing Console. \n')
        except:
            pass

        time.sleep(2)
        #scanner.Cancel()

        if called_from == 'test':
            return information_for_report

        if check_for_changes:
            if int(moved) > 0 or int(created) > 0 or int(moved) > 0 or int(corrupted_or_changed) > 0 or missing_files_total > 0:

                return {'file_changed_found': True, 'report_path': created_report_info['path']}
            else:

                return {'file_changed_found': False, 'report_path': created_report_info['path']}
        else:

            if (self.scheduler.getEmail_only_upon_warning() == '0' or self.scheduler.getEmail_only_upon_warning() == 0) or (self.scheduler.getEmail_only_upon_warning() == '1' or  self.scheduler.getEmail_only_upon_warning() == 1) and send_email_new:
                email_config = self.Fixity.Configuration.getEmailConfiguration()
                try:
                    if self.getEmail_address() != '' and self.getEmail_address() is not None and email_config['smtp'] != '' and email_config['smtp'] is not None:
                        email_notification = EmailNotification.EmailNotification()
                        try:
                            project_name = self.getTitle()
                        except:
                            project_name = ''
                            pass

                        email_notification.ReportEmail(self.getEmail_address(), created_report_info['path'], created_report_info['email_content'], email_config, project_name)
                except:
                    self.Fixity.logger.LogException(Exception.message)
                    pass

        if is_from_thread:
            self.Fixity.selfDestruct()


    def applyFilter(self, filters, is_ignore_hidden_files):
        """
        Apply Filter For This project
        @param filters: sav filters againts this project

        @return bool
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        self.filters = filters
        if is_ignore_hidden_files == 1 or is_ignore_hidden_files is True:
            self.setIgnore_hidden_file(1)
        else:
            self.setIgnore_hidden_file(0)

        information = {}
        information['filters'] = filters

        if is_ignore_hidden_files == 1 or is_ignore_hidden_files is True:
            information['ignoreHiddenFiles'] = 1
        else:
            information['ignoreHiddenFiles'] = 0
        self.setIgnore_hidden_file(str(information['ignoreHiddenFiles']))
        response = self.Fixity.Database.update(self.Fixity.Database._tableProject, information, 'id = "' + str(self.getID()) + '"')
        return response

    def SaveSchedule(self):
        """
        Save Setting

        @return bool
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass
        self.scheduler.delTask(self.getTitle())

        schedule_update = 1
        schedule_update = self.scheduler.schedule(self.getTitle())

        return schedule_update

    def setProjectInfo(self, projects_info):
        """
        set Project Info from given array
        @param projects_info: Array of Project information

        @return None
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        try:
            self.setID(projects_info['id'])
        except:
            projects_info['id'] = self.getID()
            pass
        self.setTitle(projects_info['title'])
        if projects_info['ignoreHiddenFiles'] is True or projects_info['ignoreHiddenFiles'] == 1:
            self.setIgnore_hidden_file(1)
        else:
            self.setIgnore_hidden_file(0)

        self.setVersion(projects_info['versionCurrentID'])
        try:
            self.setProject_ran_before (projects_info['projectRanBefore'])
        except:
            pass
        try:
            self.setLast_dif_paths(projects_info['lastDifPaths'])
        except:
            pass
        self.setAlgorithm(projects_info['selectedAlgo'])
        self.setFilters(projects_info['filters'])

        self.scheduler.setDurationType(projects_info['durationType'])
        self.scheduler.setRunTime(projects_info['runTime'])
        self.scheduler.setRun_day_or_month(projects_info['runDayOrMonth'])
        self.scheduler.setRun_when_on_battery(projects_info['runWhenOnBattery'])
        self.scheduler.setIf_missed_run_upon_restart(projects_info['ifMissedRunUponRestart'])
        self.scheduler.setEmail_only_upon_warning(projects_info['emailOnlyUponWarning'])

        self.setEmail_address(projects_info['emailAddress'])
        self.setExtra_conf(projects_info['extraConf'])
        self.setLast_ran(projects_info['lastRan'])
        try:
            self.setCreated_at(projects_info['createdAt'])
        except:
            pass
        try:
            self.setUpdated_at(projects_info['updatedAt'])
        except:
            pass

        directories = self.Fixity.Database.getProjectPathInfo(projects_info['id'], projects_info['versionCurrentID'])

        self.setDirectories(directories)

    def writerHistoryFile(self, Content):
        """
        function to write the History File

        @param Content
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass
        history_file = str(self.Fixity.Configuration.getHistoryPath()) + str(self.getTitle()) + '_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S')) + '.tsv'
        try:
            history_file_obj = open(history_file, 'w+')
            try:
                history_file_obj.write(Content.decode('utf-8'))
            except:
                try:
                    history_file_obj.write(Content.encode('utf-8'))
                except:
                    history_file_obj.write(Content)
                    pass
                pass
            history_file_obj.close()
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

    def writerReportFile(self, information, detail_output_of_all_files_changes, start_time):
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        try:

            reports_file = open(self.Fixity.Configuration.getReportTemplatePath(), 'r')
            reports_lines = reports_file.readlines()
            reports_file.close()
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        time_elapsed = {}
        end_time = datetime.datetime.now()
        time_diff = end_time - start_time
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_elapsed['hrs'] = hours
        time_elapsed['min'] = minutes
        time_elapsed['sec'] = seconds

        information['time_elapsed'] = time_elapsed
        reports_text = ''
        try:
            for reports_single_line in reports_lines:

                try:
                    reports_single_line = reports_single_line.decode('utf-8').replace('\n', '')
                except:
                    reports_single_line = str(reports_single_line).replace('\n', '')
                    pass
                try:
                    reports_text += self.setReportInformation(reports_single_line.decode('utf-8'), information, detail_output_of_all_files_changes.encode('utf-8')) + "\n"
                except:
                    reports_text += self.setReportInformation(reports_single_line, information, detail_output_of_all_files_changes) + "\n"
                    pass

        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        try:
            reports_file = open(self.Fixity.Configuration.getReportEmailTemplatePath(), 'r')
            email_reports_lines = reports_file.readlines()
            reports_file.close()
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        reports_email_text = ''
        try:

            for email_reports_single_line in email_reports_lines:
                reports_single_line = str(email_reports_single_line).replace('\n', '')
                reports_email_text += self.setReportInformation(reports_single_line, information, detail_output_of_all_files_changes , True) +"\n"
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        rn = self.Fixity.Configuration.getReportsPath() + 'fixity_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S%f')) + '_' + str(self.getTitle())  + '.tsv'

        try:
            r = open(rn, 'w+')
            try:
                r.write(reports_text.decode('utf8'))
            except:

                try:
                    r.write(reports_text.encode('utf8'))
                except:
                    try:
                        r.write(reports_text)
                    except:
                        pass
                    pass

            r.close()
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass
        return {'path': rn, 'email_content': reports_email_text}

    def setReportInformation(self, report_text ,information, detail_output_of_all_files_changes, email_report = False):

        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        reports_text = str(report_text)

        if '{{project_name}}' in reports_text:
            reports_text = str(reports_text).replace('{{project_name}}', str(self.getTitle()))

        elif '{{algo}}' in reports_text:
            reports_text = str(reports_text).replace('{{algo}}', self.getAlgorithm())

        elif '{{date}}' in reports_text:
            reports_text = str(reports_text).replace('{{date}}', str(datetime.date.today()))

        elif '{{total_files}}' in reports_text:
            reports_text = str(reports_text).replace('{{total_files}}', str(information['total']))

        elif '{{confirmed_files}}' in reports_text:
            reports_text = str(reports_text).replace('{{confirmed_files}}', str(information['confirmed']))

        elif '{{moved_or_renamed_files}}' in reports_text:
            reports_text = str(reports_text).replace('{{moved_or_renamed_files}}', str(information['moved']))

        elif '{{new_files}}' in reports_text:
            reports_text = str(reports_text).replace('{{new_files}}', str(information['created']))

        elif '{{changed_files}}' in reports_text:
            reports_text = str(reports_text).replace('{{changed_files}}', str(information['corrupted_or_changed']))

        elif '{{removed_files}}' in reports_text:
            reports_text = str(reports_text).replace('{{removed_files}}', str(information['missing_file']))

        elif '{{time_elapsed}}' in reports_text:
            reports_text = str(reports_text).replace('{{time_elapsed}}', str(information['time_elapsed']['hrs']) + ' hrs ' + str(information['time_elapsed']['min'])+ ' min ' + str(information['time_elapsed']['sec']) + ' seconds')

        elif '{{details}}' in reports_text and email_report is False:
            utf_encode = False
            try:
                reports_text = reports_text.replace('{{details}}', detail_output_of_all_files_changes.encode('utf8'))
            except:
                utf_encode = True
                pass

            if utf_encode:
                try:
                    reports_text = reports_text.replace('{{details}}', detail_output_of_all_files_changes.decode('utf8'))
                except:
                    pass

        return reports_text

    def checkForMissingFiles(self, dict):

        """
        Method to find which files are missing in the scanned directory
        Input: defaultdict (from buildDict)
        Output: warning messages about missing files (one long string and  printing to stdout)

        @param dict: Directory of all file exists in the scanned folder
        @param file: List of all directory with inode,  hash and path information  with indexed using Inode

        @return: removed Messgae if removed and count of removed file
        """

        msg = ""
        count = 0

        global verified_files
        # walks through the dict and returns all False flags '''

        for keys in dict:
            for obj in dict[keys]:
                is_file_removed = False

                for single_line in verified_files:

                    try:
                        is_file_removed = obj[0] in single_line
                    except:

                        try:
                            is_file_removed = obj[0].decode('utf-8') in single_line
                        except:
                            pass

                        pass

                    if is_file_removed:
                        break

                try:
                    try:
                        if not is_file_removed:
                            verified_files.append(obj[0])
                            try:
                                verified_files.append(obj[0].decode('utf-8'))
                            except:
                                try:
                                    verified_files.append(obj[0].encode('utf-8'))
                                except:
                                    pass
                                pass

                            try:
                                msg += "Removed Files\t" + obj[0] + "\n"
                            except:
                                try:
                                    msg += "Removed Files\t" + obj[0].decode('utf-8') + "\n"
                                except:
                                    pass
                                pass
                            count += 1
                    except:
                        pass

                except:
                    path_info = (obj[0].decode('utf-8') == verified_files)
                    if path_info is False:
                        verified_files.append(obj[0])
                        verified_files.append(obj[0].decode('utf-8'))
                        msg += "Removed Files\t" + obj[0] + "\n"
                        count += 1
                    pass

        return msg, count

    def toTuple(self, line):

        """
        Method to convert database line into tuple
        @param line: Information of a single File

        @return tuple: (hash, abspath, id)
        """
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        try:
            return [line['hashes'], str(line['path'].encode('utf-8')).strip(), line['inode']]
        except:
            self.Fixity.logger.LogException(Exception.message)
            return None