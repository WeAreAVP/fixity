# Email Preferences Setting to send eamil
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
'''
Created on Dec 5, 2013
@author: Furqan Wasi  <furqan@geekschicago.com>
'''

from PySide.QtCore import *
from PySide.QtGui import *
from os import getcwd , path, listdir, remove, walk
import sys
import time
import re
import hashlib


class AboutFixity(QDialog):
    ''' Class to manage the Filter to be implemented for the files with specific extensions '''

    def __init__(self):
        QDialog.__init__(self)
        self.AboutFixityWin = QDialog()
        self.AboutFixityWin.setWindowTitle('Filter File')
        self.AboutFixityWin.setWindowIcon(QIcon(path.join(getcwd(), 'images\\logo_sign_small.png')))
        self.AboutFixityLayout = QVBoxLayout()

    # Distructor
    def destroyAboutFixity(self):
        del self

    def CreateWindow(self):
        self.AboutFixityWin = QDialog()

    def GetWindow(self):
        return self.AboutFixityWin

    def ShowDialog(self):
        self.AboutFixityWin.show()
        self.AboutFixityWin.exec_()


    def SetLayout(self, layout):
        self.AboutFixityLayout = layout

    def SetWindowLayout(self):
        self.AboutFixityWin.setLayout(self.AboutFixityLayout)

    def GetLayout(self):
        return self.AboutFixityLayout

    # All design Management Done in Here
    def SetDesgin(self):
        counter = 0
        self.options = QGroupBox("")
        self.information = QGroupBox("")
        self.GetLayout().addStrut(200)

        self.DescriptionBtn = QPushButton('Description')
        self.AuthorandLicenseBtn = QPushButton('Author and License')
        self.ContactBtn = QPushButton('Contact')

        self.options.addWidget(self.DescriptionBtn)
        self.options.addWidget(self.AuthorandLicenseBtn)
        self.options.addWidget(self.ContactBtn)


        self.descriptionName = QTextEdit()
        self.descriptionDescription = QTextEdit()
        self.information.addWidget(self.descriptionName)
        self.information.addWidget(self.descriptionDescription)

        self.projectSelected = QLineEdit()
        self.setInformation = QPushButton("Start Importing")

        self.projectSelected.setPlaceholderText("Project Path")

        self.projectSelected.setMaximumSize(200, 100)

        self.setInformation.setMaximumSize(200, 100)

        self.GetLayout().addWidget(self.options)
        self.GetLayout().addWidget(self.information)


        self.projectSelected.setDisabled(True)
        self.SetWindowLayout()

    # close the dailog box
    def Cancel(self):
        self.destroyAboutFixity()
        self.AboutFixityWin.close()


# Main Code
#app = QApplication('asdas')
#w = AboutFixity()
#w.CreateWindow()
#w.SetWindowLayout()
#w.SetDesgin()
#w.ShowDialog()
#app.exec_()
