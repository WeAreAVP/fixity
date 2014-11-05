# -*- coding: UTF-8 -*-
#Created on May 14, 2014
#
#@author: Furqan Wasi <furqan@avpreserve.com>

# Custom Libraries

from GUI import GUILibraries, AboutFixityGUI, ApplyFiltersGUI, ChangeAlgorithmGUI
from GUI import ChangeNameGUI, EmailNotificationGUI, ImportProjGUI, PathChangeGUI
from Core import SharedApp, ProjectCore, DatabaseLockHandler


# Built-in Libraries
import datetime
import os

''' Project GUI Class '''
class ProjectGUI(GUILibraries.QMainWindow):

    #Constructor
    def __init__(self):
        super(ProjectGUI, self).__init__()

        self.should_update = True
        self.is_path_changed = False
        self.Fixity = SharedApp.SharedApp.App
        self.unsaved = False
        self.about_fixity_gui = AboutFixityGUI.AboutFixityGUI(self)
        self.apply_filters_gui = ApplyFiltersGUI.ApplyFiltersGUI(self)
        self.change_algorithm_gui = ChangeAlgorithmGUI.ChangeAlgorithmGUI(self)
        self.change_name_gui = ChangeNameGUI.ChangeNameGUI(self)
        self.email_notification_gui = EmailNotificationGUI.EmailNotificationGUI(self)
        self.import_project_gui = ImportProjGUI.ImportProjectGUI(self)
        self.path_change_gui = PathChangeGUI.PathChangeGUI(self)
        self.notification = GUILibraries.NotificationGUI.NotificationGUI()

        self.setWindowIcon(GUILibraries.QIcon(self.Fixity.Configuration.getLogoSignSmall()))
        self.setWindowTitle(self.Fixity.Configuration.getApplicationName())

        # create Menu
        self.createMenu()

        # Set Short Cuts
        self.setShortCuts()

        #Set All Menu
        self.setAllMenus()

        #Set Trigger
        self.setTriggersForMenu()

        #create Project Listing Options
        self.createProjectListingOption()

        #create Project scheduling Option
        self.creatSchedulingOptions()

        #create Directories and email Listing view
        self.createDirectories()

        if len(self.Fixity.ProjectsList) > 0:
            for project in self.Fixity.ProjectsList:
                GUILibraries.QListWidgetItem(str(self.Fixity.ProjectsList[project].getTitle()), self.projects)

        self.projects.setCurrentRow(0)

        try:
            self.old = self.projects.itemAt(0, 0)
            self.update(self.old)
            self.old.setSelected(True)
        except:
            pass

        self.unsaved = False
        self.toggler((self.projects.count() == 0))
        self.show()
        self.unsaved = False

        if self.Fixity.Configuration.getOsType() == 'Windows':
            # set Fixed Size(Width, Height)
            self.setFixedSize(900, 318)
        else:
            # set Fixed Size(Width, Height)
            self.setFixedSize(1000, 300)


    def createDirectories(self):
        self.mail_layout = GUILibraries.QVBoxLayout()
        self.mail_layout.setSpacing(0)
        self.mail_text_fields = []

        self.dirs_layout = GUILibraries.QVBoxLayout()
        self.dirs_layout.setSpacing(0)
        self.dirs_text_fields, self.browse_dirs, self.bin_of_dirs = [], [], []

        for n in xrange(0, self.Fixity.Configuration.getNumberOfPathDirectories()):
            hbox = GUILibraries.QHBoxLayout()
            hbox.setContentsMargins(0, 0, 0, 0)

            hbox.setSpacing(0)
            self.dirs_text_fields.append(GUILibraries.QLineEdit())
            self.browse_dirs.append(GUILibraries.QPushButton('...'))
            self.bin_of_dirs.append(GUILibraries.QPushButton('X'))

            self.browse_dirs[n].setFixedSize(30, 21)
            self.dirs_text_fields[n].setContentsMargins(0, 2, 7, 0)
            self.dirs_text_fields[n].setFixedSize(150,22)
            self.bin_of_dirs[n].setFixedSize(25,22)
            self.bin_of_dirs[n].setStyleSheet('QPushButton {color: red; font: bold}')
            self.browse_dirs[n].clicked.connect(self.pickDir)
            self.dirs_text_fields[n].textChanged.connect(self.changed)
            self.bin_of_dirs[n].clicked.connect(self.removeDirs)

            hbox.addWidget(self.dirs_text_fields[n])
            hbox.addWidget(self.browse_dirs[n])
            hbox.addWidget(self.bin_of_dirs[n])

            self.dirs_layout.addLayout(hbox)
            self.mail_text_fields.append(GUILibraries.QLineEdit())
            self.mail_layout.addWidget(self.mail_text_fields[n])
            self.mail_text_fields[n].textChanged.connect(self.changed)
            self.dirs_text_fields[n].setReadOnly(True)

        self.dirs =GUILibraries.QGroupBox("Directories")
        self.dirs.setFixedSize(273,289)
        self.mail = GUILibraries.QGroupBox("Recipient Email Addresses")

        self.dirs.setLayout(self.dirs_layout)
        self.mail.setLayout(self.mail_layout)

        self.main = GUILibraries.QHBoxLayout()

        self.main.addWidget(self.pgroup)
        self.main.addWidget(self.scheduling_groupBox)
        self.main.addWidget(self.dirs)
        self.main.addWidget(self.mail)

        self.widget.setLayout(self.main)
        self.setCentralWidget(self.widget)

        self.run_only_on_ac_power.setDisabled(False)
        self.start_when_available.setDisabled(False)
        self.email_only_when_something_changed.setDisabled(False)

        if len(self.Fixity.ProjectsList) <= 0:
            self.togglerMenu(True)

    def createMenu(self):
         #Creat All Menu
        self.menubar = self.menuBar()
        self.file_manu_fixity = self.menubar.addMenu('&File')
        self.preferences = self.menubar.addMenu('&Preferences')
        self.new_menu = GUILibraries.QAction('&New Project', self)
        self.save_menu = GUILibraries.QAction('&Run Now', self)
        self.update_menu = GUILibraries.QAction('&Save Settings', self)
        self.delete_menu = GUILibraries.QAction('&Delete Project', self)
        self.config_email_menu = GUILibraries.QAction('&Email Settings', self)
        self.about_fixity_menu = GUILibraries.QAction('&About Fixity', self)
        self.quit_menu = GUILibraries.QAction('&Quit Fixity', self)
        self.quit_menu.setShortcut(GUILibraries.QKeySequence.Quit)
        self.filter_files_menu = GUILibraries.QAction('&Filter Files', self)
        self.change_name_menu = GUILibraries.QAction('&Change Project Name', self)
        self.decryption_manager_menu = GUILibraries.QAction('&Select Checksum Algorithm', self)
        self.debuging_menu = GUILibraries.QAction('&Turn Debuging Off', self)
        self.import_menu = GUILibraries.QAction('&Import Project', self)

    def setShortCuts(self):
        self.save_menu.setShortcut('CTRL+R')
        self.new_menu.setShortcut('CTRL+N')
        self.update_menu.setShortcut('CTRL+S')
        self.about_fixity_menu.setShortcut('CTRL+,')
        self.filter_files_menu.setShortcut('CTRL+F')
        self.change_name_menu.setShortcut("CTRL+U")
        self.decryption_manager_menu.setShortcut("CTRL+A")
        self.debuging_menu.setShortcut("CTRL+D")
        self.import_menu.setShortcut("CTRL+I")
        self.config_email_menu.setShortcut("CTRL+E")
        self.delete_menu.setShortcut(GUILibraries.QKeySequence.DeleteStartOfWord)

    def setAllMenus(self):
        self.file_manu_fixity.addAction(self.new_menu)
        self.file_manu_fixity.addAction(self.update_menu)
        self.file_manu_fixity.addAction(self.save_menu)
        self.file_manu_fixity.addAction(self.delete_menu)
        self.file_manu_fixity.addAction(self.change_name_menu)
        self.file_manu_fixity.addAction(self.about_fixity_menu)
        self.file_manu_fixity.addAction(self.quit_menu)
        self.preferences.addAction(self.filter_files_menu)
        self.preferences.addAction(self.debuging_menu)
        self.preferences.addAction(self.import_menu)
        self.preferences.addAction(self.config_email_menu)
        self.preferences.addAction(self.decryption_manager_menu)

    def setTriggersForMenu(self):

        self.delete_menu.triggered.connect(self.delete)
        self.new_menu.triggered.connect(self.new)
        self.save_menu.triggered.connect(self.run)
        self.update_menu.triggered.connect(self.Save)
        self.quit_menu.triggered.connect(self.Close)
        self.debuging_menu.triggered.connect(self.switchDebugger)
        self.about_fixity_menu.triggered.connect(self.AboutFixity)
        self.config_email_menu.triggered.connect(self.setEmailConfiguration)
        self.filter_files_menu.triggered.connect(self.setFilter)
        self.change_name_menu.triggered.connect(self.ChangeName)
        self.decryption_manager_menu.triggered.connect(self.setAlgorithm)
        self.import_menu.triggered.connect(self.importOld)

    def creatSchedulingOptions(self):
        self.scheduling_groupBox = GUILibraries.QGroupBox("Scheduling")
        self.monthly = GUILibraries.QRadioButton("Monthly")
        self.weekly = GUILibraries.QRadioButton("Weekly")
        self.daily = GUILibraries.QRadioButton("Daily")

        self.run_only_on_ac_power = GUILibraries.QCheckBox("Run when on battery power")
        self.start_when_available  = GUILibraries.QCheckBox("If missed, run upon restart")
        self.email_only_when_something_changed = GUILibraries.QCheckBox("Email only upon warning or failure")

        self.run_only_on_ac_power.clicked.connect(self.changed)
        self.start_when_available.clicked.connect(self.changed)
        self.email_only_when_something_changed.clicked.connect(self.changed)

        self.run_only_on_ac_power.setChecked(True)
        self.start_when_available.setChecked(True)
        self.email_only_when_something_changed.setChecked(True)

        self.monthly.clicked.connect(self.monthClick)
        self.weekly.clicked.connect(self.weekClick)
        self.daily.clicked.connect(self.dayClick)

        self.switchDebugger(True)
        self.scheduling_layout = GUILibraries.QVBoxLayout()

        self.scheduling_layout.addWidget(self.monthly)
        self.scheduling_layout.addWidget(self.weekly)
        self.scheduling_layout.addWidget(self.daily)
        self.scheduler_run_time = GUILibraries.QLabel("Scheduler Run Time: ")
        self.scheduling_layout.addWidget(self.scheduler_run_time)
        self.timer = GUILibraries.QTimeEdit(GUILibraries.QTime())

        self.timer.setDisplayFormat(self.Fixity.Configuration.getTimeFormat())
        self.scheduling_layout.addWidget(self.timer)

        self.scheduler_run_on = GUILibraries.QLabel("Scheduler Run On: ")
        self.scheduling_layout.addWidget(self.scheduler_run_on)
        self.day_of_week = GUILibraries.QComboBox()
        self.day_of_week.addItems(self.Fixity.Configuration.getWeekDays())
        self.day_of_week.activated.connect(self.changed)
        self.scheduling_layout.addWidget(self.day_of_week)
        self.day_of_week.hide()



        self.day_of_month = GUILibraries.QSpinBox()
        self.day_of_month.setMaximum(31)
        self.day_of_month.setMinimum(1)

        self.day_of_month.valueChanged.connect(self.changed)
        self.scheduling_layout.addWidget(self.day_of_month)
        self.day_of_month.hide()


        self.spacer = GUILibraries.QSpacerItem(125, 30)
        self.scheduling_layout.addItem(self.spacer)
        system_information = self.Fixity.Configuration.getWindowsInformation()

        if self.Fixity.Configuration.getOsType() == 'Windows' and str(system_information['WindowsType']) == '7':
            self.scheduling_layout.addWidget(self.run_only_on_ac_power)
            self.scheduling_layout.addWidget(self.start_when_available)
        self.scheduling_layout.addWidget(self.email_only_when_something_changed)

        self.lastrun = GUILibraries.QLabel("Last checked: ")
        self.scheduling_layout.addWidget(self.lastrun)
        self.scheduling_groupBox.setLayout(self.scheduling_layout)
        self.scheduling_groupBox.setFixedSize(260, 289)

    def closeEvent(self, event):
        if self.unsaved:
            response = self.notification.showQuestion(self, 'Unsaved Project', GUILibraries.messages['close_unsaved'])
            if response:
                self.unsaved = True
                event.ignore()
                return False
            else:
                event.accept()
                self.close()

    def changed(self):
        self.unsaved = True

    def createProjectListingOption(self):
        self.widget = GUILibraries.QWidget(self)
        self.pgroup = GUILibraries.QGroupBox("Projects")
        self.project_layout = GUILibraries.QVBoxLayout()
        self.projects = GUILibraries.QListWidget(self)
        self.projects.setFixedSize(115, 190)
        self.projects.setCurrentRow(0)
        self.project_layout.addWidget(self.projects)
        self.pgroup.setLayout(self.project_layout)
        self.projects.itemSelectionChanged.connect(self.update)

    #Updates Fields When Project Is Selected In List
    #@Slot(str)
    #@param new: Is New Project
    #@param projectName: project Name If Not Selected

    def Close(self):
        if self.unsaved:
            response = self.notification.showQuestion(self, 'Unsaved Project', GUILibraries.messages['close_unsaved'])
            if response:
                self.unsaved = False
                self.projects.setCurrentRow(self.projects.indexFromItem(self.old).row())
                self.unsaved = True
                return
            else:
                self.unsaved = False
                self.close()
        else:
            self.close()

    def update(self, new='', project_name_force=None):

        if self.should_update is False:
            return

        if self.unsaved:

            response = self.notification.showQuestion(self, 'Unsaved Project', GUILibraries.messages['new_project_unsaved'])

            if response:

                self.should_update = False
                self.unsaved = False

                if self.old:
                    try:
                        self.projects.setCurrentRow(self.projects.indexFromItem(self.old).row())
                    except:
                        self.projects.setCurrentRow(0)
                        pass
                else:
                    self.projects.setCurrentRow(0)

                self.should_update = True

                self.unsaved = True
                self.old = self.projects.currentItem()
                return

            else:

                selected = int(self.projects.currentIndex().row())
                self.unsaved = False
                self.refreshProjectSettings()
                self.unsaved = False
                self.projects.setCurrentRow(selected)

        try:
            project_name = self.projects.currentItem().text()
        except:
            project_name = ''

        try:
            project_core = self.Fixity.ProjectRepo.getSingleProject(project_name)

        except:
            self.Fixity.logger.LogException(Exception.message)
            pass
        try:
            if project_core is False:
                return
        except:
            return

        for n in range(0, self.Fixity.Configuration.getNumberOfPathDirectories()):
            self.dirs_text_fields[(n)].setText("")
            self.mail_text_fields[(n)].setText("")

        self.run_only_on_ac_power.setChecked(False)
        self.start_when_available.setChecked(False)
        self.email_only_when_something_changed .setChecked(False)

        emails = str(project_core.getEmail_address())
        emails = emails.split(',')
        last_run_label = project_core.getLast_ran()

        countEmail = 0
        for email in emails:
            try:
                self.mail_text_fields[(countEmail)].setText(str(email).strip())
            except:
                pass
            countEmail += 1

        directories = project_core.getDirectories()
        for n in directories:
            try:
                try:
                    self.dirs_text_fields[(n)].setText(directories[(n)].getPath())
                except:
                    self.dirs_text_fields[(n)].setText(str(directories[(n)].getPath()).strip())
                    pass

            except:
                try:
                    self.dirs_text_fields[(n)].setText("")
                except:
                    pass
                pass

        if int(project_core.scheduler.getEmail_only_upon_warning()) == 1:
            self.email_only_when_something_changed .setChecked(True)
        elif int(project_core.scheduler.getEmail_only_upon_warning()) == 0:
            self.email_only_when_something_changed .setChecked(False)

        if int(project_core.scheduler.getRun_when_on_battery()) == 1:
            self.run_only_on_ac_power.setChecked(True)
        elif int(project_core.scheduler.getRun_when_on_battery()) == 0:
            self.run_only_on_ac_power.setChecked(False)

        if int(project_core.scheduler.getIf_missed_run_upon_restart()) == 1:
            self.start_when_available.setChecked(True)
        elif int(project_core.scheduler.getIf_missed_run_upon_restart()) == 0:
            self.start_when_available.setChecked(False)

        if str(project_core.scheduler.getDurationType()) == '1':
                self.monthly.setChecked(True)
                self.monthClick()
                try:
                    self.day_of_month.setValue(int(project_core.scheduler.getRun_day_or_month()))
                except:
                    self.Fixity.logger.LogException(Exception.message)
                    return

        elif str(project_core.scheduler.getDurationType()) == '2':
                self.weekly.setChecked(True)
                self.weekClick()
                self.day_of_week.setCurrentIndex(int(project_core.scheduler.getRun_day_or_month()))

        elif str(project_core.scheduler.getDurationType()) == '3':
                self.daily.setChecked(True)
                self.dayClick()

        try:
            t = str(project_core.scheduler.getRunTime()).split(':')
        except:
            t = ['00', '00']

        self.timer.setTime(GUILibraries.QTime(int(t[0]), int(t[1])))
        self.timer.timeChanged.connect(self.changed)

        if last_run_label and last_run_label is not None and last_run_label != 'None':
            self.lastrun.setText("Last checked:\n" + last_run_label)
        else:
            self.lastrun.setText("Last checked:\n --")
        if new:
            self.old = new
        else:
            self.old = self.projects.currentItem()
        self.unsaved = False

    def switchDebugger(self, is_start=False):
        status = self.Fixity.logger.get()
        if is_start:
            if status == 'true':
                debug_text = 'Turn Debugging On'
            else:
                debug_text = 'Turn Debugging Off'
        else:
            if status == 'true':
                new_status = 'false'
                self.Fixity.logger.set('false')
                debug_text = 'Turn Debugging Off'
            else:
                new_status = 'true'
                debug_text = 'Turn Debugging On'

            self.Fixity.logger.set(new_status)
        self.debuging_menu.setText(debug_text)

    def delete(self):
        try:
            response = self.notification.showQuestion(self, 'Delete Project?', str(GUILibraries.messages['sure_delete']) + self.projects.currentItem().text() + "?")
        except:
            self.Fixity.logger.LogException(Exception.message)
            return

        if response:
            try:
                project_core = self.Fixity.ProjectRepo.getSingleProject(self.projects.currentItem().text())

                project_core.Delete()


            except:
                pass
            self.unsaved = False
            self.projects.takeItem(self.projects.row(self.projects.currentItem()))
            self.unsaved = True
            for SingleRangeValue in xrange(0, self.Fixity.Configuration.getNumberOfPathDirectories()):
                    self.dirs_text_fields[SingleRangeValue].setText("")
                    self.mail_text_fields[SingleRangeValue].setText("")

            self.monthly.setChecked(True)
            self.monthClick()
            self.timer.setTime(GUILibraries.QTime(0, 0))
            self.lastrun.setText("Last checked:\n --")
            self.toggler((self.projects.count() == 0))
            self.unsaved = False
            self.update(False)
            if len(self.Fixity.ProjectsList) <= 0:
                self.toggler(True)
                self.togglerMenu(True)

    def run(self):
        if all(d.text() == "" for d in self.dirs_text_fields):
            self.notification.showError(self, "Error", GUILibraries.messages['no_directories'])
            return

        if not(self.monthly.isChecked() or self.weekly.isChecked() or self.daily.isChecked()):
            self.notification.showError(self, "Error", GUILibraries.messages['project_schedule_not_set'])
            return
        is_lock_exists = False
        is_dead_lock = False

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
            is_lock_exists = lock.isLockFileExists()
        except:
            pass

        if is_lock_exists is False:
            project_core = self.Save()
            self.notification.showInformation(self, "Success", self.projects.currentItem().text() + " is currently scanning.\nPlease do not close Fixity until a report is generated.")
            self.scanner = Scanner(self)
            project_core.launchThread(self.scanner)

        else:
            self.notification.showWarning(self, "Warning", "Fixity is already scanning a project.\nPlease wait until the current scan completes before starting a new one.")

    #Check For Changes In the provided base  path and old given base path the given project name
    #@param projectName: Project Name
    #@param searchForPath: Path of a given base Dire in the view
    #@param code: Code of that specific path in the view
    #
    #@return: None

    def checkForChanges(self, search_for_path, code):
        try:
            self.Fixity = SharedApp.SharedApp.App
            project_core = self.Fixity.ProjectRepo.getSingleProject(str(self.projects.currentItem().text()))
            if project_core is False:
                return
            project_info = self.Fixity.Database.getProjectInfo(str(self.projects.currentItem().text()))

            project_core.setProjectInfo(project_info[0])
            directory_detail = project_core.getDirectories()

            if len(directory_detail) > 0:
                for directory_detail_single in directory_detail:
                    if str(directory_detail[directory_detail_single].getPathID().strip()) == str(code).strip():
                        if directory_detail[directory_detail_single].getPath().strip() != '' and  search_for_path != '':
                            if directory_detail[directory_detail_single].getPath().strip() != search_for_path:
                                self.is_path_changed = True
                                self.ChangeRootDirectoryInformation(directory_detail[directory_detail_single].getPath(), search_for_path, code )

            if self.is_path_changed is True and (project_core.getLast_dif_paths() is None or project_core.getLast_dif_paths() == '' or project_core.getLast_dif_paths() == 'None'):
                all_previous_paths = ''
                for directory_detail_single in directory_detail:
                    if directory_detail[directory_detail_single].getPath() is not None:
                        if all_previous_paths == '':
                            all_previous_paths = directory_detail[directory_detail_single].getPath()+'||-||'+directory_detail[directory_detail_single].getPathID()
                        else:
                            all_previous_paths = all_previous_paths+','+directory_detail[directory_detail_single].getPath() + '||-||' + directory_detail[directory_detail_single].getPathID()

                self.is_path_changed_global = True

                if len(directory_detail) > 0:
                    update_inf = {}
                    update_inf['lastDifPaths'] = all_previous_paths
                    self.Fixity.Database.update(self.Fixity.Database._tableProject, update_inf, "id = '" + str(project_core.getID()) + "'")
                    project_core.setLast_dif_paths(all_previous_paths)

                self.is_path_changed = False

        except:
            self.Fixity.logger.LogException()
            pass

    #Pop Up to Change Root Directory If any change occured
    #@param orignalPathText: Path In Manifest
    #@param change_path_text: New Path Given in Fixity Tool

    def ChangeRootDirectoryInformation(self,orignal_path_text, change_path_text, code):
        self.path_change_gui.Cancel()
        code_of_directory =  str(code).split('-')
        self.path_change_gui = PathChangeGUI.PathChangeGUI(self,orignal_path_text, change_path_text, int(code_of_directory[1]))
        self.path_change_gui.SetDesgin()
        self.path_change_gui.ShowDialog()
        self.setWindowTitle("Fixity " + self.Fixity.Configuration.getApplicationVersion())

    def checkNumberOfDirsChange(self):
        try:
            number_of_current_dirs = 0
            for directory_single in self.dirs_text_fields:
                if directory_single.text().strip() != "":
                    number_of_current_dirs += 1
            num_if_path_in_db = 0

            project_core = self.Fixity.ProjectRepo.getSingleProject(str(self.projects.currentItem().text()))
            directory_detail = project_core.getDirectories()

            all_previous_paths = ''
            for directory_detail_single in directory_detail:
                if str(directory_detail[directory_detail_single].getPath()).strip() != "":
                    if directory_detail[directory_detail_single].getPath() is not None:
                        if all_previous_paths == '':
                            all_previous_paths = str(directory_detail[directory_detail_single].getPath())+'||-||'+str(directory_detail[directory_detail_single].getPathID())
                        else:
                            all_previous_paths = all_previous_paths+','+str(directory_detail[directory_detail_single].getPath())+'||-||'+str(directory_detail[directory_detail_single].getPathID())

                        num_if_path_in_db += 1

            if int(num_if_path_in_db) > int(number_of_current_dirs) and (project_core.getLast_dif_paths() == '' or project_core.getLast_dif_paths() == 'None'):
                update_inf = {}
                update_inf['lastDifPaths'] = all_previous_paths
                self.Fixity.Database.update(self.Fixity.Database._tableProject, update_inf, "id = '" + str(project_core.getID()) + "'")
                project_core.setLast_dif_paths(all_previous_paths)
        except:
            pass

    def check_for_path_changes(self):
        num_if_path_scanned = 0
        for directory_single in self.dirs_text_fields:

            if directory_single.text().strip() != "":
                num_if_path_scanned += 1

        directory_increment = 1
        for directory_single in self.dirs_text_fields:
            self.checkForChanges(directory_single.text(), 'Fixity-'+str(directory_increment))
            directory_increment += 1

    def togglerMenu(self, status):
        self.save_menu.setDisabled(status)
        self.update_menu.setDisabled(status)
        self.delete_menu.setDisabled(status)
        self.change_name_menu.setDisabled(status)
        self.filter_files_menu.setDisabled(status)
        self.decryption_manager_menu.setDisabled(status)

    def new(self):

        if self.unsaved is True:
            self.notification.showError(self, "Fixity", str(GUILibraries.messages['save_other_projects']))
            return

        QID = GUILibraries.QInputDialog(self)
        QID.setWindowModality(GUILibraries.Qt.WindowModal)
        name = QID.getText(self, "Project Name", "Name for new Fixity project:", text="New_Project")

        if not name[1]:
            if len(self.Fixity.ProjectsList) <= 0:
                self.update_menu.setDisabled(True)
                self.delete_menu.setDisabled(True)
            return

        is_project_name_valid = self.Fixity.Validation.ValidateProjectName(name[0])
        if not is_project_name_valid:
            self.notification.showError(self, "Fixity", str(GUILibraries.messages['in_valid_project_name']))
            return

        project_info = self.Fixity.Database.select(self.Fixity.Database._tableProject, 'id', 'title="'+name[0]+'"')

        if len(project_info) > 0:
            self.notification.showError(self, "Fixity", str(GUILibraries.messages['in_valid_project_name_detailed']))
            return

        self.update_menu.setDisabled(False)
        self.delete_menu.setDisabled(False)
        new_item = GUILibraries.QListWidgetItem(name[0], self.projects)

        self.projects.setCurrentItem(new_item)
        self.monthly.setChecked(True)
        self.monthClick()
        self.day_of_month.setValue(1)
        self.timer.setTime(GUILibraries.QTime(0, 0))

        for SingleRangeValue in xrange(0, self.Fixity.Configuration.getNumberOfPathDirectories()):
            self.dirs_text_fields[SingleRangeValue].setText("")
            self.mail_text_fields[SingleRangeValue].setText("")

        self.toggler(False)
        self.unsaved = True

        if new_item:
            self.old = new_item

    def Save(self, project = None):

        all_email_address = ''
        is_recipient_email_address_set = False
        for mail_string in self.mail_text_fields:
            SingleEmail = mail_string.text().strip()
            if SingleEmail != "":
                all_email_address = all_email_address + str(SingleEmail) + ','
                is_recipient_email_address_set = True
                error_msg = self.Fixity.Validation.ValidateEmail(SingleEmail)
                if not error_msg:
                    self.notification.showWarning(self, "Error", GUILibraries.messages['invalid_email'])
                    return

        if is_recipient_email_address_set:
                self.Fixity = SharedApp.SharedApp.App
                email_info = self.Fixity.Configuration.getEmailConfiguration()
                try:
                    if (email_info['email'] == '' and email_info['email'] is None) and (email_info['smtp'] != '' or email_info['smtp'] is None):
                        self.notification.showWarning(self, "Email Validation", GUILibraries.messages['configure_email_pref'])
                        return
                except:
                    self.notification.showWarning(self, "Email Validation", GUILibraries.messages['configure_email_pref'])
                    return

        if all(d.text() == "" for d in self.dirs_text_fields):
            self.notification.showError(self, "Error", GUILibraries.messages['no_directories'])
            return

        check_for_duplicate_path = {}
        counter = 0
        for value in self.dirs_text_fields:

            if not os.path.isdir(value.text()) and value.text().strip() != '':
                try:
                    self.notification.showError(self, "Error", GUILibraries.messages['path_not_found'] + " \n*Path: " + value.text())
                except:
                    try:
                        self.notification.showError(self, "Error", GUILibraries.messages['path_not_found'] + " \n*Path: " + value.text().decode('utf-8'))
                    except:
                        pass
                return

            for single_path in check_for_duplicate_path:
                if check_for_duplicate_path[single_path] != '' and check_for_duplicate_path[single_path] is not None:
                    if check_for_duplicate_path[single_path] == value.text():

                        self.notification.showError(self, "Error", GUILibraries.messages['duplicate_path'])
                        return

            check_for_duplicate_path[counter] = value.text()
            counter += 1

        self.Fixity = SharedApp.SharedApp.App

        if project:
            self.project = project
        else:
            try:
                self.project = self.Fixity.getSingleProject(str(self.projects.currentItem().text()))
            except:
                self.project = ProjectCore.ProjectCore()
                pass

        if self.project is None or self.project is False:
            self.project = ProjectCore.ProjectCore()
        if len(self.Fixity.ProjectsList) > 0:
            self.check_for_path_changes()
            self.checkNumberOfDirsChange()
        try:
            current_item = self.projects.currentItem().text()

            self.project.setTitle(current_item)
        except:
            pass

        is_month, is_week = 99, 99

        if self.monthly.isChecked():
                interval = 1
                is_month = int(self.day_of_month.value())
        elif self.weekly.isChecked():
                interval = 2
                is_week = int(self.day_of_week.currentIndex())
        elif self.daily.isChecked():
                interval = 3

        self.project.scheduler.setDurationType(interval)
        self.project.scheduler.setRunTime(self.timer.time().toString())
        run_only_on_ac_power = '2'

        if is_month == 99 and is_week == 99:
            run_only_on_ac_power = ''
        elif is_month == 99 and is_week != 99:
            run_only_on_ac_power = self.day_of_week.currentIndex()

        elif is_month != 99 and is_week == 99:
            run_only_on_ac_power = self.day_of_month.value()

        self.project.setEmail_address(all_email_address)
        self.project.scheduler.setRun_day_or_month(run_only_on_ac_power)

        if self.run_only_on_ac_power.isChecked():
            self.project.scheduler.setRun_when_on_battery(1)
        else:
            self.project.scheduler.setRun_when_on_battery(0)

        if self.start_when_available.isChecked():
            self.project.scheduler.setIf_missed_run_upon_restart(1)
        else:
            self.project.scheduler.setIf_missed_run_upon_restart(0)

        if self.email_only_when_something_changed.isChecked():
            self.project.scheduler.setEmail_only_upon_warning(1)
        else:
            self.project.scheduler.setEmail_only_upon_warning(0)

        if self.run_only_on_ac_power.isChecked():
            self.project.scheduler.setRun_when_on_battery(1)
        else:
            self.project.scheduler.setRun_when_on_battery(0)

        if self.start_when_available.isChecked():
            self.project.scheduler.setIf_missed_run_upon_restart(1)
        else:
            self.project.scheduler.setIf_missed_run_upon_restart(0)

        if self.start_when_available.isChecked():
            self.project.scheduler.setIf_missed_run_upon_restart(1)
        else:
            self.project.scheduler.setIf_missed_run_upon_restart(0)

        if self.email_only_when_something_changed.isChecked():
            self.project.scheduler.setEmail_only_upon_warning(1)
        else:
            self.project.scheduler.setEmail_only_upon_warning(0)

        information = {}
        information[0] = {}
        information[1] = {}
        information[2] = {}
        information[3] = {}
        information[4] = {}
        information[5] = {}
        information[6] = {}

        for n in xrange(0,self.Fixity.Configuration.getNumberOfPathDirectories()):
            path_info = self.dirs_text_fields[n].text()
            ID = 'Fixity-' + str(n+1)
            information[n]['projectID'] = self.project.getID()
            information[n]['versionID'] = self.project.getVersion()
            information[n]['path'] = path_info
            information[n]['pathID'] = ID

        self.project.setDirectories(information)
        self.project.Save()
        self.notification.showInformation(self, "Success", GUILibraries.messages['settings_saved'] + self.projects.currentItem().text())
        self.togglerMenu(False)
        self.unsaved = False
        return self.project

    def AboutFixity(self):
        self.email_notification_gui.Cancel()
        self.about_fixity_gui = AboutFixityGUI.AboutFixityGUI(self)
        self.about_fixity_gui.LaunchDialog()

    def setEmailConfiguration(self):
        self.email_notification_gui.Cancel()
        self.email_notification_gui = EmailNotificationGUI.EmailNotificationGUI(self)
        self.email_notification_gui.LaunchDialog()

    def setFilter(self):
        self.apply_filters_gui.Cancel()
        self.apply_filters_gui = ApplyFiltersGUI.ApplyFiltersGUI(self)
        self.apply_filters_gui.LaunchDialog()

    def ChangeName(self):
        self.change_name_gui.Cancel()
        self.change_name_gui = ChangeNameGUI.ChangeNameGUI(self)
        self.change_name_gui.LaunchDialog()

    def setAlgorithm(self):
        self.change_algorithm_gui.Cancel()
        self.change_algorithm_gui = ChangeAlgorithmGUI.ChangeAlgorithmGUI(self)
        self.change_algorithm_gui.LaunchDialog()

    def importOld(self):
        self.import_project_gui.Cancel()
        self.import_project_gui = ImportProjGUI.ImportProjectGUI(self)
        self.import_project_gui.LaunchDialog()

    #Day check box Click Trigger
    #(Trigger on day Check box click)
    #
    #@return: None

    def dayClick(self):
        self.changed()
        self.day_of_month.hide()
        self.day_of_week.hide()
        self.scheduler_run_on.hide()
        self.spacer.changeSize(30, 25)

    #Month check box Click Trigger
    #(Trigger on week Check box click)
    #
    #@return: None

    def weekClick(self):
        self.changed()
        self.spacer.changeSize(0, 0)
        self.day_of_month.hide()
        self.day_of_week.show()
        self.scheduler_run_on.show()
        self.scheduler_run_on.setText('Scheduler Run Every ')

    #Month check box Click Trigger
    #(Trigger on Month Check box click)
    #
    #@return: None

    def monthClick(self):
        self.changed()
        self.spacer.changeSize(0, 0)
        self.day_of_week.hide()
        self.day_of_month.show()
        self.scheduler_run_on.show()
        self.scheduler_run_on.setText('Scheduler Run On ')

    #Pick Directory
    #(Trigger on Pick Directory Button Menu)
    #
    #@return: None

    def pickDir(self):

        n = self.browse_dirs.index(self.sender())
        path_selected = GUILibraries.QFileDialog.getExistingDirectory(self, dir=self.Fixity.Configuration.getUserHomePath() + GUILibraries.os.sep + 'Desktop' + GUILibraries.os.sep)
        duplicate_path = False
        for single_index in xrange(self.Fixity.Configuration.getNumberOfPathDirectories()):
            if self.dirs_text_fields[single_index].text() == path_selected and self.dirs_text_fields[single_index].text() != '' and path_selected != '':
                duplicate_path = True

        if duplicate_path:
            self.notification.showError(self, "Error", GUILibraries.messages['duplicate_path'])
            return

        if path_selected and path_selected != '':
            self.dirs_text_fields[n].setText(path_selected)

    def removeDirs(self):
        n = self.bin_of_dirs.index(self.sender())
        self.dirs_text_fields[n].setText('')

    def toggler(self, status):
        for n in xrange(self.Fixity.Configuration.getNumberOfPathDirectories()):
            self.mail_text_fields[n].setDisabled(status)
            self.dirs_text_fields[n].setDisabled(status)
            self.bin_of_dirs[n].setDisabled(status)
            self.browse_dirs[n].setDisabled(status)
            self.lastrun.setDisabled(status)

        self.timer.setDisabled(status)
        self.monthly.setDisabled(status)
        self.weekly.setDisabled(status)
        self.daily.setDisabled(status)
        self.timer.setDisabled(status)
        self.day_of_month.setDisabled(status)
        self.day_of_week.setDisabled(status)

        try:
            self.run_only_on_ac_power.setDisabled(status)
        except:
            pass
        try:
            self.start_when_available.setDisabled(status)
        except:
            pass
        try:
            self.email_only_when_something_changed .setDisabled(status)
        except:
            pass

    #Refresh Project Settings on the main Window
    def refreshProjectSettings(self):
            self.Fixity = SharedApp.SharedApp.App
            allProjects = self.Fixity.getProjectList()

            try:
                self.projects.clear()
            except:
                pass
            try:
                if allProjects is not None:
                    if len(allProjects) > 0:
                        for p in allProjects:
                            self.projects.addItem(p)
            except:
                pass
            self.unsaved = False
