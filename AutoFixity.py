# Fixity command line application
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
 
from AutoRuner import AutoRuner
import sys
from Threading import Threading
# project = sys.argv[1]
# IsemailSet = ''
# try:
#     if sys.argv[2]:
#         IsemailSet = sys.argv[2]
# except:
#     pass

Thread = Threading('New_Project','New_Project',1,'AutoFixity.exe','D:\python\Fixity Project\schedules\/','New_Project Run')
Thread.start()

AR = AutoRuner()

project = 'New_Project'
IsemailSet = 'Run'
AR.runAutoFix(project , IsemailSet)
