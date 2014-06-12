# -*- coding: UTF-8 -*-
#Created on May 14, 2014
#
#@author: Furqan Wasi <furqan@avpreserve.com>
import re
__author__ = 'Furqan'
'''
    Validate given email address
    @param Email: Email Address

    @return: String Message of failure
'''
def ValidateProjectName(projectName):
    if not re.match(r"^[a-zA-Z0-9-_]+$", projectName):
        return False
    return True

''' Validate given email address
    @param Email: Email Address
    @return: String Message of failure

'''
def ValidateEmail(Email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
        return False
    return True