
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