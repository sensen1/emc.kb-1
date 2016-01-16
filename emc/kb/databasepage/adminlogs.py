#-*- coding: UTF-8 -*-
from five import grok

from eisoo.operation import operation_session
from eisoo.operation.mapping_db import Adminlogs
from eisoo.operation.interfaces import IAdminlogsLocator
from eisoo.operation.utility import operationdate

from zope.interface import implements
from zope.component import getUtility

class AdminlogsLocator(grok.GlobalUtility):
    """
    """
    implements(IAdminlogsLocator)
    
    def Getconditionsloginlogs(self, **kwargs): 
        conditions = "rolename= '" + str(kwargs['rolename']) + "'"
        
        if kwargs['time'] != '-1':
            ago = operationdate.getdayofday(-int(kwargs['time']))
            conditions += " && date >= '" + str(ago.year) + "-" + str(ago.month) + "-" + str(ago.day) + "'"
        if kwargs['elevelname'] != '-1':
            conditions += " && elevelname = '" + str(kwargs['elevelname']) + "'"
                            
        star = kwargs['rows'] * int(kwargs['pages'])
        try:
            admin_logs = operation_session.query("username", "rolename", "levelname", "description", "date").from_statement("select * from admin_logs "
                                        "where " + str(conditions) + " order by date desc limit " + str(star) + "," + str(kwargs['rows'])).all()
            operation_session.commit()            
            return admin_logs  
        except:
            operation_session.rollback()
            raise                 
     
    def GetconditionslogsCount(self, **kwargs):
        """根据指定条件返回日志个数"""
        conditions = "rolename= '" + str(kwargs['rolename']) + "'"
        
        if kwargs['time'] != '-1':
            ago = operationdate.getdayofday(-int(kwargs['time']))
            conditions += " && date >= '" + str(ago.year) + "-" + str(ago.month) + "-" + str(ago.day) + "'"
        if kwargs['elevelname'] != '-1':
            conditions += " && elevelname = '" + str(kwargs['elevelname']) + "'"
                            
        
        try:
            admin_logs = operation_session.query("username", "rolename", "levelname", "description", "date").from_statement("select * from admin_logs "
                                        "where " + str(conditions) + " order by date desc").all()
            operation_session.commit()
            return len(admin_logs)
        except:
            operation_session.rollback()
            return 0
           
            
    
    def addadminlogs(self, **kwargs):
        """新增系统日志信息"""
        from eisoo.mpsource.interfaces import IUserLocator
        locator = getUtility(IUserLocator)
        
        if locator.IsUser(kwargs['username']):            
            adminlogs = Adminlogs()
            adminlogs.username = kwargs['username']
            adminlogs.rolename = kwargs['rolename']        
            adminlogs.levelname = kwargs['levelname']
            adminlogs.elevelname = kwargs['elevelname']
            adminlogs.description = kwargs['description']            
            adminlogs.date = kwargs['date']
            try:
                operation_session.add(adminlogs)
                operation_session.commit()
            except:
                operation_session.rollback()
                raise               
                
