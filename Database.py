# -*- coding: UTF-8 -*-
'''
Created on Feb 27, 2014

@author: Furqan
'''
from PySide.QtCore import *
from PySide.QtGui import *
import sqlite3
from os import  getcwd
import re
from Debuger import Debuger
import os
import time
OS_Info = ''
if os.name == 'posix':
    OS_Info = 'linux'
elif os.name == 'nt':
    OS_Info = 'Windows'
elif os.name == 'os2':
    OS_Info = 'check'

# from avp import DBHanlder
# from DBObjectHanlder import DBObjectHanlder  as hanlder
class Database(object):

    def __init__(self):

        self._tableConfiguration = 'configuration'
        self._tableProject = 'project'
        self._tableProjectPath = 'projectPath'
        self._tableVersionDetail = 'versionDetail'
        self._tableVersions ='versions'
        self.con = None
        self.cursor = None
        self.timeSpan = 1

    def connect(self):

        pathInfo = str(getcwd()).replace('\\schedules','')
        pathInfo = pathInfo.replace('schedules','')
        gab = 30
        try:
            if(OS_Info == 'Windows'):
                self.con = sqlite3.connect(pathInfo+"\\bin\\Fixity.db")
            else:
                self.con = sqlite3.connect(pathInfo+"/bin/Fixity.db")

            self.cursor = self.con.cursor()

        except (sqlite3.OperationalError,Exception) as ex:
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
            debuger = Debuger()
            debuger.tureDebugerOn()
            debuger.logError('Error Reporting 36 - 42 File Database While Connecting for database information'+"\n", moreInformation)

            if not self.timeSpan:
                self.timeSpan = 1

            if self.timeSpan <= 600:
                self.timeSpan = self.timeSpan + gab
                time.sleep(gab)
                self.connect()

            else:

                print('Exiting process')
                self.closeConnection()
                self = None
                exit()


    def sqlQuery(self, query):

        try:
            try:
                self.connect()
            except:
                pass

            response = self.cursor.execute(query)
            try:
                self.commit()
            except:
                pass

            try:
                self.closeConnection()
            except:
                pass
            self.closeConnection()
            return response

        except Exception as e:
            try:
                self.closeConnection()
                self.connect()
                response = self.cursor.execute(query)
                return response
            except:
                pass

    def select(self,tableName , select  = '*' ,condition=None,orderBy = None):
        try:
            query= ''
            query = 'SELECT '+ str(select) +' FROM '+str(tableName)
            if(condition != None):
                query += ' WHERE ' + condition
            if(orderBy != None):
                query += ' ORDER BY '+ orderBy

            response = {}
            responseCounter = 0

            try:
                self.connect()
            except:
                pass

            try:
                for r in self.dict_gen(self.cursor.execute(query)):
                    response[responseCounter] = r
                    responseCounter =responseCounter + 1
            except Exception as e:
                print(e[0])
                pass

            try:
                self.commit()
            except:
                pass

            try:
                self.closeConnection()
            except:
                pass
            return response


        except Exception as e:
            print(e[0])
            self.closeConnection()
            pass

    def dict_gen(self,curs):
        ''' From Python Essential Reference by David Beazley
        '''
        import itertools
        field_names = [d[0] for d in curs.description]
        while True:
            rows = curs.fetchmany()
            if not rows: return
            for row in rows:
                yield dict(itertools.izip(field_names, row))

    def insert(self, tableName, information):

            query = 'INSERT INTO '+str(tableName)
            values = {}
            columnName = {}
            counter = 0
            for index in information:
                try:
                    columnName[str(counter)] = index
                    values[str(counter)]  = str(information[index])
                    counter = counter + 1
                except:
                    pass

            query = query + ' ( '+self.implode ( columnName , ' , ' ) + ' ) VALUES ( ' + self.implode ( values , ' , ' , False ) + ' ) '

            try:
                self.connect()
            except:
                print('er1')
                pass

            try:
                self.cursor.execute(query)
            except Exception as e:
                print(e[0])
                print('er1')
                pass

            try:
                self.commit()
            except Exception as e:
                print(e[0])
                print('er2')
                pass
            self.closeConnection()
            try:
                self.closeConnection()
            except:
                print(e[0])
                print('er3')
                pass
            return {'id':self.cursor.lastrowid}

    def delete(self,tableName , condition):
        try:
            query = 'DELETE FROM '+str(tableName) + ' WHERE '+ condition
            print('Deleting  info from ' + tableName)
            response = self.sqlQuery(query)

            self.closeConnection()
            return response
        except Exception as e:
            print(e[0])
            self.closeConnection()
            return None

    def update(self,tableName , information,condition):
        try:
            query = 'UPDATE '+str(tableName) +' SET '
            counter = 0
            for singleInfo in information:

                    if(counter == 0):
                        query += str(singleInfo) + "='" + str(information[singleInfo]) +"'"
                    else:
                        query += ' , '+ str(singleInfo) + "='" + str(information[singleInfo]) +"'"
                    counter=counter+1
            query += ' WHERE '+condition

            try:
                self.connect()
            except:
                pass

            try:

                response = self.cursor.execute(query)
            except:
                print('er1')
                pass

            try:
                self.commit()
            except:
                pass

            try:
                self.closeConnection()
            except:
                pass

            return response

        except Exception as e:
            print(e[0])
            self.closeConnection()
            return None

    def implode(self,information , glue , isColumn = True):

            counter = 0
            stringGlued = ''
            for info in information:
                try:
                    if isColumn:
                        if(counter == 0):
                            stringGlued = stringGlued + information[info]
                        else:
                            stringGlued =  stringGlued +' , ' + information[info]

                    else:
                        if(counter == 0):
                            stringGlued = stringGlued + ' "'+ str(information[info]).encode('utf-8') + '" '
                        else:
                            stringGlued =  stringGlued +' , "'    + information[info].encode('utf-8') + '" '
                    counter = counter + 1
                except Exception as e:
                    self.closeConnection()
                    pass

            return stringGlued

    def commit(self):
        if(self.con and self.con != None):
            self.con.commit()

    def closeConnection(self):
        if(self.con and self.con != None):
            self.con.close()
            self.con = None
            self = None

    def getProjectInfo(self,projectName = None ,limit = True):
        response = {}
        try:

            information = {}
            information['id'] = None
            limit = ' '
            condition = None
            if limit:
                limit  = " LIMIT 1"

            if projectName:
                condition ="title like '"+projectName+"' " + limit

            response = self.select(self._tableProject, '*', condition)

            self.closeConnection()
        except:
            pass

        self.closeConnection()
        return response


    def getProjectPathInfo(self,projectID,versionID):
        self.connect()
        information = {}
        information['id'] = None
        response = self.select(self._tableProjectPath, '*', "projectID='"+str(projectID)+"' and versionID = '"+ str(versionID) + "'")
        self.closeConnection()
        return response

    def getConfiguration(self):
        response = self.select(self._tableConfiguration, '*')
        self.closeConnection()
        return response

    def getVersionDetails(self,projectID,versionID,OrderBy=None):
        response = self.select(self._tableVersionDetail, '*'," projectID='"+str(projectID)+"' and versionID='"+str(versionID)+"'" , OrderBy)
        self.closeConnection()
        return response

    def getVersionDetailsLast(self,projectID):
        response = {}
        resultOfLastVersion = self.select(self._tableVersionDetail, '*'," projectID='"+str(projectID)+"'", ' versionID DESC LIMIT 1')
        self.closeConnection()
        if(len(resultOfLastVersion) > 0):
            response = self.getVersionDetails(projectID,resultOfLastVersion[0]['versionID'],' id DESC')
        return response
    def listToTuple(self,provededList):

        NewList = []
        for singleOfprovededList in  provededList:
            NewList.append(provededList[singleOfprovededList])
        return tuple(NewList)

