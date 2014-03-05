'''
Created on Feb 27, 2014

@author: Furqan
'''
import sqlite3 as sql
from os import   getcwd
from avp import DBHanlder
from DBObjectHanlder import DBObjectHanlder  as hanlder

class Database(hanlder):
    
    def __init__(self):
        super(hanlder,self).__init__()
        self._tableConfiguration = 'configuration'
        self._tableProject = 'project'
        self._tableProjectPath = 'projectPath'
        self._tableVersionDetail = 'versionDetail'
        self._tableVersions ='versions' 

    def sqlQuery(self, query):
        print(query)
        try:
            response = self.cursor.execute(query)
            return response
        except Exception as e:
            print(e[0])
            print('sqlQuery')
            try:
                self.closeConnection()                
                self.connect()
                response = self.cursor.execute(query)
                print(response)
                return response
            except:
                print(e[0])
                print('sqlQuery')
                pass

            
         
    def select(self,tableName , select  = '*' ,condition=None):
        try:
            query= ''
            query = 'SELECT '+ str(select) +' FROM '+str(tableName)
            if(condition != None):
                query += ' WHERE ' + condition
            
            response = {}
            responseCounter = 0
            for r in self.dict_gen(self.cursor.execute(query)):
                response[responseCounter] = r
                responseCounter =responseCounter + 1
            return response

        
        except Exception as e:
#             print('select')
#             print(e[0])
            self.con.close()
            self.closeConnection()
            pass
        finally:
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
                except Exception as e:
#                     print('insert')
#                     print(e[0])
                    self.con.close()
                    self.closeConnection()
                    pass
                finally:
                    pass
                
            query = query + ' ( '+self.implode ( columnName , ' , ' ) + ' ) VALUES ( ' + self.implode ( values , ' , ' , False ) + ' ) '
            self.sqlQuery(query)
            
            return {'id':self.cursor.lastrowid}
            
       
        
    def delete(self,tableName , condition):
        try:
            query = 'DELETE FROM '+str(tableName) + ' WHERE '+ condition
            return self.sqlQuery(query)
        except Exception as e:
#             print('delete')
#             print(e[0])
            self.con.close()
            self.closeConnection()
            return None
        finally:
            self.closeConnection()
    
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
                    self.connect()

                    return self.cursor.execute(query)
                except Exception as e:
                    print('update')
                    print(e[0])
                    self.con.close()
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
                            stringGlued = stringGlued + " '"+information[info] + "'"
                        else:
                            stringGlued =  stringGlued +" , '"    + information[info] + "'"
                    counter = counter + 1
                except Exception as e:
#                     print('implode')
#                     print(e[0])
                    self.con.close()
                    self.closeConnection()
                    pass
                finally:
                    pass
            return stringGlued
        
    
    def closeConnection(self):
        try:
            self.con.commit()
            self.con.close()
            self.con = None
            self = None
        except Exception as e:
#             print(e[0])
#             print('close')
            self.con.close()
            pass
        finally:
            self = None
            pass
        
    def getProjectInfo(self,projectName = None ,limit = True):
        
        self.connect()
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
        
        return response
      
    
    def getProjectPathInfo(self,projectID):
        
        
        self.connect()
        information = {}
        information['id'] = None
        response = self.select(self._tableProjectPath, '*', "projectID='"+str(projectID)+"'")
        self.closeConnection()
        return response


# print(1)
# try:
#     var1 = {'runWhenOnBattery': 1, 'durationType': 2, 'extraConf': '', 'title': u'New_Project', 'runDayOrMonth': '1', 'lastRan': None, 'selectedAlgo': 'sha256', 'filters': '', 'ifMissedRunUponRestart': 1, 'runTime': u'00:00:00', 'emailOnlyUponWarning': 1}
db = Database()
# db._tableProject
db.connect()
    
print(db.select(db._tableProject, '*'))
db.closeConnection()
#      
# except Exception as e :
#     print(e)
#     print(e[0])
    
    
# print(2)
# db1 = Database()
# db1.connect()
# db1.insert(db1._tableProject, var1)
# print(3)

        