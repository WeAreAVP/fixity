# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''
from os import path
from Core import SharedApp, DatabaseLockHandler
from GUI import GUILibraries
import App
from argparse import ArgumentParser
import sys, os, traceback, types

class Main (object):

    def __init__(self, is_unit_test = False):
        SharedApp.SharedApp.App = App.App.getInstance(is_unit_test)
        self.Fixity = SharedApp.SharedApp.App
        self.Fixity.is_unit_test = is_unit_test


    def LaunchGUI(self, arg):
        app = GUILibraries.QApplication(arg)
        app.MainFixityWindow = App.ProjectGUI.ProjectGUI()
        app.MainFixityWindow.show()

        app.exec_()

    def LaunchCLI(self, project_name, called_from = 'CLI', new_path = None):
        print('started')
        is_lock_exists = False
        is_dead_lock = False

        try:
            process_id = os.getpid()
        except:
            process_id = None
            pass

        print('Get File Locker and check for dead lock')
        # Get File Locker and check for dead lock
        try:
            lock = DatabaseLockHandler.DatabaseLockHandler(self.Fixity.Configuration.getLockFilePath(),process_id, timeout=20)

            is_dead_lock = lock.isProcessLockFileIsDead()
        except:
            self.Fixity.logger.LogException(Exception.message)
            print(Exception.message)
            pass


        print('is_dead_lock')
        try:
            if is_dead_lock:
                lock.is_locked = True
                lock.release()
        except:
            self.Fixity.logger.LogException(Exception.message)
            pass

        print('isLockFileExists')
        try:
            is_lock_exists = lock.isLockFileExists()
        except:
            pass

        print('getSingleProject')
        project_core = self.Fixity.ProjectRepo.getSingleProject(project_name)
        if is_lock_exists is False:
            if new_path is not None:
                dir_information = {}
                dir_information['path'] = new_path


                self.Fixity.Database.update(self.Fixity.Database._tableProjectPath, dir_information, '1 = 1')

                for dirs_objects in project_core.directories:
                    project_core.directories[dirs_objects].setPath(new_path)
                    break

            project_core.Save(False)
            if called_from == 'test':
                return project_core.Run(False, False, False, 'test')
            else:
                project_core.Run()
        else:
            print('Fixity is already scanning a project.\nPlease wait until the current scan completes before starting a new one.')
        return ''
if __name__ == '__main__':
    try:
        parser = ArgumentParser()
        parser.add_argument('-a', '--autorun')
        args = parser.parse_args()
    except:
        pass

    # If Received argument (project name and run command), it with run the
    # scheduler other wise it will open Fixity Front end View)
    Fixity = Main(False)
    if args.autorun is None or args.autorun == '':
        Fixity.LaunchGUI(sys.argv)
    else:
        try:
            Fixity.LaunchCLI(args.autorun)
        except:
           exc_type, exc_obj, exc_tb = sys.exc_info()
           file_name = path.split(exc_tb.tb_frame.f_code.co_filename)[1]

           print("Could not run this Project "+str(Exception.message))


