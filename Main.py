'''
Created on May 14, 2014

@author: Furqan
'''
import sys, os
from Core import SharedApp
from GUI import GUILibraries
import App
import argparse

class Main (object):

    ''' classdocs '''
    def __init__(self):
        SharedApp.SharedApp.App = App.App.getInstance()
        self.Fixity = SharedApp.SharedApp.App

    def LaunchGUI(self,arg):
        app = GUILibraries.QApplication(arg)
        app.MainFixityWindow = App.ProjectGUI.ProjectGUI()
        app.MainFixityWindow.show()
        app.exec_()

    def LaunchScheduler(self, project_name):
        project_core = self.Fixity.getSingleProject(project_name)
        project_core.Run()




if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-a', '--autorun')
        args = parser.parse_args()
    except Exception:
        print("Could not run this Project "+str(Exception.message))
        pass

    # If Received argument (project name and run command), it with run the
    # scheduler other wise it will open Fixity Front end View)

    if args.autorun is None or args.autorun == '':
        Fixity = Main()
        Fixity.LaunchGUI(sys.argv)

    else:
        try:
            print('Scanning is in progress!........')
            Fixity = Main()
            Fixity.LaunchScheduler(args.autorun)
            sys.exit()
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
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
            print(error_information)

            print("Could not run this Project "+str(Exception.message))


