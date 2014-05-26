'''
Created on May 14, 2014
@author: Furqan <furqan@geekschicago.com>
'''

import GUILibraries
from Core import SharedApp, ProjectCore

# Class to manage the Filter to be implemented for the files with specific extensions


class ImportProjectGUI(GUILibraries.QDialog):

    '''Constructor '''
    def __init__(self, parent_win):

        GUILibraries.QDialog.__init__(self,parent_win)
        self.Fixity = SharedApp.SharedApp.App
        self.parent_win = parent_win
        self.setWindowModality(GUILibraries.Qt.WindowModal)
        self.parent_win.setWindowTitle('Import Project')
        self.setWindowTitle('Import Project')
        self.setWindowIcon(GUILibraries.QIcon(r''+(str((self.Fixity.Configuration.getLogoSignSmall())))))
        self.import_projects_layout = GUILibraries.QVBoxLayout()
        self.project_list_widget = None
        self.notification = GUILibraries.NotificationGUI.NotificationGUI()
    '''
    Distructor
    '''
    def destroy(self):
        del self


    '''
    Get Window
    '''
    def GetWindow(self):
        return self
    '''
    Show Dialog
    '''
    def ShowDialog(self):
        self.show()
        self.exec_()

    '''
    Set Layout
    '''
    def SetLayout(self, layout):
        self.import_projects_layout = layout

    '''
    Set Window Layout
    '''
    def SetWindowLayout(self):
        self.setLayout(self.import_projects_layout)

    '''
    Get Layout
    '''
    def GetLayout(self):
        return self.import_projects_layout

    '''
    All design Management Done in Here
    '''
    def SetDesgin(self):
        self.GetLayout().addStrut(200)
        self.projects = GUILibraries.QPushButton('Select Project')

        self.project_selected = GUILibraries.QTextEdit()
        self.projects.clicked.connect(self.pickDir)


        self.GetLayout().addWidget(self.projects)
        self.project_selected = GUILibraries.QLineEdit()
        self.set_information = GUILibraries.QPushButton("Import")
        self.cancel = GUILibraries.QPushButton("Close Without Saving")

        self.project_selected.setPlaceholderText("Project Path")

        self.GetLayout().addWidget(self.project_selected)
        self.GetLayout().addWidget(self.set_information)

        self.GetLayout().addWidget(self.cancel)

        self.set_information.clicked.connect(self.ImportInformation)

        self.cancel.clicked.connect(self.Cancel)
        self.project_selected.setDisabled(True)
        self.SetWindowLayout()

    '''
    Over ride reject QDialog Trigger
    '''
    def reject(self):
        self.parent_win.setWindowTitle("Fixity "+self.Fixity.Configuration.getApplicationVersion())
        super(ImportProjectGUI,self).reject()

    '''
    Pick Directory

    @return: None
    '''
    def pickDir(self):
        path = self.Fixity.Configuration.getBasePath()
        fileInformation  = list(GUILibraries.QFileDialog.getOpenFileName(self,"Select File",str(path)))
        self.project_selected.setText(str(fileInformation[0]))


    '''
    Reset form
    @return: None
    '''
    def Reset(self):
        self.project_selected.setText('')


    def ImportInformation(self):

        project_core = ProjectCore.ProjectCore()
        file_path = str(self.project_selected.text())

        if file_path is None or file_path == '':
            return 'select_manifest_file'

        flag_is_a_tsv_file = False
        flag_is_a_fxy_file = False

        file_name = str(GUILibraries.os.path.basename(file_path))

        if '.tsv' in file_name:
            flag_is_a_tsv_file = True

        if '.fxy' in file_name:
            flag_is_a_fxy_file = True

        if not flag_is_a_fxy_file and not flag_is_a_tsv_file:
            self.notification.showError(self, 'Invalid Name', GUILibraries.messages['invalid_file_given'])
            return

        QID = GUILibraries.QInputDialog(self)
        QID.setWindowModality(GUILibraries.Qt.WindowModal)
        name = QID.getText(self, "Project Name", "Name for new Fixity project:", text="New_Project")

        if not name[1]:
            self.notification.showError(self, 'Invalid Name', GUILibraries.messages['in_valid_project_name'])
            return

        file_name = name[0]

        responseName = self.Fixity.Validation.ValidateProjectName(file_name)
        if not responseName:
            self.notification.showError(self, 'Invalid Name', GUILibraries.messages['in_valid_project_name'])
            return

        Project = self.Fixity.ProjectRepo.getSingleProject(str(file_name))

        if Project != False:
            self.notification.showError(self, 'Invalid Name', GUILibraries.messages['project_already_selected'])
            return

        self.setWindowTitle('Importing Project ....')
        self.parent_win.setWindowTitle('Importing Project ....')

        if project_core.ImportProject(self.project_selected.text(), file_name, flag_is_a_tsv_file, flag_is_a_fxy_file):
            self.notification.showInformation(self, 'Invalid Name', GUILibraries.messages['project_imported_sccuessfully'])
        self.parent_win.refreshProjectSettings()
        self.parent_win.toggler(False)
        self.Cancel()

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

#app = GUILibraries.QApplication('asdas')
#w = ImportProjectGUI(GUILibraries.QDialog())
#w.SetWindowLayout()
#w.SetDesgin()
#w.ShowDialog()
#exit(app.exec_())