# try:
#     var1 = {'runWhenOnBattery': 1, 'durationType': 2, 'extraConf': '', 'title': u'New_Project', 'runDayOrMonth': '1', 'lastRan': None, 'selectedAlgo': 'sha256', 'filters': '', 'ifMissedRunUponRestart': 1, 'runTime': u'00:00:00', 'emailOnlyUponWarning': 1}
#db = Database()
#db.connect()

#db.select(db._tableVersionDetail, '*')
#db.closeConnection()
#
# except Exception as e :
# db = Database()
# versionDetailOptions ={}
# versionDetailOptions['md5_hash'] = 'sadasdsadas'
# versionDetailOptions['ssh256_hash'] = 'sadasdsadas'
# versionDetailOptions['path'] = 'Fixity-1||\Bright Morningstar   DJ Ti√´sto   Elements of Life www.dilandau.eu.mp3'
# versionDetailOptions['inode'] = '112312312'
# versionDetailOptions['versionID'] = '1'
# versionDetailOptions['projectID'] = '1'
# versionDetailOptions['projectPathID'] = '1'
# print(versionDetailOptions)
# db.insert(db._tableVersionDetail, versionDetailOptions)
#
# db.connect()
# resposne = db.select(db._tableVersionDetail, '*')
# db.closeConnection()
# print(resposne[0]['path'])
# print(resposne)
#







