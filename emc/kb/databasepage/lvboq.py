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
from emc.kb.interfaces import ILvboqLocator

from emc.kb import  _

class LvboqLocator(grok.GlobalUtility):
    implements(ILvboqLocator)
    
    def add(self,kwargs):
        """parameters db lvboq table"""
        recorder = Lvboq()
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
            recorders = kb_session.query("cssbdm", "cssbmc","pcdm","location",
                                      "fb_upper","fb_lower","freq",
                                      "f_upper","f_lower","order1","s21").\
            from_statement(
            text("select * from lvboq  order by lvboqId desc limit :start,:size").\
            params(start=start,size=size)).all()            
        else:
            nums = kb_session.query(func.count(Lvboq.lvboqId)).scalar()
            return int(nums) 
        try:
            kb_session.commit()            
            return recorders  
        except:
            kb_session.rollback()
            pass
    
    def DeleteByCode(self,cssbdm):
        "delete the specify cssbdm lvboq recorder"

#         xhdm = kwargs['xhdm']
        if cssbdm != "":
            try:
                recorder = kb_session.query(Lvboq).\
                from_statement(text("SELECT * FROM lvboq WHERE cssbdm=:cssbdm")).\
                params(cssbdm=cssbdm).one()
                kb_session.delete(recorder)                                                  
                kb_session.commit()           
            except:
                kb_session.rollback()
                pass
        else:
            return None
    
    def updateByCode(self,kwargs):
        "update the speicy cssbdm lvboq recorder"
        
        """
        session.query(User).from_statement(text("SELECT * FROM users WHERE name=:name")).\
params(name='ed').all()
session.query(User).from_statement(
text("SELECT * FROM users WHERE name=:name")).params(name='ed').all()
        """

        cssbdm = kwargs['cssbdm']
        if cssbdm != "":
            try:
                recorder = kb_session.query(Lvboq).\
                from_statement(text("SELECT * FROM lvboq WHERE cssbdm=:cssbdm")).\
                params(cssbdm=cssbdm).one()
                updatedattrs = [kw for kw in kwargs.keys() if kw != 'cssbdm']
                for kw in updatedattrs:
                    setattr(model,kw,kwargs[kw])                                                  
                kb_session.commit()           
            except:
                kb_session.rollback()
                pass
        else:
            return None

    def getByCode(self,cssbdm):
        if cssbdm != "":
            try:
                recorder = kb_session.query(Lvboq).\
                from_statement(text("SELECT * FROM lvboq WHERE cssbdm=:cssbdm")).\
                params(cssbdm=cssbdm).one()
                return recorder          
            except:
                kb_session.rollback()
                None
        else:
            return None
                                