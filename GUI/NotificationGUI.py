# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014
 
@author: Furqan Wasi <furqan@avpreserve.com>
'''

from PySide.QtCore import *
from PySide.QtGui import *


'''
    Pop Up Messages,  handler
'''


class NotificationGUI(QMessageBox):
    

    '''
        Constructor
    '''
    def __init__(self):
        ''' QMessageBox  Constructor '''
        super(NotificationGUI,self).__init__()


    '''
    Show Error Message
     
    @param Object parent: Parent Or Called Instance
    @param String heading: heading of the Pop Up
    @param String message: Message of The Pop Up
    
    @return None
    
    '''    
    def showError(self,parent,heading,message):
        self.critical(parent, heading, message)
        return
        
        
    '''
    Show Error Message
     
    @param Object parent: Parent Or Called Instance
    @param String heading: heading of the Pop Up
    @param String message: Message of The Pop Up
    
    @return None
    
    '''    
    def showWarning(self,parent,heading,message):
        self.warning(parent, heading, message)
        return
    
    
    '''
    Show Question Message
     
    @param Object parent: Parent Or Called Instance
    @param String heading: heading of the Pop Up
    @param String message: Message of The Pop Up
    
    @return Boolean: response by User 
    
    ''' 
    def showQuestion(self,parent,heading,message):
        response = self.question(parent, heading, message, self.Yes | self.No)
        
        result = {
                  self.Yes: True,
                  self.No:False,
                  self.Cancel:False
                  }
        

        return result[response]
        
        
    '''
    Show Question Message
     
    @param Object parent: Parent Or Called Instance
    @param String heading: heading of the Pop Up
    @param String message: Message of The Pop Up
    
    @return None 
    
    ''' 
    def showInformation(self,parent,heading,message):
        self.information(parent, heading, message)
        return
    
# app = QApplication('asd')
# N = Notifications()
# N.showQuestion(N,'testing','asdas asdasasdasasdasasdasasdasasdasasdas')
# N.showWarning(N,'testing','asdas asdasasdasasdasasdasasdasasdasasdas')
# N.showError(N,'testing','asdas asdasasdasasdasasdasasdasasdasasdas')
# N.showInformation(N,'testing','asdas asdasasdasasdasasdasasdasasdasasdas')
# 
# exit(app.exec_())     