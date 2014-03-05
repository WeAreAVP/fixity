'''
Created on Feb 27, 2014

@author: Furqan
'''
from avp import DBHanlder

class Database(object):
    def __init__(self):
        self.ConfigurationObj = None
        self.VersionsObj = None
        self.VersionDetailObj = None
        self.ProjectPathObj = None  
        self.ProjectObj = None
        self.dbSession = DBHanlder.session
        self.DBHanlder = DBHanlder
        
    def initProjectObj(self):
        self.ProjectObj = self.DBHanlder.model.Project()
        self.ProjectCls = self.DBHanlder.model.Project
     
    def initVersionsObj(self):
        
        self.VersionsObj =  self.DBHanlder.model.Versions()
        self.VersionsCls = self.DBHanlder.model.Versions
    
    def initVersionDetailObj(self):
        self.VersionDetailObj =  self.DBHanlder.model.VersionDetail()
        self.VersionDetailCls = self.DBHanlder.model.VersionDetail
    
    def initProjectPathObj(self):
        self.ProjectPathObj =  self.DBHanlder.model.ProjectPath()
        self.ProjectPathCls = self.DBHanlder.model.ProjectPath
        
    
    def initConfigurationObj(self):
        self.ConfigurationObj = self.DBHanlder.model.Configuration()
        self.ConfigurationCls = self.DBHanlder.model.Configuration
        
    def queryTableBased(self, Cls,condition = None):
        query = None
        if condition:
            query =  self.dbSession.query(Cls).filter(str(condition))
        else:
            query =  self.dbSession.query(Cls)
            
        return self.dbSession.execute(str(query))
    
    def query(self, query):
        return self.dbSession.execute(str(query))

    
    def getById(self, Cls , ConditionalId ):
        page_q =  self.dbSession.query(Cls)
        return page_q.get(ConditionalId)
                     
    def save(self, obj):
        self.dbSession.add(obj)
        self.dbSession.flush()
        self.dbSession.commit()
        
    def delete(self, obj):
        self.dbSession.delete(obj) 

db1 = Database()
# db1.initConfigurationObj()

# page_q =  db1.queryTableBased(db1.ConfigurationCls)
# print(page_q)
# for page in page_q:
#     print(page.email)

page_q = db1.dbSession.query(DBHanlder.model.Configuration)
ressult =page_q.all()
print(ressult)
# for page in page_q:
#   print page

# print(SingleResult.id)
exit()