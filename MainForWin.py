# Fixity GUI
# Version 0.4, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0


import os
OS_Info = ''
if os.name == 'posix':
    OS_Info = 'linux'
elif os.name == 'nt':
    OS_Info = 'Windows'
elif os.name == 'os2':
    OS_Info = 'check'
# import resource

#Bultin Libraries
from PySide.QtCore import *
from PySide.QtGui import *
if OS_Info == 'linux':
    from os import path, listdir, remove, walk , getcwd , spawnl , system
else:
    from os import path, listdir, remove, walk , getcwd , P_DETACH , spawnl , system

from collections import deque
from genericpath import exists
import re
import datetime
import shutil
import sys
import argparse
import platform
import os


#Custom Libraries
from EmailPref import EmailPref
from FilterFiles import FilterFiles


from ProjectWin import ProjectWin

if __name__ == '__main__':
        app = QApplication(sys.argv)
        w = ProjectWin(EmailPref , FilterFiles)
        w.show()
        sys.exit(app.exec_())

