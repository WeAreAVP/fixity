# -*- coding: UTF-8 -*-
# Fixity SQLITE Database Handler
# Version 0.3, Dec 1, 2013
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

'''
Created on Feb 27, 2014
@author: Furqan Wasi <furqan@geekschicago.com>
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

debuger = Debuger()

class MsgBox(QDialog):
    def __init__(self):
        QDialog.__init__(self)


class Database(object):
    '''Constructor'''
    def __init__(self):

        self._tableConfiguration = 'configuration'
        self._tableProject = 'project'
        self._tableProjectPath = 'projectPath'
        self._tableVersionDetail = 'versionDetail'
        self._tableVersions ='versions'
        self.con = None
        self.cursor = None
        self.timeSpan = 1

    '''Connect to Database'''
    def connect(self):

        pathInfo = str(getcwd()).replace('\\schedules','')
        pathInfo = pathInfo.replace('schedules','')
        gab = 10
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

            debuger.tureDebugerOn()
            debuger.logError('Error Reporting 36 - 42 File Database While Connecting for database information'+"\n", moreInformation)
            if not self.timeSpan:
                self.timeSpan = 1

            if self.timeSpan <= 60:
                self.timeSpan = self.timeSpan + gab

                try:
                    self.QMChecking.close()
                except Exception as ex:
                    pass

                try:
                    self.QMWait = QMessageBox()
                    self.QMWait.information(MsgBox(), "Information", "Please wait, Some the Database recourses are in use, Fixity will continue this process as soon as Database is released ,this may take several ")
                except Exception as ex:

                    pass

                time.sleep(gab)
                try:
                    self.QMWait.close()
                    QCoreApplication.processEvents()
                except Exception as ex:

                    pass

                try:
                    self.QMChecking = QMessageBox()
                    self.QMChecking.information(MsgBox(), "Information", "Checking for Recourses")
                except Exception as ex:

                    pass

                self.connect()

            else:
                print('Exiting process')
                self.closeConnection()
                self = None
                exit()
                
    ''' 
    Get one record using given sql query
    @param query: SQL Raw Query
    
    @return: One sQuery Result 
    '''             
    def getOne(self,query):
        
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
            Row= self.cursor.fetchone()
            try:
                self.closeConnection()
            except:
                pass

            self.closeConnection()
            return Row

        except Exception as e:
            try:
                self.closeConnection()
                self.connect()
                response = self.cursor.execute(query)
                try:
                    self.closeConnection()
                except:
                    pass
                return response
            except:
                pass
    '''SQL Query Runner
    @param query: SQL Raw Query
    
    @return: Query Result 
    '''  
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
                try:
                    self.closeConnection()
                except:
                    pass
                return response
            except:
                pass

    '''
    SQL Select Query
    @param tableName: Table Name
    @param select: Column To Select
    @param condition: Conditions as String
    @param orderBy: order By Columns
    
    @return: Query Result
    '''
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

                debuger.tureDebugerOn()
                debuger.logError('Error Reporting 140- 155 File Database While Querying database information'+"\n", moreInformation)
                print(moreInformation)
                print('Error Reporting 140- 155 File Database While Querying database information')
                try:
                    self.closeConnection()
                except:
                    pass

            try:
                self.commit()
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

                debuger.tureDebugerOn()
                debuger.logError('Error Reporting 160- 170 File Database While Commiting database information'+"\n", moreInformation)
                print(moreInformation)
                print('Error Reporting 160- 170 File Database While Commiting database information')
                try:
                    self.closeConnection()
                except:
                    pass

            try:
                self.closeConnection()
            except:
                pass
            return response


        except Exception as e:

            self.closeConnection()
            pass

    '''
    Query Result to list converter
    '''
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

    '''
    SQL Insert Query
    @param tableName: Table Name
    @param information: List of columns with Values (index as Column and Value as Column Value)
    
    @return: Insert Id of this record
    '''
    
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

                debuger.tureDebugerOn()
                debuger.logError('Error Reporting 320- 336 File Database While Commiting database information'+"\n", moreInformation)
                print(moreInformation)
                print('Error Reporting 320- 336 File Database While Commiting database information')
                try:
                    self.closeConnection()
                except:
                    pass

            try:
                self.cursor.execute(query)
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

                debuger.tureDebugerOn()
                debuger.logError('Error Reporting 250- 255 File Database While executing Query information'+"\n", moreInformation)
                print(moreInformation)
                print('Error Reporting 250- 255 File Database While executing Query information')
                try:
                    self.closeConnection()
                except:
                    pass

            try:
                self.commit()
                self.closeConnection()
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

                debuger.tureDebugerOn()
                debuger.logError('Error Reporting 160- 170 File Database While Commiting database information'+"\n", moreInformation)
                print(moreInformation)
                try:
                    self.closeConnection()
                except:
                    pass


            try:
                self.closeConnection()
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

                debuger.tureDebugerOn()
                debuger.logError('Error Reporting 295- 296 File Database While closing Database information'+"\n", moreInformation)
                print(moreInformation)
                print('Error Reporting 295- 296 File Database While closing Database information')
                try:
                    self.closeConnection()
                except:
                    pass
            return {'id':self.cursor.lastrowid}

    '''
    SQL Delete Query
    @param tableName: Table Name
    @param condition: Condition of which row will deleted
    
    @return: Response of Query Result
    '''
    
    def delete(self,tableName , condition):
        try:
            query = 'DELETE FROM '+str(tableName) + ' WHERE '+ condition
            response = self.sqlQuery(query)
            self.closeConnection()
            return response
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

                debuger.tureDebugerOn()
                debuger.logError('Error Reporting 324- 330 File Database While executing Query information'+"\n", moreInformation)
                
                try:
                    self.closeConnection()
                except:
                    pass
                return None

    '''SQL Update Query
      @param tableName: Table Name
      @param information: List of columns with Values (index as Column and Value as Column Value)
      @param condition: Condition of which row will deleted
    
      @return: Response of Query Result
    '''
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

                debuger.tureDebugerOn()
                debuger.logError('Error Reporting 367- 370 File Database While executing Query information'+"\n", moreInformation)
                print(moreInformation)
                print('Error Reporting 367- 370 File Database While executing Query information')
                try:
                    self.closeConnection()
                except:
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

                debuger.tureDebugerOn()
                debuger.logError('Error Reporting 250- 255 File Database While executing Query information'+"\n", moreInformation)
               
                try:
                    self.closeConnection()
                except:
                    pass
                return None

    '''Columns and records Implode for query
      @param information: Array of Value to be imploded
      @param glue: glue with values will be glued
      @param isColumn: Given Information is of tables columns or Row
       
      @return: Response of Query Result
    '''
        
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
                            stringGlued = stringGlued + ' "'+ str(information[info])+ '" '
                        else:
                            stringGlued =  stringGlued +' , "'    + information[info]+ '" '
                    counter = counter + 1
                except Exception as e:
                    self.closeConnection()
                    pass

            return stringGlued

    '''Commit Query'''
    def commit(self):
        if(self.con and self.con != None):
            self.con.commit()

    '''Close connection safely
    '''
    def closeConnection(self):
        if(self.con and self.con != None):
            self.con.close()
            self.con = None
            self = None

    '''
    Get Project Information
    @param projectName: Project Name to be searched in database
    @param limit: If Ture 1 limit with be applied
    
    @return project information 
    '''
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

    '''
    Get Projects paths Information
    @param projectID: Project ID
    @param versionID: ID of Version of Project to be fetched
    
    @return project information 
    '''
    def getProjectPathInfo(self,projectID,versionID):
        self.connect()
        information = {}
        information['id'] = None
        response = self.select(self._tableProjectPath, '*', "projectID='"+str(projectID)+"' and versionID = '"+ str(versionID) + "'")
        self.closeConnection()
        return response

    '''
    Get SMTP and User Email Configuration
   
    @return Configuration 
    
    '''
    def getConfiguration(self):
        response = self.select(self._tableConfiguration, '*')
        self.closeConnection()
        return response

    '''
    Get Given Version Details
    @param projectID: Project ID
    @param versionID: ID of Version of Project who's detail to be fetched
    @param OrderBy: Order By
    
    @return project information 
    '''
    def getVersionDetails(self,projectID,versionID,OrderBy=None):
        response = self.select(self._tableVersionDetail, '*'," projectID='"+str(projectID)+"' and versionID='"+str(versionID)+"'" , OrderBy)
        self.closeConnection()
        return response
    
    ''' Fetch information related to email configuration'''
    def getConfigInfo(self, project=None):
        

        queryResult = self.select(self._tableConfiguration)

        try:
            if len(queryResult)>0 :
                information = {}
                for  result in queryResult:
                    information['id'] = queryResult[result]['id']
                    information['smtp'] = self.DecodeInfo(queryResult[result]['smtp'])
                    information['email'] = self.DecodeInfo(queryResult[result]['email'])
                    information['pass'] = self.DecodeInfo(queryResult[result]['pass'])
                    information['port'] = queryResult[result]['port']
                    information['protocol'] = queryResult[result]['protocol']
                    information['debugger'] = queryResult[result]['debugger']
                    break;
                return information
        except:
            pass
        return {}
    
    '''Get Last Inserted Version of given project'''
    def getVersionDetailsLast(self,projectID):
        response = {}
        resultOfLastVersion = self.select(self._tableVersionDetail, '*'," projectID='"+str(projectID)+"'", ' versionID DESC LIMIT 1')
        self.closeConnection()
        if(len(resultOfLastVersion) > 0):
            response = self.getVersionDetails(projectID,resultOfLastVersion[0]['versionID'],' id DESC')
        return response

    '''Convert List to Tuple Data type'''
    def listToTuple(self,provededList):

        NewList = []
        for singleOfprovededList in  provededList:
            NewList.append(provededList[singleOfprovededList])
        return tuple(NewList)

