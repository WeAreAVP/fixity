# -*- coding: UTF-8 -*-
#!/usr/bin/env python
#
#@author: Furqan Wasi <furqan@avpreserve.com>
from Core import SharedApp

class ProjectRepository(object):

    def __init__(self):
        self.Fixity = SharedApp.SharedApp.App

    def getAll(self):
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        return self.Fixity.Database.getProjectInfo()

    def getSingleProject(self, project_name):
        try:self.Fixity = SharedApp.SharedApp.App
        except:pass

        try:
            selected_project_object = self.Fixity.ProjectsList[project_name]
            return selected_project_object
        except:
            return False
