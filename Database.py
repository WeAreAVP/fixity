# -*- coding: UTF-8 -*-

# Fixity command line application
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0
'''
Created on Feb 27, 2014
@author: Furqan Wasi
'''
from PySide.QtCore import *
from PySide.QtGui import *
import sqlite3
from os import  getcwd
import re
from Debuger import Debuger
import os
import time
#Getting OS Info
OS_Info = ''
if os.name == 'posix':
    OS_Info = 'linux'
elif os.name == 'nt':
    OS_Info = 'Windows'
elif os.name == 'os2':
    OS_Info = 'check'


class Database(object):
    #Constructor
    def __init__(self):

        self._tableConfiguration = 'configuration'
        self._tableProject = 'project'
        self._tableProjectPath = 'projectPath'
        self._tableVersionDetail = 'versionDetail'
        self._tableVersions ='versions'
        self.con = None
        self.cursor = None
        self.timeSpan = 1
    #Connect to Database
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

    #SQL Query Runner
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
    #SQL Select Query
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
    #Query Result to list converter
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
    #SQL Insert Query
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
    #SQL Delete Query
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
    #SQL Update Query
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
    #Columns and records Implode for query
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
    #Commit Query
    def commit(self):
        if(self.con and self.con != None):
            self.con.commit()
    #Close connection safely
    def closeConnection(self):
        if(self.con and self.con != None):
            self.con.close()
            self.con = None
            self = None
    #Get Project Information
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

    #Get Projects paths Information
    def getProjectPathInfo(self,projectID,versionID):
        self.connect()
        information = {}
        information['id'] = None
        response = self.select(self._tableProjectPath, '*', "projectID='"+str(projectID)+"' and versionID = '"+ str(versionID) + "'")
        self.closeConnection()
        return response
    #Get Configuration
    def getConfiguration(self):
        response = self.select(self._tableConfiguration, '*')
        self.closeConnection()
        return response
    #Get Given Version Details
    def getVersionDetails(self,projectID,versionID,OrderBy=None):
        response = self.select(self._tableVersionDetail, '*'," projectID='"+str(projectID)+"' and versionID='"+str(versionID)+"'" , OrderBy)
        self.closeConnection()
        return response
    #Get Last Inserted Version of given project
    def getVersionDetailsLast(self,projectID):
        response = {}
        resultOfLastVersion = self.select(self._tableVersionDetail, '*'," projectID='"+str(projectID)+"'", ' versionID DESC LIMIT 1')
        self.closeConnection()
        if(len(resultOfLastVersion) > 0):
            response = self.getVersionDetails(projectID,resultOfLastVersion[0]['versionID'],' id DESC')
        return response
    #Convert List to Tuple Data type
    def listToTuple(self,provededList):

        NewList = []
        for singleOfprovededList in  provededList:
            NewList.append(provededList[singleOfprovededList])
        return tuple(NewList)





