# -*- coding: UTF-8 -*-
#Created on May 14, 2014
#
#@author: Furqan Wasi <furqan@avpreserve.com>
import plistlib

from Core import SharedApp
import sqlite3, _winreg,os
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
    def getInstance(is_unit_test = False):
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
            Database._instance.connect(is_unit_test)

        return Database._instance

    def selfDestruct(self):
        del self

    def connect(self, is_unit_test=False):
        """
        connect To Database
        @param is_unit_test: is call came from unit test

        @return Connect Instance
        """
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

    def getOne(self, query):
        """
        Get one record using given sql query
        @param query: SQL Raw Query

        @return: One sQuery Result
        """
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

    def sqlQuery(self, query):
        """
        SQL Query Runner
        @param query: SQL Raw Query

        @return: Query Result
        """
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

    def getProjectInfo(self,project_name = None, limit = True):
        """
        Get Project Information
        @param project_name: Project Name to be searched in database
        @param limit: If Ture 1 limit with be applied

        @return project information
        """
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

    def getProjectPathInfo(self ,project_id ,version_id):
        """
        Get Projects paths Information
        @param project_id: Project ID
        @param version_id: ID of Version of Project to be fetched

        @return project information
        """
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

    def getConfiguration(self):
        global counter_recursion
        information = {}
        if self.Fixity.Configuration.getOsType() == 'Windows':
            try:
                global counter_recursion
                keyval = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
                root_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyval, 0, _winreg.KEY_READ)
                [email, regtype] = (_winreg.QueryValueEx(root_key, "fixityEmail"))
                [smtp, regtype] = (_winreg.QueryValueEx(root_key, "fixitySMTP"))
                [passwrd, regtype] = (_winreg.QueryValueEx(root_key, "fixityPass"))
                [port, regtype] = (_winreg.QueryValueEx(root_key, "fixityPort"))
                [protocol, regtype] = (_winreg.QueryValueEx(root_key, "fixityProtocol"))
                [debugg, regtype] = (_winreg.QueryValueEx(root_key, "fixityDebugger"))
                _winreg.CloseKey(root_key)
                information['smtp'] = smtp
                information['email'] = email
                information['pass'] = self.Fixity.Configuration.decrypt_val(passwrd)
                information['port'] = int(port)
                information['protocol'] = protocol
                information['debugger'] = int(debugg)
                counter_recursion = 0
                return information
            except WindowsError:
                if counter_recursion < 2:
                    counter_recursion += 1
                return self.getConfiguration()
            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False
        else:
            try:
                pl = plistlib.readPlist("~/Library/Preferences/Fixity.plist")
                information['smtp'] = pl["smtp"]
                information['email'] = pl["email"]
                information['pass'] = self.Fixity.Configuration.decrypt_val(pl["passwrd"])
                information['port'] = pl["port"]
                information['protocol'] = pl["protocol"]
                information['debugger'] = pl["debugger"]
                counter_recursion = 0
                return information
            except IOError:
                if counter_recursion < 2:
                    counter_recursion += 1
                return self.getConfiguration()
            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False


    def getVersionDetails(self, project_id, version_id, OrderBy = None):
        """
        Get Version Details
        @param project_id: Project ID
        @param version_id: Project ID
        """
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

    def getConfigInfo(self, project=None):
        """
        Fetch information related to email configuration
        """
        global counter_recursion
        information = {}
        if self.Fixity.Configuration.getOsType() == 'Windows':
            try:
                global counter_recursion
                keyval = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
                root_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyval, 0, _winreg.KEY_READ)
                [email, regtype] = (_winreg.QueryValueEx(root_key, "fixityEmail"))
                [smtp, regtype] = (_winreg.QueryValueEx(root_key, "fixitySMTP"))
                [passwrd, regtype] = (_winreg.QueryValueEx(root_key, "fixityPass"))
                [port, regtype] = (_winreg.QueryValueEx(root_key, "fixityPort"))
                [protocol, regtype] = (_winreg.QueryValueEx(root_key, "fixityProtocol"))
                [debugg, regtype] = (_winreg.QueryValueEx(root_key, "fixityDebugger"))
                _winreg.CloseKey(root_key)
                information['smtp'] = smtp
                information['email'] = email
                information['pass'] = self.Fixity.Configuration.decrypt_val(passwrd)
                information['port'] = int(port)
                information['protocol'] = protocol
                information['debugger'] = int(debugg)
                counter_recursion = 0
                return information

            except WindowsError:
                if counter_recursion < 2:
                    counter_recursion += 1
                return self.getConfigInfo(project)
                counter_recursion = 0
                self.Fixity.logger.LogException(Exception.message)
                return False
        else:
            try:
                pl = plistlib.readPlist("~/Library/Preferences/Fixity.plist")
                information['smtp'] = pl["smtp"]
                information['email'] = pl["email"]
                information['pass'] = self.Fixity.Configuration.decrypt_val(pl["passwrd"])
                information['port'] = pl["port"]
                information['protocol'] = pl["protocol"]
                information['debugger'] = pl["debugger"]
                counter_recursion = 0
                return information
            except IOError:
                if counter_recursion < 2:
                    counter_recursion += 1
                return self.getConfiguration()
            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False
        return {}

    def getVersionDetailsLast(self, project_id):
        """
        Get Last Inserted Version of given project

        @param project_id: Project ID
        """
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

    def listToTuple(self, provided_list):
        """
        Convert List to Tuple Data type
        """
        global counter_recursion
        try:
            new_list = []
            for single_of_provided_list in  provided_list:
                new_list.append(provided_list[single_of_provided_list])
            return tuple(new_list)

        except (sqlite3.OperationalError,Exception):

            SharedApp.SharedApp.App.Database = Database()
            self = Database()
            if counter_recursion < 2:
                counter_recursion += 1
                return self.listToTuple(provided_list)

            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False

    def commit(self):
        self.con.commit()

    def select(self,table_name, select='*', condition=None, order_by=None):
        """
        SQL Select Query
        @param table_name: Table Name
        @param select: Column To Select
        @param condition: Conditions as String
        @param order_by: order By Columns

        @return: Query Result
        """
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

    def dict_gen(self,curs):
        """
        Query Result to list converter
        """
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

    def insert(self, table_name, information):
        """
        SQL Insert Query
        @param table_name: Table Name
        @param information: List of columns with Values (index as Column and Value as Column Value)

        @return: Insert Id of this record
        """
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

            query = query + ' ( ' + self.implode( columnName,  ',  ') + ' ) VALUES ( ' + self.implode( values,  ' , ', False ) + ' ) '

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

            self.Fixity.logger.LogException(Exception.message)
            return False

    def delete(self, table_name, condition):
        """
        SQL Delete Query
        @param table_name: Table Name
        @param condition: Condition of which row will deleted

        @return: Response of Query Result
        """
        global counter_recursion
        try:

            query = 'DELETE FROM ' + str(table_name) + ' WHERE ' + condition
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

    def update(self, table_name, information, condition):
        """
        SQL Update Query
        @param table_name: Table Name
        @param information: List of columns with Values (index as Column and Value as Column Value)
        @param condition: Condition of which row will deleted

        @return: Response of Query Result
        """
        global counter_recursion
        try:

            query = 'UPDATE '+str(table_name) + ' SET '
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

    def implode(self,information, glue, is_column=True):
        """
        Columns and records Implode for query
        @param information: Array of Value to be imploded
        @param glue: glue with values will be glued
        @param is_column: Given Information is of tables columns or Row

        @return: Response of Query Result
        """
        try:

            counter = 0
            string_glued = ''
            for info in information:
                try:
                    if is_column:
                        if counter == 0:
                            string_glued = string_glued + information[info]
                        else:
                            string_glued = string_glued + ' , ' + information[info]
                    else:
                        if counter == 0:
                            try:
                                string_glued = string_glued + ' "' + str(information[info]) + '" '
                            except:
                                string_glued = string_glued + ' "' + information[info] + '" '
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
            global counter_recursion

            SharedApp.SharedApp.App.Database = Database()
            self = Database()

            if counter_recursion < 2:
                counter_recursion += 1
                return self.implode(information , glue , is_column)

            counter_recursion = 0
            self.Fixity.logger.LogException(Exception.message)
            return False