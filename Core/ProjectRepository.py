#!/usr/bin/env python
from Core import SharedApp
from Core import Database
class ProjectRepository(object):
    def __init__(self):
        self.Database = Database.Database()
        self.Fixity = SharedApp.SharedApp.App
        self.Database = Database.Database()

    def getAll(self):
        return self.Database.getProjectInfo()

