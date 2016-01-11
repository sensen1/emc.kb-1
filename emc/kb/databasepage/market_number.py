#-*- coding: UTF-8 -*-
from five import grok

from zope import schema
from zope.interface import implements

from eisoo.operation import operation_session
from eisoo.market.mapping_db import Market_number
from eisoo.market.interfaces import IMarket_numberLocator

from eisoo.market import MessageFactory as _


class market_numberLocator(grok.GlobalUtility):
    implements(IMarket_numberLocator)
    
    def AddNumber(self,num,state):
        """添加一个礼品记录
        """
        number = Market_number()
        number.number = num
        number.state = state
        operation_session.add(number)
        try:
            operation_session.commit()
        except:
            operation_session.rollback()
            raise
        
    def IsNumber(self,num,state):
        """判断一个号码是否属于礼品"""
        results = operation_session.query(Market_number).filter(Market_number.number==num).filter(Market_number.state==state).all()
                    
        if len(results)==0:
            return True
        else: 
            return False
        
        
        
        