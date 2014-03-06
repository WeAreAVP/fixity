'''
Created on Feb 27, 2014

@author: Furqan
'''
import sqlite3 as sql
from os import   getcwd



class DBObjectHanlder(object):
    
        
    def connect(self):

        self.con = None
        self.con = sql.connect(getcwd()+'\\Fixity.db')
        self.cursor = self.con.cursor()
     
    def printing(self):
        print(';asdas')
 
        