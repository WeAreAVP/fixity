# Base Path Directory Changed
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

'''
Created on Feb 4, 2014
@author: Furqan Wasi <furqan@geekschicago.com>
'''
# Fixity Scheduler
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0


import base64
from os import getcwd  , path
from PySide.QtCore import *
from PySide.QtGui import *

import os

''' Class to manage all the the errors and warning loging'''
class FileChanged(QDialog):


    # Constuctor
    def __init__(self , orignalPathText ='', changePathText = '' ):
        self.FileChangedWin = QDialog()
        self.FileChangedWin.setWindowTitle('Change Directory')
        self.FileChangedWin.setWindowIcon(QIcon(path.join(getcwd(), 'images'+str(os.sep)+'logo_sign_small.png')))
        self.FileChangedLayout = QVBoxLayout()
        self.version = '0.4'
        self.orignalPathText = orignalPathText
        self.changePathText = changePathText
        self.changeThePathInformation = False
        self.ReplacementArray ={}

    # Distructor
    def destroyFileChanged(self):
        del self

    # Get Version
    def getVersion(self):
        return self.version

    # Set Version
    def setVersion(self,version):
        return self.version

    # Create Window
    def CreateWindow(self):
        self.FileChangedWin = QDialog()

    # Get this Window
    def GetWindow(self):
        return self.FileChangedWin

    # Show Dialog
    def ShowDialog(self):
        self.FileChangedWin.show()
        self.FileChangedWin.exec_()

    # Set Layout
    def SetLayout(self, layout):
        self.FileChangedLayout = layout

    # Get Layout
    def GetLayout(self):
        return self.FileChangedLayout

    # Set Window Layout
    def SetWindowLayout(self):
        self.FileChangedWin.setLayout(self.FileChangedLayout)

    # Close Click
    def CloseClick(self):
        self.changeThePathInformation = False
        self.FileChangedWin.close()

    # Destroy window Information
    def DestroyEveryThing(self):
        self.destroyFileChanged()
        self.FileChangedWin.close()

    # All design Management Done in Here
    def SetDesgin(self):



        self.GetLayout().addStrut(400)

        #initializing view elements
        self.orignalPathLable = QLabel()
        self.changePathToLable = QLabel()
        self.setInformation = QPushButton("&Orignal Path Information")
        self.setInformation = QPushButton("&Change Path")
        self.cancel = QPushButton("Close")
        self.orignalPath = QTextEdit()
        self.changePathTo = QTextEdit()


        #Set view text
        self.orignalPath.setText(self.orignalPathText)
        self.changePathTo.setText(self.changePathText)
        self.orignalPathLable.setText('Change Path From')
        self.changePathToLable.setText('To')
        self.orignalPath.setDisabled(True)
        self.changePathTo.setDisabled(True)

        #Styling
        self.orignalPath.setMaximumSize(400, 100)
        self.changePathTo.setMaximumSize(400, 100)
        self.cancel.setMaximumSize(200, 100)
        self.setInformation.setMaximumSize(200, 100)

        #set Widget to layouts
        self.GetLayout().addWidget(self.orignalPathLable)
        self.GetLayout().addWidget(self.orignalPath)
        self.GetLayout().addWidget(self.changePathToLable)
        self.GetLayout().addWidget(self.changePathTo)
        self.GetLayout().addWidget(self.setInformation)
        self.GetLayout().addWidget(self.cancel)

        #set triggers
        self.setInformation.clicked.connect(self.changeRootDirInfo)
        self.cancel.clicked.connect(self.CloseClick)
        self.SetWindowLayout()

    #Points out to change the Path of Manifest or not
    def changeRootDirInfo(self):
        if not path.exists(self.changePathText):
            msgBox = QMessageBox();
            msgBox.setText(self.changePathText + ' does not exist.\nPlease provide a valid path and try again.')
            msgBox.exec_()
            self.changeThePathInformation = False
        else:
            if (self.orignalPathText != None and self.changePathText != None) and (self.orignalPathText != '' and self.changePathText != ''):
                self.changeThePathInformation = True
            else:
                self.changeThePathInformation = False
        self.FileChangedWin.close()

