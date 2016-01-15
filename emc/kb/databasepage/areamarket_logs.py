#-*- coding: UTF-8 -*-
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import implements

from eisoo.operation import operation_session
from emc.kb.mapping_db import AreaMarketlogs
from emc.kb.interfaces import IAreaMarketlogsLocator

from emc.kb import MessageFactory as _

class AreaMarketlogsLocator(grok.GlobalUtility):
    implements(IAreaMarketlogsLocator)
    
    def AddareaMarket(self,applyuser,areaid,spent_fee,state,type):
        """state=1扩张费用,state=2彩页费用"""
        market = AreaMarketlogs()
        market.applyuser = applyuser
        market.areaid = areaid
        market.spent_fee = spent_fee
        market.state = state
        market.type = type
        market.date = datetime.now()
        operation_session.add(market)
        try:
            operation_session.commit()
        except:
            operation_session.rollback()
            raise