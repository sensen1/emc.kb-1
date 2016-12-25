#-*- coding: UTF-8 -*-
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import implements
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func

from emc.kb import kb_session
from emc.kb.mapping_db import Fashej,IFashej
from emc.kb.mapping_db import Jieshouj,IJieshouj
from emc.kb.mapping_db import Fashetx,IFashetx
from emc.kb.mapping_db import Jieshoutx,IJieshoutx
from emc.kb.mapping_db import Lvboq,ILvboq
from emc.kb.mapping_db import Dianxingtxzyzk,IDianxingtxzyzk
from emc.kb.mapping_db import ITianxianzyzk,Tianxianzyzk
from emc.kb.mapping_db import IJieshoujzk,Jieshoujzk
from emc.kb.mapping_db import IFashejzk,Fashejzk
from emc.kb.interfaces import IJieshoujLocator

from emc.kb import  _

class JieshoujLocator(grok.GlobalUtility):
    implements(IJieshoujLocator)
    
    def add(self,**kwargs):
        """parameters db jieshouj table"""
        recorder = Jieshouj()
        for kw in kwargs.keys():
            setattr(recorder,kw,kwargs[kw])
        kb_session.add(recorder)
        try:
            kb_session.commit()
        except:
            kb_session.rollback()
            pass
        
    def query(self,**kwargs):
        """以分页方式提取model 记录，参数：start 游标起始位置；size:每次返回的记录条数;
        fields:field list
        if size = 0,then不分页，返回所有记录集
        order_by(text("id"))
        """    
                            
        start = int(kwargs['start'])
        size = int(kwargs['size'])
#         fields = kwargs['fields']
        if size != 0:
            recorders = kb_session.query("sbdm", "sbmc","pcdm","location","fb_upper","fb_lower",
                                      "freq","bw_receiver","sen_receiver","mf_freq_sign",
                                      "mf_freq","lo_freq").\
            from_statement(
            text("select * from jieshouj  order by jieshoujId desc limit :start,:size").\
            params(start=start,size=size)).all()            
        else:
            nums = kb_session.query(func.count(Jieshouj.jieshoujId)).scalar()
            return int(nums) 
        try:
            kb_session.commit()            
            return recorders  
        except:
            kb_session.rollback()
            pass
    
    def DeleteByCode(self,sbdm):
        "delete the specify sbdm jieshouj recorder"

#         xhdm = kwargs['xhdm']
        if sbdm != "":
            try:
                recorder = kb_session.query(Jieshouj).\
                from_statement(text("SELECT * FROM jieshouj WHERE sbdm=:sbdm")).\
                params(sbdm=sbdm).one()
                kb_session.delete(recorder)                                                  
                kb_session.commit()           
            except:
                kb_session.rollback()
                pass
        else:
            return None
    
    def updateByCode(self,**kwargs):
        "update the speicy sbdm jieshouj recorder"
        
        """
        session.query(User).from_statement(text("SELECT * FROM users WHERE name=:name")).\
params(name='ed').all()
session.query(User).from_statement(
text("SELECT * FROM users WHERE name=:name")).params(name='ed').all()
        """

        sbdm = kwargs['sbdm']
        if sbdm != "":
            try:
                recorder = kb_session.query(Jieshouj).\
                from_statement(text("SELECT * FROM jieshouj WHERE sbdm=:sbdm")).\
                params(sbdm=sbdm).one()
                updatedattrs = [kw for kw in kwargs.keys() if kw != 'sbdm']
                for kw in updatedattrs:
                    setattr(recorder,kw,kwargs[kw])                                                  
                kb_session.commit()           
            except:
                kb_session.rollback()
                pass
        else:
            return None

    def getByCode(self,sbdm):
        if sbdm != "":
            try:
                recorder = kb_session.query(Jieshouj).\
                from_statement(text("SELECT * FROM jieshouj WHERE sbdm=:sbdm")).\
                params(sbdm=sbdm).one()
                return recorder          
            except:
                kb_session.rollback()
                None
        else:
            return None
                                