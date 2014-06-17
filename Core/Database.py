# -*- coding: UTF-8 -*-
#Created on May 14, 2014
#
#@author: Furqan Wasi <furqan@avpreserve.com>


from Core import SharedApp
import sqlite3
counter_recursion = 0
class Database(object):
    _instance = None
    def __init__(self):

        self.Fixity = SharedApp.SharedApp.App
        self._tableConfiguration = 'configuration'
        self._tableProject = 'project'
        self._tableProjectPath = 'projectPath'
        self._tableVersionDetail = 'versionDetail'
        self._tableVersions = 'versions'

        self.con = None
        self.cursor = None
        self.timeSpan = 1
        self.connect()

    @staticmethod
    def getInstance():
        if not isinstance(Database._instance, Database):
            Database._instance = object.__new__(Database)
            Database._instance.Fixity = SharedApp.SharedApp.App
            Database._instance._tableConfiguration = 'configuration'
            Database._instance._tableProject = 'project'
            Database._instance._tableProjectPath = 'projectPath'
            Database._instance._tableVersionDetail = 'versionDetail'
            Database._instance._tableVersions ='versions'
            Database._instance.con = None
            Database._instance.cursor = None
            Database._instance.timeSpan = 1
            Database._instance.connect()

        return Database._instance

    def selfDestruct(self):
        del self

    def connect(self):
        global counter_recursion
        try:

            self.con = sqlite3.connect(self.Fixity.Configuration.getDatabaseFilePath())
            self.cursor = self.con.cursor()
            counter_recursion = 0
        except:

            SharedApp.SharedApp.App.Database = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                return self.connect()


            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            pass

    #Get one record using given sql query
    #@param query: SQL Raw Query
    #
    #@return: One sQuery Result

    def getOne(self, query):
        global counter_recursion
        try:

            self.cursor.execute(query)
            self.con.commit()
            Row = self.cursor.fetchone()
            counter_recursion = 0
            return Row
        except (sqlite3.OperationalError):

            SharedApp.SharedApp.App.Database = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                return self.getOne(query)


            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            pass

    #SQL Query Runner
    #@param query: SQL Raw Query
    #
    #@return: Query Result

    def sqlQuery(self, query):
        global counter_recursion
        try:

            response = self.cursor.execute(query)
            self.con.commit()
            counter_recursion = 0
            return response
        except (sqlite3.OperationalError,Exception):

            SharedApp.SharedApp.App.Database = Database()
            self = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                return self.sqlQuery(query)

            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False

    #Get Project Information
    #@param project_name: Project Name to be searched in database
    #@param limit: If Ture 1 limit with be applied
    #
    #@return project information

    def getProjectInfo(self,project_name = None, limit = True):
        global counter_recursion
        try:
            information = {}
            information['id'] = None
            limit = ' '
            condition = None
            if limit:
                limit  = " LIMIT 1"

            if project_name:
                condition ="title like '"+project_name+"' " + limit

            return self.select(self._tableProject, '*', condition)

        except (sqlite3.OperationalError,Exception):

            SharedApp.SharedApp.App.Database = Database()
            self = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                return self.getProjectInfo(project_name, limit)


            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False

    #Get Projects paths Information
    #@param project_id: Project ID
    #@param version_id: ID of Version of Project to be fetched
    #
    #@return project information

    def getProjectPathInfo(self ,project_id ,version_id):
        global counter_recursion
        try:

            self.connect()
            information = {}
            information['id'] = None
            response = self.select(self._tableProjectPath, '*', "projectID='"+str(project_id)+"' and versionID = '"+ str(version_id) + "'")
            counter_recursion = 0
            return response
        except (sqlite3.OperationalError,Exception):

            SharedApp.SharedApp.App.Database = Database()
            self = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                return self.getProjectPathInfo(project_id ,version_id)


            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False

    #Get SMTP and User Email Configuration
    #@return Configuration

    def getConfiguration(self):
        global counter_recursion
        try:

            response = self.select(self._tableConfiguration, '*')
            counter_recursion = 0
            return response
        except (sqlite3.OperationalError,Exception):

            SharedApp.SharedApp.App.Database = Database()
            self = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                return self.getConfiguration()


            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False

    def getVersionDetails(self, project_id, version_id, OrderBy = None):
        global counter_recursion
        try:

            response = self.select(self._tableVersionDetail, '*'," projectID='"+str(project_id)+"' and versionID='"+str(version_id)+"'" , OrderBy)
            if len(response) <=0 or response is False:
                counter_recursion = 0
                return {}
            else:
                counter_recursion = 0
                return  {'version_id':version_id, 'response':response}

        except (sqlite3.OperationalError,Exception):

            SharedApp.SharedApp.App.Database = Database()
            self = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                return self.getVersionDetails(project_id, version_id, OrderBy)


            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False

    ''' Fetch information related to email configuration'''
    def getConfigInfo(self, project=None):
        global counter_recursion
        queryResult = self.select(self._tableConfiguration)
        try:
            global counter_recursion
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
                    break
                counter_recursion = 0
                return information
        except (sqlite3.OperationalError,Exception):

            SharedApp.SharedApp.App.Database = Database()
            self = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                return self.getConfigInfo(project)


            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False
        return {}

    #Get Last Inserted Version of given project
    def getVersionDetailsLast(self, project_id):
        global counter_recursion
        try:

            response = {}
            result_of_last_version = self.select(self._tableVersionDetail, '*'," projectID='"+str(project_id)+"'", ' versionID DESC LIMIT 1')
            if len(result_of_last_version) > 0:

                response = self.getVersionDetails(project_id,result_of_last_version[0]['versionID'],' id DESC')
            counter_recursion = 0
            return response
        except (sqlite3.OperationalError,Exception):

            SharedApp.SharedApp.App.Database = Database()
            self = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                return self.getVersionDetailsLast(project_id)


            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False

    #Convert List to Tuple Data type
    def listToTuple(self, proveded_list):
        global counter_recursion
        try:
            new_list = []
            for single_of_proveded_list in  proveded_list:
                new_list.append(proveded_list[single_of_proveded_list])
            return tuple(new_list)

        except (sqlite3.OperationalError,Exception):

            SharedApp.SharedApp.App.Database = Database()
            self = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                return self.listToTuple(proveded_list)


            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False

    def commit(self):
        self.con.commit()

    #SQL Select Query
    #@param table_name: Table Name
    #@param select: Column To Select
    #@param condition: Conditions as String
    #@param order_by: order By Columns
    #
    #@return: Query Result

    def select(self,table_name ,select = '*', condition=None, order_by = None):
        global counter_recursion
        try:
            query = 'SELECT '+ str(select) +' FROM '+str(table_name)
            if condition is not None:
                query += ' WHERE ' + condition
            if order_by is not None:
                query += ' ORDER BY '+ order_by

            response = {}
            response_counter = 0
            for r in self.dict_gen(self.cursor.execute(query)):
                response[response_counter] = r
                response_counter += 1

            self.commit()
            counter_recursion = 0
            return response
        except (sqlite3.OperationalError,Exception):

            SharedApp.SharedApp.App.Database = Database()
            self = Database()
            if counter_recursion < 2:

                counter_recursion += 1
                return self.select(table_name ,select, condition, order_by)


            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False

    #Query Result to list converter

    def dict_gen(self,curs):
        global counter_recursion
        try:
            import itertools
            field_names = [d[0] for d in curs.description]
            while True:
                rows = curs.fetchmany()
                if not rows: return
                for row in rows:

                    yield dict(itertools.izip(field_names, row))

        except (sqlite3.OperationalError,Exception):

            SharedApp.SharedApp.App.Database = Database()
            self = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                self.dict_gen(curs)


            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            pass

    #SQL Insert Query
    #@param table_name: Table Name
    #@param information: List of columns with Values (index as Column and Value as Column Value)
    #
    #@return: Insert Id of this record


    def insert(self, table_name, information):
        global counter_recursion
        try:

            query = 'INSERT INTO '+str(table_name)
            values = {}
            columnName = {}
            counter = 0

            for index in information:
                try:
                    columnName[str(counter)] = index
                    if self.Fixity.Configuration.getOsType() == 'Windows':
                        values[str(counter)] = information[index]
                    else:

                        try:
                            values[str(counter)] = str(information[index])
                        except:
                            values[str(counter)] = information[index]
                            pass

                    counter += 1
                except:
                    pass

            query = query + ' ( '+self.implode( columnName,  ',  ') + ' ) VALUES ( ' + self.implode(values,  ' , ', False) + ' ) '


            self.cursor.execute(query)
            self.commit()
            counter_recursion = 0
            return {'id':self.cursor.lastrowid}
        except (sqlite3.OperationalError,Exception):

            SharedApp.SharedApp.App.Database = Database()
            self = Database()

            if counter_recursion < 2:
                counter_recursion += 1
                return self.insert(table_name, information)

            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False

    #SQL Delete Query
    #@param table_name: Table Name
    #@param condition: Condition of which row will deleted
    #
    #@return: Response of Query Result

    def delete(self,table_name ,condition):
        global counter_recursion
        try:

            query = 'DELETE FROM '+str(table_name) + ' WHERE '+ condition
            response = self.sqlQuery(query)
            counter_recursion = 0
            return response
        except (sqlite3.OperationalError,Exception):

            SharedApp.SharedApp.App.Database = Database()
            self = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                return self.delete(table_name ,condition)

            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False

    #SQL Update Query
    #@param table_name: Table Name
    #@param information: List of columns with Values (index as Column and Value as Column Value)
    #@param condition: Condition of which row will deleted
    #
    #@return: Response of Query Result

    def update(self, table_name, information, condition):
        global counter_recursion
        try:

            query = 'UPDATE '+str(table_name) +' SET '
            counter = 0
            for single_info in information:

                    if counter == 0:
                        try:
                            query += str(single_info) + "='" + information[single_info].encode('utf-8') + "'"
                        except:
                            query += str(single_info) + "='" + str(information[single_info]) + "'"
                            pass
                    else:
                        try:
                            query += ' , '+ str(single_info) + "='" + information[single_info].encode('utf-8') + "'"
                        except:
                            query += ' , '+ str(single_info) + "='" + str(information[single_info]) + "'"
                            pass
                    counter = counter+1
            query += ' WHERE '+condition


            response = self.cursor.execute(query)
            self.commit()
            counter_recursion = 0
            return response

        except (sqlite3.OperationalError,Exception):


            SharedApp.SharedApp.App.Database = Database()
            self = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                return self.update(table_name, information, condition)

            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False

    #  Columns and records Implode for query
    #  @param information: Array of Value to be imploded
    #  @param glue: glue with values will be glued
    #  @param is_column: Given Information is of tables columns or Row
    #
    #  @return: Response of Query Result


    def implode(self,information , glue , is_column = True):
        try:

            counter = 0
            string_glued = ''
            for info in information:
                try:
                    if is_column:
                        if counter == 0:
                            string_glued = string_glued + information[info]
                        else:
                            string_glued =  string_glued + ' , ' + information[info]

                    else:

                        if counter == 0:
                            try:
                                string_glued = string_glued + ' "'+ str(information[info]) + '" '
                            except:
                                string_glued = string_glued + ' "'+ information[info] + '" '
                                pass
                        else:
                            try:
                                string_glued = string_glued + ' , "' + str(information[info]) + '" '
                            except:
                                string_glued = string_glued + ' , "' + information[info] + '" '
                                pass
                    counter += 1
                except:
                    pass

            return string_glued
        except (sqlite3.OperationalError,Exception):

            SharedApp.SharedApp.App.Database = Database()
            self = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                return self.implode(information , glue , is_column)
            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False