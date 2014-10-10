# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''
from os import path
from Core import SharedApp
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
        project_core = self.Fixity.ProjectRepo.getSingleProject(project_name)
        print(project_name)
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


    def runAsAdmin(self, cmdLine=None, wait=True):

        if os.name != 'nt':
            raise RuntimeError, "This function is only implemented on Windows."

        import win32api, win32con, win32event, win32process
        from win32com.shell.shell import ShellExecuteEx
        from win32com.shell import shellcon

        python_exe = sys.executable

        if cmdLine is None:
            cmdLine = [python_exe] + sys.argv
        elif type(cmdLine) not in (types.TupleType,types.ListType):
            raise ValueError, "cmdLine is not a sequence."
        cmd = '"%s"' % (cmdLine[0],)
        # XXX TODO: isn't there a function or something we can call to massage command line params?
        params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
        cmdDir = ''
        showCmd = win32con.SW_SHOWNORMAL
        #showCmd = win32con.SW_HIDE
        lpVerb = 'runas'  # causes UAC elevation prompt.

        # print "Running", cmd, params

        # ShellExecute() doesn't seem to allow us to fetch the PID or handle
        # of the process, so we can't get anything useful from it. Therefore
        # the more complex ShellExecuteEx() must be used.

        #procHandle = win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)
        print(cmd)
        procInfo = ShellExecuteEx(nShow=showCmd,
                                  fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                                  lpVerb=lpVerb,
                                  lpFile=cmd,
                                  lpParameters=params)

        #if wait:
        #    procHandle = procInfo['hProcess']
        #    obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        #    rc = win32process.GetExitCodeProcess(procHandle)
        #    #print "Process handle %s returned code %s" % (procHandle, rc)
        #else:
        #    rc = None

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
        #if not Fixity.isUserAdmin():
        #     rc = Fixity.runAsAdmin()
        Fixity.LaunchGUI(sys.argv)
    else:
        try:
            Fixity.LaunchCLI(args.autorun)
        except:
           exc_type, exc_obj, exc_tb = sys.exc_info()
           file_name = path.split(exc_tb.tb_frame.f_code.co_filename)[1]

           print("Could not run this Project "+str(Exception.message))


