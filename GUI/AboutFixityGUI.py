# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''

from GUI import GUILibraries
from Core import SharedApp
import GUI.messages as singleMessage

OS_Info = 'Windows'

''' Class to manage the Filter to be implemented for the files with specific extensions '''


class AboutFixityGUI(GUILibraries.QDialog):
    
      
    ''' Class to manage the Filter to be implemented for the files with specific extensions '''
    
    '''Contstructor'''
    def __init__(self, parent_win):

        GUILibraries.QDialog.__init__(self, parent_win)
        self.Fixity = SharedApp.SharedApp.App

        self.setWindowTitle('About Fixity')
        
        self.parent_win = parent_win
        self.setWindowModality(GUILibraries.Qt.WindowModal)
        
        self.parent_win.setWindowTitle('About Fixity')
        singleMessage.version = self.Fixity.Configuration.getApplicationVersion()
        
        self.setWindowIcon(GUILibraries.QIcon(self.Fixity.Configuration.getLogoSignSmall()))
        self.AboutFixityLayout =GUILibraries.QVBoxLayout()

        self.widget = GUILibraries.QWidget(self)
        self.pgroup = GUILibraries.QGroupBox()
        self.detail_layout = GUILibraries.QVBoxLayout()

        self.description_btn = GUILibraries.QPushButton('Description')
        self.author_and_license_btn = GUILibraries.QPushButton('Author and License')
        self.contact_btn = GUILibraries.QPushButton('Contact')
        self.close_btn = GUILibraries.QPushButton('Close')

        self.about_layout =GUILibraries.QGroupBox()
        self.heading = GUILibraries.QTextEdit()
        self.content = GUILibraries.QTextEdit()

        self.heading.setReadOnly(True)
        self.content.setReadOnly(True)

        self.main = GUILibraries.QHBoxLayout()
        self.notification = GUILibraries.NotificationGUI.NotificationGUI()

    def destroy(self):
        ''' Distructor'''
        del self

    def ShowDialog(self):
        ''' Show Dialog'''
        self.show()
        self.exec_()

    def SetLayout(self, layout):
        ''' Set Layout'''
        self.AboutFixityLayout = layout

    def showDescription(self):
        ''' Show Description'''
        self.heading.setText(singleMessage.messages['description_heading'])
        descriptionText = singleMessage.messages['description_Content']

        self.content.setText(descriptionText)
        self.description_btn.setDisabled(True)
        self.author_and_license_btn.setDisabled(False)
        self.contact_btn.setDisabled(False)
    def showLicense(self):
        ''' Show License Information On About Us Page(Trigger in  button press)'''
        self.heading.setText(singleMessage.messages['License_heading'])
        ''' Header Detail '''
        LicenseText = singleMessage.messages['License_Content']

        self.content.setText(LicenseText)
        self.description_btn.setDisabled(False)
        self.author_and_license_btn.setDisabled(True)
        self.contact_btn.setDisabled(False)

    def showContact(self):
        '''Trigger The Show Contact'''
        self.heading.setText(singleMessage.messages['Contact_heading'])
        ContactText = singleMessage.messages['Contact_Content']

        self.content.setText(ContactText)
        self.description_btn.setDisabled(False)
        self.author_and_license_btn.setDisabled(False)
        self.contact_btn.setDisabled(True)

    def SetDesgin(self):
        ''' All design Management Done in Here'''
        try:
            self.description_btn.setFixedSize(210, 30)
            self.author_and_license_btn.setFixedSize(210, 30)
            self.contact_btn.setFixedSize(210, 30)
        except:
            self.description_btn =GUILibraries.QPushButton('Description')
            self.author_and_license_btn =GUILibraries.QPushButton('Author and License')
            self.contact_btn =GUILibraries.QPushButton('Contact')
            self.close_btn =GUILibraries.QPushButton('Close')

        pic =GUILibraries.QLabel(self)
        pic.setGeometry(30, 30, 500, 600)
        pic.setFixedSize(400,400)

        '''use full ABSOLUTE path to the image, not relative'''

        pic.setPixmap(GUILibraries.QPixmap(self.Fixity.Configuration.getLogoSignSmall()))

        self.description_btn.clicked.connect(self.showDescription)
        self.author_and_license_btn.clicked.connect(self.showLicense)
        self.contact_btn.clicked.connect(self.showContact)
        self.close_btn.clicked.connect(self.Cancel)

        self.detail_layout.addWidget(self.description_btn)
        self.detail_layout.addWidget(self.author_and_license_btn)
        self.detail_layout.addWidget(self.contact_btn)
        self.detail_layout.addWidget(pic)
        self.pgroup.setLayout(self.detail_layout)

        slay =GUILibraries.QVBoxLayout()
        if OS_Info == 'Windows':
            self.heading.setFixedSize(485,40)
            self.content.setFixedSize(485,500)
        else:
            self.heading.setFixedSize(500,40)
            self.content.setFixedSize(500,500)

        slay.addWidget(self.heading)
        slay.addWidget(self.content)
        self.close_btn.setFixedSize(200,30)
        slay.addWidget(self.close_btn)
        if OS_Info == 'Windows':
            self.about_layout.setFixedSize(495, 600)
        else:
            self.about_layout.setFixedSize(540, 600)
        self.pgroup.setFixedSize(255, 600)
        self.main.addWidget(self.pgroup)
        self.main.addWidget(self.about_layout)

        self.about_layout.setLayout(slay)
        self.setLayout(self.main)
        self.showDescription()

    def Cancel(self):
        """
        Close the Dialog Box
        @return:
        """

        try:self.Fixity = SharedApp.SharedApp.App
        except:pass
        self.parent_win.setWindowTitle("Fixity "+self.Fixity.Configuration.getApplicationVersion())
        self.destroy()
        self.close()

    def LaunchDialog(self):
        """
        Launch Dialog

        @return:
        """
        self.SetDesgin()
        self.ShowDialog()

