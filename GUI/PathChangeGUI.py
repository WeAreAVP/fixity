# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014
@author: Furqan <furqan@geekschicago.com>
'''

from GUI import GUILibraries
from Core import SharedApp

__author__ = 'Furqan'

# Class to manage the Filter to be implemented for the files with specific extensions


class PathChangeGUI(GUILibraries.QDialog):
    def __init__(self,parent_win,  orignal_path_text ='', change_path_text = '', code = ''):
        GUILibraries.QDialog.__init__(self,parent_win)
        self.Fixity = SharedApp.SharedApp.App
        self.parent_win = parent_win
        self.path_change_win = GUILibraries.QDialog(self.parent_win)
        self.path_change_win.setWindowModality(GUILibraries.Qt.WindowModal)
        self.path_change_win.setWindowTitle('Change Directory')
        self.setWindowIcon(GUILibraries.QIcon(r''+(str((self.Fixity.Configuration.getLogoSignSmall())))))
        self.path_change_layout = GUILibraries.QVBoxLayout()
        self.orignal_path_text = orignal_path_text
        self.change_path_text = change_path_text
        self.code = code
        self.notification = GUILibraries.NotificationGUI.NotificationGUI()

    '''
    Distructor

    @return: None
    '''
    def destroy(self):
        del self

    '''
    Create Window

    @return: None
    '''
    def CreateWindow(self):
        self.path_change_win = GUILibraries.QDialog()


    '''
    Get this Window

    @return: None
    '''
    def GetWindow(self):
        return self.path_change_win

    '''
    Show Dialog

    @return: None
    '''
    def ShowDialog(self):
        self.path_change_win.show()
        self.path_change_win.exec_()
    '''
    Set Layout

    @return: None
    '''
    def SetLayout(self, layout):
        self.path_change_layout = layout

    '''
    Get Layout

    @return: None
    '''
    def GetLayout(self):
        return self.path_change_layout

    '''
    Set Window Layout

    @return: None
    '''
    def SetWindowLayout(self):
        self.path_change_win.setLayout(self.path_change_layout)

    '''
    Close Click

    @return: None
    '''
    def CloseClick(self):
        self.parent_win.setWindowTitle("Fixity "+self.Fixity.Configuration.getApplicationVersion())
        self.change_the_path_information = False
        if self.code >=0:
            try:
                self.parent_win.dirs_text_fields[(int(self.code) - 1)].setText(str(self.orignal_path_text))
            except:
                pass

        self.path_change_win.close()

    '''
    Destroy window Information

    @return: None
    '''
    def DestroyEveryThing(self):
        self.destroy()
        self.path_change_win.close()


    '''
    All design Management Done in Here

    @return: None
    '''

    def SetDesgin(self):

        self.GetLayout().addStrut(400)

        # Initializing view elements
        self.orignalPathLable = GUILibraries.QLabel()
        self.changePathToLable = GUILibraries.QLabel()
        self.setInformation = GUILibraries.QPushButton("&Orignal Path Information")
        self.setInformation = GUILibraries.QPushButton("&Change Path")
        self.cancel = GUILibraries.QPushButton("Do Not Change Path")
        self.orignalPath = GUILibraries.QTextEdit()
        self.changePathTo = GUILibraries.QTextEdit()


        # Set view text
        self.orignalPath.setText(self.orignal_path_text)
        self.changePathTo.setText(self.change_path_text)
        self.orignalPathLable.setText('Change Path From')
        self.changePathToLable.setText('To')
        self.orignalPath.setDisabled(True)
        self.changePathTo.setDisabled(True)

        # Styling
        self.orignalPath.setMaximumSize(400, 100)
        self.changePathTo.setMaximumSize(400, 100)
        self.cancel.setMaximumSize(200, 100)
        self.setInformation.setMaximumSize(200, 100)

        # Set Widget to layouts
        self.GetLayout().addWidget(self.orignalPathLable)
        self.GetLayout().addWidget(self.orignalPath)
        self.GetLayout().addWidget(self.changePathToLable)
        self.GetLayout().addWidget(self.changePathTo)
        self.GetLayout().addWidget(self.setInformation)
        self.GetLayout().addWidget(self.cancel)

        # Set triggers
        self.setInformation.clicked.connect(self.changeRootDirInfo)
        self.cancel.clicked.connect(self.CloseClick)
        self.SetWindowLayout()


    #Points out to change the Path of Manifest or not
    #
    #@return: None

    def changeRootDirInfo(self):
        if not GUILibraries.os.path.exists(self.change_path_text):

            self.notification.showWarning(self,'Path Dose Not Exists' ,self.change_path_text + GUILibraries.messages['dir_dnt_exists'])
            self.change_the_path_information = False

        else:
            if (self.orignal_path_text is not None and self.change_path_text is not None) and (self.orignal_path_text != '' and self.change_path_text != ''):
                self.change_the_path_information = True
            else:
                self.change_the_path_information = False
        self.path_change_win.close()

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
#w = PathChange(GUILibraries.QDialog())
#w.SetWindowLayout()
#w.SetDesgin()
#w.ShowDialog()
#app.exec_()