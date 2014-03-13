'''
Created on Feb 27, 2014

@author: Furqan
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
            print(moreInformation)
#             Debugging = Debuger.Debuger()
#             Debugging.tureDebugerOn()    
#             Debugging.logError('Error Reporting 615  - 621 File FixityCore While inserting information'+"\n", moreInformation)    
            
     

 
