from sqlalchemy import orm
import datetime
from sqlalchemy import select , schema, types  

from BaseVersions import BaseVersions
from BaseConfiguration import BaseConfiguration
from BaseVersionDetail import BaseVersionDetail
from BaseProjectPath import BaseProjectPath
from BaseProject import BaseProject

metadata = schema.MetaData()

def now():
    return datetime.datetime.now()

project_table = schema.Table('project', metadata,
    schema.Column('id', types.Integer, schema.Sequence('project_seq_id', optional=True), primary_key=True),
    schema.Column('versionCurrentID', types.Integer, schema.ForeignKey('versions.id'), nullable = False),
    schema.Column('title', types.String(255)),
    
    # 0=Monthly, 1=Weekly, 2=Daily 
    schema.Column('durationType', types.Integer),
    schema.Column('runTime', types.String(10)),
    schema.Column('runDayOrMonth', types.String(12)),
    schema.Column('selectedAlgo', types.String(8), default = u'sha256' ),
    schema.Column('filters', types.Text, nullable=True , default = u''),
    schema.Column('runWhenOnBattery', types.SmallInteger, default = 1 ),
    schema.Column('ifMissedRunUponRestart', types.SmallInteger, default = 1),
    schema.Column('emailOnlyUponWarning', types.SmallInteger, default = 1 ),
    schema.Column('emailAddress', types.Text, default = 1 ),
    schema.Column('extraConf', types.Text, default = None),
    schema.Column('lastRan', types.DateTime(), default = None),
    schema.Column('updatedAt', types.DateTime() , default = now),
    schema.Column('createdAt', types.DateTime() , default = now),
)
projectPath_table = schema.Table('projectPath', metadata,
    schema.Column('id', types.Integer, schema.Sequence('project_seq_id', optional=True), primary_key = True),
    schema.Column('projectID', types.Integer, schema.ForeignKey('project.id'), nullable = False),
    schema.Column('versionID', types.Integer, schema.ForeignKey('versions.id'), nullable = True),
    schema.Column('path', types.Text, nullable = False),
    schema.Column('pathID', types.String(15), nullable = False),
    schema.Column('updatedAt', types.DateTime() , default = now),
    schema.Column('createdAt', types.DateTime() , default = now),
    
)

versions_table = schema.Table('versions', metadata,
    schema.Column('id', types.Integer, schema.Sequence('versions_seq_id', optional=True), primary_key=True),
#     schema.Column('projectID', types.Integer, schema.ForeignKey('project.id'), nullable=False),
    schema.Column('versionType', types.String(10) , nullable = False),
    schema.Column('name', types.String(255) , nullable = False),
    schema.Column('updatedAt', types.DateTime() , default=now),
    schema.Column('createdAt', types.DateTime() , default=now),
)

versionDetail_table = schema.Table('versionDetail', metadata,
    schema.Column('id', types.Integer,schema.Sequence('vd_seq_id', optional=True), primary_key=True),
    schema.Column('versionID', types.Integer, schema.ForeignKey('versions.id'), nullable=False),
    schema.Column('projectID', types.Integer, schema.ForeignKey('project.id'), nullable=False),
    schema.Column('projectPathID', types.Integer, schema.ForeignKey('projectPath.id'), nullable = False),
    schema.Column('md5_hash', types.Text , nullable = False),
    schema.Column('ssh256_hash', types.Text , nullable = False),
    schema.Column('path', types.Text, nullable = False),
    schema.Column('inode', types.Text, nullable = False),
    schema.Column('updatedAt', types.DateTime() , default=now),
    schema.Column('createdAt', types.DateTime() , default=now),
)

configuration_table = schema.Table('configuration', metadata,
    schema.Column('id', types.Integer, schema.Sequence('conf_seq_id', optional=True), primary_key=True),
#     schema.Column('projectID', types.Integer, schema.ForeignKey('project.id'), nullable=False),
    schema.Column('smtp', types.Text ,default=u'' , nullable = True),
    schema.Column('email', types.Text, default=u'' , nullable = True),
    schema.Column('pass', types.Text, default=u'' , nullable = True),
    schema.Column('port', types.Integer, default=u'' , nullable = True),
    schema.Column('protocol', types.Text, default=u'' , nullable = True),
    
    # 0=off, 1=off 
    schema.Column('debugger', types.SmallInteger, default=0),
    schema.Column('updatedAt', types.DateTime() , default=now),
    schema.Column('createdAt', types.DateTime() , default=now),
)



class Configuration(BaseConfiguration):
    pass

class Project(BaseProject):
    pass

class Versions(BaseVersions):
    pass

class VersionDetail(BaseVersionDetail):
    pass

class ProjectPath(BaseProjectPath):
    pass

orm.mapper(Project, project_table, properties={
        'Versions':orm.relation(Versions, backref='project_versions'),
        'Configuration':orm.relation(Configuration, backref='project_configuration'),
        'ProjectPath':orm.relation(ProjectPath, backref='project_projectPath'),
        'VersionDetail':orm.relation(VersionDetail, backref='project_versionDetail')
});
# 
orm.mapper(Versions, versions_table,properties={
#     'Project':orm.relation(Project, backref='versions_project'),
    });
orm.mapper(Configuration, configuration_table,properties={
        'Project':orm.relation(Project, backref='Configuration_project'),
    });
     
orm.mapper(VersionDetail, versionDetail_table,properties={
        'Versions':orm.relation(Versions, backref='versionDetail_versions'),
        'Project':orm.relation(Project, backref='versionDetai_project'),
    });
     
orm.mapper(ProjectPath, projectPath_table,properties={
        'Versions':orm.relation(Versions, backref='projectPath_versions'),
        'Project':orm.relation(Project, backref='projectPath_project'),
    });
