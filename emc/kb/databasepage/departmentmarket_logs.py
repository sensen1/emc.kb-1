#-*- coding: UTF-8 -*-
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import implements

from eisoo.operation import operation_session
from eisoo.market.mapping_db import DepartmentMarketlogs
from eisoo.market.interfaces import IDepartmentMarketlogsLocator

from eisoo.market import MessageFactory as _


class DepartmentMarketlogsLocator(grok.GlobalUtility):
    implements(IDepartmentMarketlogsLocator)
    
    def AdddepartmentMarket(self,applyuser,departmentid,spent_fee,type):
        try:
            market = DepartmentMarketlogs()
            market.applyuser = applyuser
            market.departmentid = departmentid
            market.spent_fee = spent_fee
            market.date = datetime.now()
            market.type = type
            operation_session.add(market)
            operation_session.commit()
        except:
            operation_session.rollback()
            raise