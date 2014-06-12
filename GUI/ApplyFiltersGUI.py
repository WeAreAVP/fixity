# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014
@author: Furqan <furqan@geekschicago.com>
'''

from GUI import GUILibraries
from Core import SharedApp
__author__ = 'Furqan'


#Class to manage the Filter to be implemented for the files with specific extensions

class ApplyFiltersGUI(GUILibraries.QDialog):

    '''
            Constructor
    '''
    def __init__(self,parent_win):

        GUILibraries.QDialog.__init__(self,parent_win)
        self.Fixity = SharedApp.SharedApp.App

        self.parent_win = parent_win
        self.setWindowModality(GUILibraries.Qt.WindowModal)
        self.parent_win.setWindowTitle('Filter File')
        self.setWindowTitle('Filter File')
        self.setWindowIcon(GUILibraries.QIcon(r''+(str((self.Fixity.Configuration.getLogoSignSmall())))))
        self.filter_files_layout = GUILibraries.QVBoxLayout()
        self.notification = GUILibraries.NotificationGUI.NotificationGUI()


    '''
        catch Reject even of the Dialog box
    '''
    def reject(self):

        self.parent_win.setWindowTitle("Fixity "+self.Fixity.Configuration.getApplicationVersion())
        super(ApplyFiltersGUI,self).reject()


    '''
        Distructor
    '''
    def destroy(self):
        del self


    '''
    Get Window of this
    '''
    def GetWindow(self):
        return self.FilterFilesWin

    '''
    Get Window of this
    '''
    def ShowDialog(self):
        self.show()
        self.exec_()

    '''
    Set Layout
    '''
    def SetLayout(self, layout):
        self.filter_files_layout = layout

    '''
    Set Window Layout
    '''
    def SetWindowLayout(self):
        self.setLayout(self.filter_files_layout)

    '''
    Get Layout
    '''
    def GetLayout(self):
        return self.filter_files_layout

    '''
     All design Management Done in Here
    '''
    def SetDesgin(self):

        counter = 0
        isEnable = True
        project_list = self.Fixity.getProjectList()

        if len(project_list) <= 0:
            isEnable = False
            project_list.append('Create & Save Project')


        self.GetLayout().addStrut(200)
        self.projects = GUILibraries.QComboBox()
        self.projects.addItems(project_list)
        self.scheduling_groupBox =GUILibraries.QGroupBox("Scheduling")
        self.GetLayout().addWidget(self.projects)
        self.filter_field = GUILibraries.QLineEdit()
        self.setInformation =GUILibraries.QPushButton("Save && Close")
        self.reset = GUILibraries.QPushButton("Reset")
        self.cancel = GUILibraries.QPushButton("Close Without Saving")

        self.filter_field.setPlaceholderText("Add Filter")

        self.ignore_hidden_files = GUILibraries.QCheckBox("Ignore Hidden Files")


#         if OS_Info == 'linux':
        self.GetLayout().addWidget(self.ignore_hidden_files)
        self.GetLayout().addWidget(self.filter_field)
        self.GetLayout().addWidget(self.setInformation)
        self.GetLayout().addWidget(self.reset)
        self.GetLayout().addWidget(self.cancel)

        if not isEnable:
            self.setInformation.setDisabled(True)
            self.reset.setDisabled(True)
            self.projects.setDisabled(True)
            self.filter_field.setDisabled(True)
            self.ignore_hidden_files.setDisabled(True)

        self.setInformation.clicked.connect(self.Save)
        self.reset.clicked.connect(self.Reset)
        self.cancel.clicked.connect(self.Cancel)

        self.projects.currentIndexChanged .connect(self.projectChanged)
        self.SetWindowLayout()
        self.projectChanged()

    ''' Reset Text of Filters '''
    def Reset(self):
        self.filter_field.setText('')
        self.ignore_hidden_files.setChecked(False)

    def Save(self):

        selected_project = self.projects.currentText()
        filters = self.filter_field.text()
        Is_ignore_hidden_files = self.ignore_hidden_files.isChecked()

        if selected_project == '':
            self.notification.showError(self, "No Project Selected", GUILibraries.messages['no_project_selected'])
            return
        flag = True
        project_core = self.Fixity.ProjectRepo.getSingleProject(selected_project)
        project_core.applyFilter(filters, Is_ignore_hidden_files)
        SharedApp.SharedApp.App = self.Fixity
        if flag is not None:
            self.notification.showInformation(self, "Success", GUILibraries.messages['filter_success'])
            self.Cancel()
            return
        else:
            self.notification.showError(self, "Failure", GUILibraries.messages['filter_fail'])

    '''
    Triggers on project changed from drop down and sets related information in filters Field
    '''
    def projectChanged(self):
        selected_project = self.projects.currentText()
        project_core = self.Fixity.ProjectRepo.getSingleProject(selected_project)
        try:
            filters = project_core.getFilters()
            ignore_hidden_files = project_core.getIgnore_hidden_file()

            self.filter_field.setText(filters)

            if ignore_hidden_files == 1 or ignore_hidden_files == '1':
                self.ignore_hidden_files.setChecked(True)
            else:
                self.ignore_hidden_files.setChecked(False)
        except:
            pass

        return

    '''
    Close the Dialog Box
    '''
    def Cancel(self):
        self.parent_win.setWindowTitle("Fixity "+self.Fixity.Configuration.getApplicationVersion())
        self.destroy()
        self.close()

    # Launch Dialog
    def LaunchDialog(self):

        self.SetDesgin()
        self.ShowDialog()

#app = GUILibraries.QApplication('sadas')
#w = ApplyFilters(GUILibraries.QDialog())
#w.SetWindowLayout()
#w.SetDesgin()
#w.ShowDialog()
#exit(app.exec_())