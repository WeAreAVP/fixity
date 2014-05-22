#!/usr/bin/env python

from Core import DirsHandler
from Core import SharedApp, SchedulerCore
import datetime, re

global verified_files
class ProjectCore(object):
    def __init__(self):
        super(ProjectCore, self).__init__()
        self.Fixity = SharedApp.SharedApp.App
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
        for n in directories:
            try: self.directories[(n)] = DirsHandler.DirsHandler(directories[n]['path'], directories[n]['pathID'], directories[n]['id'])
            except: self.directories[(n)] = DirsHandler.DirsHandler(directories[n]['path'], directories[n]['pathID'],'')

    def setID(self, ID):self.ID = ID

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




    # Creates New Version
    #
    # @param project_id: Project ID
    # @param version_type: Version is created For
    #
    # @return Version ID Created
    def createNewVersion(self, project_id, version_type ):

        get_old_version  = self.Fixity.Database.select(self.Fixity.Database._tableVersions,'*','projectID="'+ str(project_id) + '"','versionID DESC ' )

        version_id = 1
        if len(get_old_version) > 0:
            version_id = int(get_old_version[0]['versionID'])
            version_id = version_id + 1

        information = {}
        current_date = str(datetime.datetime.now()).split('.')
        information['projectID'] = project_id
        information['versionID'] = version_id
        information['name'] = self.Fixity.Configuration.EncodeInfo(str(current_date[0]))
        information['versionType'] = version_type
        information['updatedAt'] = self.Fixity.Configuration.getCurrentTime()
        information['createdAt'] = self.Fixity.Configuration.getCurrentTime()

        return self.Fixity.Database.insert(self.Fixity.Database._tableVersions, information)

    # Save Project
    #
    # @return Project ID Created

    def Save(self):
        project_information = {}
        project_information['title'] = self.getTitle()
        project_information['ignoreHiddenFiles'] = self.getIgnore_hidden_file()
        project_information['versionCurrentID'] = self.getVersion()
        project_information['projectRanBefore'] = self.getProject_ran_before()
        project_information['lastDifPaths'] = self.getLast_dif_paths()
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
        project_exists = self.Fixity.Database.select(self.Fixity.Database._tableProject,'*','title like "' + str(self.getTitle()) + '"')


        if len(project_exists) <= 0:
            # Insert Project
            project_information['createdAt'] = self.Fixity.Configuration.getCurrentTime()
            project_id = self.Fixity.Database.insert(self.Fixity.Database._tableProject, project_information)
            self.setPreviousVersion('')

        else:

            # Update Project
            self.Fixity.Database.update(self.Fixity.Database._tableProject, project_information, 'id ="' + str(project_exists[0]['id']) + '"')
            project_id['id'] = project_exists[0]['id']
            self.setPreviousVersion(project_exists[0]['versionCurrentID'])


        self.setID(project_id['id'])
        version_id = self.createNewVersion(project_id['id'], 'project')
        self.setVersion(version_id['id'])

        # Update version
        update_version = {}
        update_version['versionCurrentID'] = version_id['id']
        self.setVersion(update_version['versionCurrentID'])


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
        self.SaveSchedule()


        if project_id['id'] :
            self.Fixity.ProjectsList[self.getTitle()] = self

        return project_id['id']

    # Delete this project
    #
    # @return Bool
    def Delete(self):
        self.Fixity.Database.delete(self.Fixity.Database._tableProject,'id ="' + str(self.getID()) + '"')
        self.Fixity.removeProject(str(self.getTitle()))
        return True


    # Import New project
    # @param file_path: file Path of imported File
    # @param project_name: Project Name
    # @param flag_is_a_tsv_file: is File .tsv
    # @param flag_is_a_fxy_file: is File .fxy
    #
    # @return Bool
    def ImportProject(self, file_path, project_name, flag_is_a_tsv_file, flag_is_a_fxy_file):

        flag_project_contain_detail = False
        file_to_import_info_of = open(file_path,'rb')

        file_to_import_info_of = str(file_to_import_info_of.readline())
        email_address =  str(file_to_import_info_of.readline())
        project_configuration = str(file_to_import_info_of.readline())
        last_ran  = str(file_to_import_info_of.readline())
        filters = {}
        algorithm_selected = ''
        if flag_is_a_tsv_file:
            filters  = str(self.Fixity.Configuration.CleanStringForDictionary(file_to_import_info_of.readline()))
            algorithm_selected  = str(self.Fixity.Configuration.CleanStringForDictionary(file_to_import_info_of.readline()))
            filters = filters.split('||-||')
        all_content = file_to_import_info_of.readlines()

        if(file_to_import_info_of and  project_configuration):

            config = {}
            run_say_or_month = ''
            duration_type = 0
            run_time = '00:00'

            config['title'] = str(project_name)
            config['versionCurrentID'] =''

            information = project_configuration.split(' ')
            is_month, is_week = 99, 99
            run_time = str(information[1])
            is_week = information[2]
            is_month = str(self.Fixity.Configuration.CleanStringForDictionary(information[3]))

            # 0 = Monthly, 1 = Weekly, 2 = Daily
            if int(is_month) == 99 and int(is_week) == 99:
                duration_type = 3
                run_say_or_month = '-'
            elif int(is_month) == 99 and int(is_week) != 99 :
                duration_type = 2
                run_say_or_month = is_week
            elif int(is_month) != 99 and int(is_week) == 99 :
                duration_type = 1
                run_say_or_month = is_month

            if algorithm_selected == '' or algorithm_selected is None:
                algorithm_selected = self.checkForAlgoUsed(all_content)

            if algorithm_selected == '' or algorithm_selected is None:
                algorithm_selected = 'sha256'

            config['lastRan'] = str(last_ran)

            if flag_is_a_tsv_file:
                config['filters'] = str(filters[0])
                config['ignoreHiddenFiles'] = str(filters[1])
                config['selectedAlgo'] = algorithm_selected
            else:
                config['filters'] = ''
                config['ignoreHiddenFiles'] = 0
                config['selectedAlgo'] = algorithm_selected

            config['runTime'] = run_time
            config['durationType'] = duration_type
            config['runDayOrMonth']  = run_say_or_month
            config['emailOnlyUponWarning'] = 0
            config['ifMissedRunUponRestart'] = 0
            config['emailOnlyUponWarning'] = 0
            config['runWhenOnBattery'] = 1
            config['extraConf'] = ''
            config['emailAddress'] = self.Fixity.Configuration.CleanStringForDictionary(str(email_address).replace(';',''))

            project_id = self.Fixity.Database.insert(self.Fixity.Database._tableProject, config)
            version_id = self.createNewVersion(project_id['id'], 'project')
            information_project_update = {}
            information_project_update['versionCurrentID'] = version_id['id']

            self.Fixity.Database.update(self.Fixity.Database._tableProject,information_project_update,'id = "'+ str(project_id['id']) +'"')

            all_project_paths = []
            path_info = file_to_import_info_of.split(';')


            if '|-|-|' in file_to_import_info_of:
                for single_path in path_info:
                    single_path_detail = single_path.split('|-|-|')
                    if(len(single_path_detail) > 1):
                        listing = []
                        listing.append(str(single_path_detail[0]))
                        listing.append(str(single_path_detail[1]))
                        all_project_paths.append(listing)
            else:
                counter = 1
                for  single_path in path_info:
                    if single_path != '' and single_path is not None :
                        listing = []
                        listing.append(str(single_path))
                        listing.append('Fixity-'+str(counter))
                        all_project_paths.append(listing)
                        counter = counter + 1

            if project_id:
                for inform_path in all_project_paths:

                    information_project_path = {}
                    information_project_path['project_id'] = project_id['id']
                    information_project_path['versionID'] = version_id['id']
                    information_project_path['path'] = inform_path[0]
                    information_project_path['pathID'] = inform_path[1]

                    self.Fixity.Database.insert(self.Fixity.Database._tableProjectPath, information_project_path)

            if project_id and len(all_content) > 0:
                flag_project_contain_detail = True
                for single_content in all_content:

                    fix_info = re.split(r'\t+', single_content)

                    if fix_info is not None:
                        if(len(fix_info) > 2):
                            if len(str(fix_info[0])) == 32:
                                hashes = fix_info[0]
                            else:
                                hashes = fix_info[0]
                            information_of_path_id = {}
                            if '||' in str(fix_info[1]):
                                information_of_path_id = str(fix_info[1]).split('||')
                            else:
                                for inform_path in all_project_paths:
                                    if str(inform_path[0]) in str(fix_info[1]):
                                        information_of_path_id[0] = inform_path[1]
                                        fix_info[1] = str(fix_info[1]).replace( str(inform_path[0]), str(inform_path[1]) + '||')

                            information_version_detail = {}
                            information_version_detail['project_id'] = project_id['id']
                            information_version_detail['versionID'] = version_id['id']
                            information_version_detail['projectPathID'] = information_of_path_id[0]
                            information_version_detail['hashes'] = self.Fixity.Configuration.CleanStringForDictionary(hashes)
                            information_version_detail['path'] = self.Fixity.Configuration.CleanStringForDictionary(fix_info[1])
                            information_version_detail['inode'] = self.Fixity.Configuration.CleanStringForDictionary(fix_info[2])
                            self.Fixity.Database.insert(self.Fixity.Database._tableVersionDetail, information_version_detail)

            if flag_project_contain_detail:
                if project_id:
                    information_to_upate = {}
                    information_to_upate['projectRanBefore'] = 1
                    self.Fixity.Database.update(self.Fixity.Database._tableProject, information_to_upate, "id='" + str(project_id['id']) + "'")

        try:
            file_to_import_info_of.close()
        except:
            pass
        return True


    #Check For Algorithm Used
    #@param content: Content line containing Algorithm
    #
    #@return: Algorithm Used
    def checkForAlgoUsed(self,content):
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
        information = {}
        information['title'] = new_title
        self.Fixity.Database.update(self.Fixity.Database._tableProject,information, 'id="' + str(self.getID()) + '"')

        return False


    # Run This project
    # @param check_for_changes: if only want to know is all file confirmed or not
    #
    # @return array
    def Run(self, check_for_changes = False ):
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

        for index in self.directories:
            if self.directories[index].getPath() != '':
                all_paths += str(self.directories[index].getPath())+';'
            number_of_path = number_of_path + 1

        history_content += self.Fixity.Configuration.CleanStringForDictionary(str(all_paths))+"\n"
        history_content += self.Fixity.Configuration.CleanStringForDictionary(str(self.getEmail_address()))+"\n"
        keep_time = ''

        # - 1 = Monthly  - 2 = Week  - 3 = Daily

        if int(self.getScheduler().getDurationType()) == 3 :
            keep_time += '99 ' + self.Fixity.Configuration.CleanStringForDictionary(str(self.getScheduler().getRunTime())) + ' 99 99'
        elif int(self.getScheduler().getDurationType()) == 2 :
            keep_time += '99 ' + self.Fixity.Configuration.CleanStringForDictionary(str(self.getScheduler().getRunTime()))+ ' ' + self.Fixity.Configuration.CleanStringForDictionary(str(self.getScheduler().getRun_day_or_month())) + ' 99'
        elif int(self.getScheduler().getDurationType()) == 1 :
            keep_time += '99 ' + self.Fixity.Configuration.CleanStringForDictionary(str(self.getScheduler().getRunTime())) + ' 99 '+self.Fixity.Configuration.CleanStringForDictionary(str(self.getScheduler().getRun_day_or_month()))

        history_content += self.Fixity.Configuration.CleanStringForDictionary(keep_time) +"\n"
        history_content += datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
        history_content += str(self.getFilters())+'||-||'+str(self.getIgnore_hidden_file()) + "\n"
        history_content +=  str(self.getAlgorithm()) + "\n"

        for index in self.directories:
            if self.directories[index].getPath() != '' and self.directories[index].getPath() is not None:
                result_score = self.directories[index].Run(self.getTitle())
                try:confirmed = confirmed + int(result_score['confirmed'])
                except:pass

                try:moved = moved + int(result_score['moved'])
                except:pass

                try:created = created + int(result_score['created'])
                except:pass

                try:corrupted_or_changed = corrupted_or_changed + int(result_score['corrupted_or_changed'])
                except:pass

                try:missing_file = missing_file + int(result_score['missing_file'])
                except:pass

                try:report_content += str(result_score['content'])
                except:pass

                try:history_content += str(result_score['history_content'])
                except:pass

                try:total += str(result_score['total'])
                except:pass


        information_for_report = {}
        information_for_report['missing_file'] = missing_file
        information_for_report['corrupted_or_changed']= corrupted_or_changed
        information_for_report['created']= created
        information_for_report['confirmed']= confirmed
        information_for_report['moved']= moved
        information_for_report['total'] = total

        created_report_path = self.writerReportFile(information_for_report, report_content)
        self.writerHistoryFile(history_content)

        if check_for_changes:
            if int(moved) > 0:return {'file_changed_found':True, 'report_path':created_report_path}

            elif int(created) > 0:return {'file_changed_found':True, 'report_path':created_report_path}

            elif int(moved) > 0:return {'file_changed_found':True, 'report_path':created_report_path}

            elif int(corrupted_or_changed) > 0:return {'file_changed_found':True, 'report_path':created_report_path}

            else:return {'file_changed_found':False, 'report_path':created_report_path }

    # Apply Filter For This project
    # @param filters: sav filters againts this project
    #
    # @return bool
    def applyFilter(self,filters ,is_ignore_hidden_files):
        self.filters = filters
        self.setIgnore_hidden_file(is_ignore_hidden_files)

        information = {}
        information['filters'] = filters

        if is_ignore_hidden_files:
            information['ignoreHiddenFiles'] = 1
        else:
            information['ignoreHiddenFiles'] = 0

        response = self.Fixity.Database.update(self.Fixity.Database._tableProject, information, '"' + str(self.getID()) + '"')
        return response

    # Save Setting
    #
    # @return bool
    def SaveSchedule(self):
        self.scheduler.delTask(self.getTitle())
        self.scheduler.schedule(self.getTitle())


    # set Project Info from given array
    # @param projects_info: Array of Project information

    # @return None
    def setProjectInfo(self, projects_info):
        self.setID(projects_info['id'])
        self.setTitle (projects_info['title'])
        self.setIgnore_hidden_file (projects_info['ignoreHiddenFiles'])
        self.setVersion (projects_info['versionCurrentID'])
        self.setProject_ran_before (projects_info['projectRanBefore'])
        self.setLast_dif_paths (projects_info['lastDifPaths'])
        self.setAlgorithm (projects_info['selectedAlgo'])
        self.setFilters (projects_info['filters'])

        self.scheduler.setDurationType (projects_info['durationType'])
        self.scheduler.setRunTime (projects_info['runTime'])
        self.scheduler.setRun_day_or_month (projects_info['runDayOrMonth'])
        self.scheduler.setRun_when_on_battery (projects_info['runWhenOnBattery'])
        self.scheduler.setIf_missed_run_upon_restart (projects_info['ifMissedRunUponRestart'])
        self.scheduler.setEmail_only_upon_warning (projects_info['emailOnlyUponWarning'])

        self.setEmail_address (projects_info['emailAddress'])
        self.setExtra_conf(projects_info['extraConf'])
        self.setLast_ran(projects_info['lastRan'])
        self.setCreated_at(projects_info['createdAt'])
        self.setUpdated_at(projects_info['updatedAt'])

        directories = self.Fixity.Database.getProjectPathInfo(projects_info['id'], projects_info['versionCurrentID'])
        self.setDirectories(directories)



    def writerHistoryFile(self, Content):
        history_file = str(self.Fixity.Configuration.getHistoryPath()) + str(self.getTitle()) + '_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S')) + '.tsv'
        try:
            history_file_obj = open(history_file, 'w+')
            history_file_obj.write(Content)
            history_file_obj.close()
        except Exception:
            self.Fixity.logger.LogException(Exception.message)
            pass





    def writerReportFile(self, information, detail_output_of_all_files_changes):
        try:
            report = "Fixity report\n"
            report += "Project name\t" + self.getTitle() + "\n"
            report += "Algorithm used\t" + str(self.getAlgorithm()) + "\n"
            report += "Date\t" + str(datetime.date.today()) + "\n"
            report += "Total Files\t" + str(information['total']) + "\n"
            report += "Confirmed Files\t" + str(information['confirmed']) + "\n"
            report += "Moved or Renamed Files\t" + str(information['moved']) + "\n"
            report += "New Files\t" + str(information['created']) + "\n"
            report += "Changed Files\t" + str(information['corrupted_or_changed']) + "\n"
            report += "Removed Files\t" + str(information['missing_file']) + "\n"

            utf_encode = False
            try:
                report += detail_output_of_all_files_changes.encode('utf8')
            except:
                utf_encode = True
                pass
            if utf_encode:
                try:
                    report += detail_output_of_all_files_changes.decode('utf8')
                except:
                    pass
        except Exception:
            self.Fixity.logger.LogException(Exception.message)
            pass


        rn = self.Fixity.Configuration.getReportsPath() + 'fixity_' + str(datetime.date.today()) + '-' + str(datetime.datetime.now().strftime('%H%M%S%f')) + '_' + str(self.getTitle())  + '.tsv'

        try:
            r = open(rn, 'w+')
            try:
                r.write(report.decode('utf8'))
            except:
                try:
                    r.write(report.encode('utf8'))
                except:
                    pass

            r.close()
        except Exception:
            self.Fixity.logger.LogException(Exception.message)
            pass
        return rn
