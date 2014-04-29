# -- coding: utf-8 --
# Base Path Directory Changed
# Version 0.4, Apr 1, 2014
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

'''
Created on Feb 4, 2014
@author: Furqan Wasi <furqan@geekschicago.com>
'''

# Custom Library
import base64
from os import getcwd  , path
from PySide.QtCore import *
from PySide.QtGui import *

import os

''' Class to manage if any Change in Base path of any given project, the action occurs when saving the project information'''
class FileChanged(QDialog):


    '''
    Constuctor
    
    @return: None  
    ''' 
    def __init__(self,parentWin , orignalPathText ='', changePathText = '' ):
        self.parentWin = parentWin
        self.FileChangedWin = QDialog(self.parentWin)
        self.FileChangedWin.setWindowModality(Qt.WindowModal)
        self.FileChangedWin.setWindowTitle('Change Directory')
        self.FileChangedWin.setWindowIcon(QIcon(path.join(getcwd(), 'images'+str(os.sep)+'logo_sign_small.png')))
        self.FileChangedLayout = QVBoxLayout()
        self.version = '0.4'
        self.orignalPathText = orignalPathText
        self.changePathText = changePathText
        self.changeThePathInformation = False
        self.ReplacementArray ={}
        

    '''
    Distructor
    
    @return: None  
    ''' 
    def destroyFileChanged(self):
        del self

    ''''
    Get Version
    
    @return: None  
    ''' 
    def getVersion(self):
        return self.version

    '''
    Set Version
    
    @return: None  
    ''' 
    def setVersion(self,version):
        return self.version

    '''
    Create Window
    
    @return: None  
    ''' 
    def CreateWindow(self):
        self.FileChangedWin = QDialog()
        

    '''
    Get this Window
    
    @return: None  
    ''' 
    def GetWindow(self):
        return self.FileChangedWin

    '''
    Show Dialog
    
    @return: None  
    ''' 
    def ShowDialog(self):
        self.FileChangedWin.show()
        self.FileChangedWin.exec_()
    '''
    Set Layout
    
    @return: None  
    ''' 
    def SetLayout(self, layout):
        self.FileChangedLayout = layout
        
    '''
    Get Layout
    
    @return: None  
    ''' 
    def GetLayout(self):
        return self.FileChangedLayout

    '''
    Set Window Layout
    
    @return: None  
    ''' 
    def SetWindowLayout(self):
        self.FileChangedWin.setLayout(self.FileChangedLayout)

    '''
    Close Click
    
    @return: None  
    ''' 
    def CloseClick(self):
        self.parentWin.setWindowTitle("Fixity "+self.parentWin.versoin)
        self.changeThePathInformation = False
        self.FileChangedWin.close()
    
    '''
    Destroy window Information
    
    @return: None
    ''' 
    def DestroyEveryThing(self):
        self.destroyFileChanged()
        self.FileChangedWin.close()


    '''
    All design Management Done in Here
    
    @return: None
    ''' 
        
    def SetDesgin(self):

        self.GetLayout().addStrut(400)

        # Initializing view elements
        self.orignalPathLable = QLabel()
        self.changePathToLable = QLabel()
        self.setInformation = QPushButton("&Orignal Path Information")
        self.setInformation = QPushButton("&Change Path")
        self.cancel = QPushButton("Close")
        self.orignalPath = QTextEdit()
        self.changePathTo = QTextEdit()


        # Set view text
        self.orignalPath.setText(self.orignalPathText)
        self.changePathTo.setText(self.changePathText)
        self.orignalPathLable.setText('Change Path From')
        self.changePathToLable.setText('To')
        self.orignalPath.setDisabled(True)
        self.changePathTo.setDisabled(True)

        # Styling
        self.orignalPath.setMaximumSize(400, 100)
        self.changePathTo.setMaximumSize(400, 100)
        self.cancel.setMaximumSize(200, 100)
        self.setInformation.setMaximumSize(200, 100)

        # set Widget to layouts
        self.GetLayout().addWidget(self.orignalPathLable)
        self.GetLayout().addWidget(self.orignalPath)
        self.GetLayout().addWidget(self.changePathToLable)
        self.GetLayout().addWidget(self.changePathTo)
        self.GetLayout().addWidget(self.setInformation)
        self.GetLayout().addWidget(self.cancel)

        # set triggers
        self.setInformation.clicked.connect(self.changeRootDirInfo)
        self.cancel.clicked.connect(self.CloseClick)
        self.SetWindowLayout()
        

    '''
    Points out to change the Path of Manifest or not
    
    @return: None  
    ''' 
    def changeRootDirInfo(self):
        if not path.exists(self.changePathText):
            
            msgBox = QMessageBox()
            msgBox.setText(self.changePathText + ' does not exist.\nPlease provide a valid path and try again.')
            msgBox.exec_()
            
            self.changeThePathInformation = False
        else:
            if (self.orignalPathText is not None and self.changePathText is not None) and (self.orignalPathText != '' and self.changePathText != ''):
                self.changeThePathInformation = True
            else:
                self.changeThePathInformation = False
        self.FileChangedWin.close()