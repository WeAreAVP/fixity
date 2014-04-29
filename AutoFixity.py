# -- coding: utf-8 --
# Fixity command line application
#  Version 0.4, Apr 1, 2014
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
'''
Created on Dec 5, 2013
@author: Furqan Wasi <furqan@avpreserve.com>
'''

'''
Run Scheduler of scanning directory on schedulers demand
''' 
from AutoRuner import AutoRuner
import sys

projectName = sys.argv[1]
isEmailSendingSet = ''
try:
    if sys.argv[2]:
        isEmailSendingSet = sys.argv[2]
except:
    pass
AR = AutoRuner()

isEmailSendingSet = 'Run'
AR.runAutoFix(projectName , isEmailSendingSet)
