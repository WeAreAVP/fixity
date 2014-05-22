'''
Created on May 14, 2014

@author: Furqan
'''
import sys
from Core import SharedApp
from GUI import GUILibraries
import App

class Main (object):
    def __init__(self):
        SharedApp.SharedApp.App = App.App.getInstance()

    def LaunchGUI(self,arg):
        app = GUILibraries.QApplication(arg)
        app.MainFixityWindow = App.ProjectGUI.ProjectGUI()
        app.MainFixityWindow.show()
        app.exec_()

if __name__ == '__main__':
    Fixity = Main()
    Fixity.LaunchGUI(sys.argv)