# window to display test results
class Scanner(GUILibraries.QDialog):
    def __init__(self, parent_win):
        GUILibraries.QDialog.__init__(self, parent_win)
        self.setWindowModality(GUILibraries.Qt.WindowModal)
        self.setWindowTitle('Scanner Console')
        self.Fixity = SharedApp.SharedApp.App
        self.setWindowIcon(GUILibraries.QIcon(self.Fixity.Configuration.getLogoSignSmall()))
        self.lay = GUILibraries.QVBoxLayout(self)
        self.te = GUILibraries.QTextEdit(self)
        self.te.setReadOnly(True)
        self.lay.addWidget(self.te)
        self.setLayout(self.lay)
        self.resize(800, 300)
        self.show()
        self.AddText('Started Scanning ..... !')
        self._want_to_close = False

    def closeEvent(self, evnt):
            if not self._want_to_close:
                evnt.ignore()

    def AddText(self, text):
        self.te.moveCursor(GUILibraries.QTextCursor.End);
        self.te.insertPlainText (text);
        self.te.moveCursor (GUILibraries.QTextCursor.End);
        GUILibraries.QCoreApplication.processEvents()

    '''
    Distructor

    @return: None
    '''
    def destroy(self):
        del self

    '''
    Close the Dialog Box
    '''
    def Cancel(self):

        self.destroy()
        self._want_to_close = True
        self.close()