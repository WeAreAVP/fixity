


# Email Preferences Setting to send eamil
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
'''
Created on Dec 5, 2013
@author: Furqan Wasi  <furqan@geekschicago.com>
'''
import os
OS_Info = ''
if os.name == 'posix':
    OS_Info = 'linux'
elif os.name == 'nt':
    OS_Info = 'Windows'
elif os.name == 'os2':
    OS_Info = 'check'

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
        self.AboutFixityWin.setWindowTitle('About Fixity')
        self.AboutFixityWin.setWindowIcon(QIcon(path.join(getcwd(), 'images' + str(os.sep) + 'logo_sign_small.png')))
        self.AboutFixityLayout = QVBoxLayout()

        self.widget = QWidget(self)
        self.pgroup = QGroupBox()
        self.play = QVBoxLayout()

        self.DescriptionBtn = QPushButton('Description')
        self.AuthorandLicenseBtn = QPushButton('Author and License')
        self.ContactBtn = QPushButton('Contact')
        self.CloseBtn = QPushButton('Close')
        self.sch = QGroupBox()
        self.monthly = QTextEdit()
        self.weekly = QTextEdit()
        self.main = QHBoxLayout()

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


    def GetLayout(self):
        return self.AboutFixityLayout

    def showDescription(self):
        self.monthly.setText('<h1>Description</h1>')
        self.weekly.setText('This is description Bitch')
        self.DescriptionBtn.setDisabled(True)
        self.AuthorandLicenseBtn.setDisabled(False)
        self.ContactBtn.setDisabled(False)


    def showLicense(self):
        self.monthly.setText('<h1>Author and License </h1>')
        self.weekly.setText('This is Author and License Bitch')
        self.DescriptionBtn.setDisabled(False)
        self.AuthorandLicenseBtn.setDisabled(True)
        self.ContactBtn.setDisabled(False)

    def showContact(self):
        self.monthly.setText('<h1>Contact</h1>')
        self.weekly.setText('This is Contact Bitch')
        self.DescriptionBtn.setDisabled(False)
        self.AuthorandLicenseBtn.setDisabled(False)
        self.ContactBtn.setDisabled(True)

    # All design Management Done in Here
    def SetDesgin(self):

        self.DescriptionBtn.setFixedSize(210, 30)
        self.AuthorandLicenseBtn.setFixedSize(210, 30)
        self.ContactBtn.setFixedSize(210, 30)

        pic = QLabel(self.AboutFixityWin)
        pic.setGeometry(30, 30, 500, 600)
        pic.setFixedSize(400,400)
        #use full ABSOLUTE path to the image, not relative
        pic.setPixmap(QPixmap(path.join(getcwd(), 'images'+str(os.sep)+'audiovisual.jpg')))

        self.DescriptionBtn.clicked.connect(self.showDescription)
        self.AuthorandLicenseBtn.clicked.connect(self.showLicense)
        self.ContactBtn.clicked.connect(self.showContact)
        self.CloseBtn.clicked.connect(self.Cancel)

        self.play.addWidget(self.DescriptionBtn)
        self.play.addWidget(self.AuthorandLicenseBtn)
        self.play.addWidget(self.ContactBtn)
        self.play.addWidget(pic)
        self.pgroup.setLayout(self.play)

        slay = QVBoxLayout()
        self.monthly.setFixedSize(570,40)
        self.weekly.setFixedSize(570,500)
        slay.addWidget(self.monthly)
        slay.addWidget(self.weekly)
        self.CloseBtn.setFixedSize(200,30)
        slay.addWidget(self.CloseBtn)



        self.sch.setFixedSize(600, 600)
        self.pgroup.setFixedSize(255, 600)
        self.main.addWidget(self.pgroup)
        self.main.addWidget(self.sch)

        self.sch.setLayout(slay)
        self.AboutFixityWin.setLayout(self.main)
        self.showDescription()


    # close the dailog box
    def Cancel(self):
        self.destroyAboutFixity()
        self.AboutFixityWin.close()

# Main Code
#app = QApplication('asdas')
#w = AboutFixity()
#w.CreateWindow()
#w.SetDesgin()
#w.ShowDialog()
#app.exec_()
