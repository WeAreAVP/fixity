# Fixity command line application
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from AutoRuner import AutoRuner
import sys

project = sys.argv[1]
IsemailSet = ''
try:
    if sys.argv[2]:
        IsemailSet = sys.argv[2]
except:
    pass
AR = AutoRuner()


IsemailSet = 'Run'
AR.runAutoFix(project , IsemailSet)
