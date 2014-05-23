#!/usr/bin/env python
from Core import SharedApp

class ProjectRepository(object):
    def __init__(self):
        self.Fixity = SharedApp.SharedApp.App

    def getAll(self):
        return self.Fixity.Database.getProjectInfo()

