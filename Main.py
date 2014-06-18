# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''
import sys
import os
from os import path
from Core import SharedApp
from GUI import GUILibraries
import App
from argparse import ArgumentParser


class Main (object):

    def __init__(self):
        SharedApp.SharedApp.App = App.App.getInstance()
        self.Fixity = SharedApp.SharedApp.App

    def LaunchGUI(self,arg):
        app = GUILibraries.QApplication(arg)
        app.MainFixityWindow = App.ProjectGUI.ProjectGUI()
        app.MainFixityWindow.show()
        print(os.getpid())
        app.exec_()

    def LaunchCLI(self, project_name):
        project_core = self.Fixity.ProjectRepo.getSingleProject(project_name)
        project_core.Save(False)
        project_core.Run()

if __name__ == '__main__':
    try:
        parser = ArgumentParser()
        parser.add_argument('-a', '--autorun')
        args = parser.parse_args()
    except:
        pass

    # If Received argument (project name and run command), it with run the
    # scheduler other wise it will open Fixity Front end View)

    Fixity = Main()
    if args.autorun is None or args.autorun == '':
        Fixity.LaunchGUI(sys.argv)
    else:
        try:
            Fixity.LaunchCLI(args.autorun)
        except:
           exc_type, exc_obj, exc_tb = sys.exc_info()
           file_name = path.split(exc_tb.tb_frame.f_code.co_filename)[1]
           error_information = {}
           try:
              error_information['file_name'] = file_name
           except:
              pass

           try:
              error_information['error_type'] = exc_type
           except:
              pass

           try:
              error_information['line_no'] = exc_tb.tb_lineno
           except:
              pass
           print("Could not run this Project "+str(Exception.message))


