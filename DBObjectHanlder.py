# -- coding: utf-8 --
# DB Objects Hanlder
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

'''
Created on Feb 27, 2014
@author: Furqan Wasi  <furqan@geekschicago.com>
'''
import sqlite3 as sql
from os import   getcwd



class DBObjectHanlder(object):

    def connect(self):
        try:
            self.con = sql.connect(getcwd()+'\\bin\\Fixity.db')
            self.cursor = self.con.cursor()
        except Exception as ex:
            moreInformation = {"moreInfo":'null'}
            try:
                if not ex[0] == None:
                    moreInformation['LogsMore'] =str(ex[0])
            except:
                pass
            try:
                if not ex[1] == None:
                    moreInformation['LogsMore1'] =str(ex[1])
            except:
                pass