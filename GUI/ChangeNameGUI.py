# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''
from GUI import GUILibraries
from Core import SharedApp


# Class to manage the the Name of the project,  ChangeName class manages the action of name changing and also updating the scheduler and other information changed '''

class ChangeNameGUI(GUILibraries.QDialog ):

    # Contstructor'''
    def __init__(self, parent_win):
        super(ChangeNameGUI,self).__init__(parent_win)
        self.Fixity = SharedApp.SharedApp.App
        self.parent_win = parent_win

        self.setWindowModality(GUILibraries.Qt.WindowModal)        
        self.setWindowTitle('Change Project Name')
        self.parent_win.setWindowTitle('Change Project Name')
        self.setWindowIcon(GUILibraries.QIcon(r''+(str((self.Fixity.Configuration.getLogoSignSmall())))))
        self.change_name_layout = GUILibraries.QVBoxLayout()
        self.notification = GUILibraries.NotificationGUI.NotificationGUI()

    #  Distructor'''
    def destroyChangeName(self):
        del self  
        
        
    # QDailog Reject Tigger over writen'''
    def reject(self):

        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        self.parent_win.setWindowTitle("Fixity "+self.Fixity.Configuration.getApplicationVersion())
        super(ChangeNameGUI,self).reject()
        

    
    # Show this Dialog'''
    def ShowDialog(self):     
        self.show()
        self.exec_()

    def destroy(self):
        del self
        
    # Set  Layout '''
    def SetLayout(self, layout):
        self.change_name_layout = layout

    # Set  Layout '''
    def GetLayout(self):
        return self.change_name_layout

    # Set Window Layout'''
    def SetWindowLayout(self):
        self.setLayout(self.change_name_layout)
        
    # All design Management Done in here  got the Change Name
    def SetDesgin(self):

        isEnable = True
        project_list = self.Fixity.getProjectList()
        if len(project_list) <= 0:
            isEnable = False
            project_list.append('Create & Save Project')
        self.GetLayout().addStrut(200)
        self.projects = GUILibraries.QComboBox()
        self.projects.addItems(project_list)

        self.GetLayout().addWidget(self.projects)
        self.change_name_field =GUILibraries.QLineEdit()
        self.set_information =GUILibraries.QPushButton("Save && Close")
        
        self.cancel =GUILibraries.QPushButton("Close Without Saving")
        
        self.change_name_field.setPlaceholderText("Add New Name")
        
        self.GetLayout().addWidget(self.change_name_field)
        self.GetLayout().addWidget(self.set_information)
        
        self.GetLayout().addWidget(self.cancel)
        
        self.set_information.clicked.connect(self.Save)
        
        self.cancel.clicked.connect(self.Cancel)
        self.projects.currentIndexChanged .connect(self.project_changed)
        if not isEnable:
            self.set_information.setDisabled(True)
            self.change_name_field.setDisabled(True)
            self.projects.setDisabled(True)
            
        self.SetWindowLayout()
        self.project_changed()

    def Save(self):

        if self.change_name_field.text() == '' and self.change_name_field.text() is None:
            self.notification.showError(self, "Failure", GUILibraries.messages['no_project_selected'])
            return

        selected_project = self.projects.currentText()
        is_project_name_valid = self.Fixity.Validation.ValidateProjectName(self.change_name_field.text())

        if not is_project_name_valid:
            self.notification.showError(self, "Failure", str(GUILibraries.messages['in_valid_project_name']))
            return

        is_this_name_already_taken = False

        if is_this_name_already_taken:
            self.notification.showWarning(self, "Failure", GUILibraries.messages['project_already_selected'])
            return

        if False:
            self.notification.showInformation(self, "Failure", GUILibraries.messages['problem_proj_name_change'])
            return

        new_name = self.change_name_field.text()

        try:
            project_exists = self.Fixity.ProjectsList[str(new_name)]
            project_exists.getID()
            project_exists.getTitle()
            self.notification.showInformation(self, "Failure", GUILibraries.messages['in_valid_project_name_detailed'])
            return
        except:
            pass

        project_core = self.Fixity.ProjectsList[selected_project]
        flag_name_changed = project_core.changeProjectName(selected_project, new_name)

        if flag_name_changed:
            currentRow = self.parent_win.projects.currentRow()
            self.notification.showInformation(self, "Success", GUILibraries.messages['project_name_changed'])
            self.parent_win.refreshProjectSettings()
            self.parent_win.projects.setCurrentRow(currentRow)
            self.Cancel()
        else:
            self.notification.showInformation(self, "Failure", GUILibraries.messages['in_valid_project_name_detailed'])
            return


    def project_changed(self):
        project_changed = ''

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