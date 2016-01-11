#-*- coding: UTF-8 -*-
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import implements

from eisoo.operation import operation_session
from eisoo.market.mapping_db import ChannelMarketlogs
from eisoo.market.interfaces import IChannelMarketlogsLocator

from eisoo.market import MessageFactory as _

class AreaMarketlogsLocator(grok.GlobalUtility):
    implements(IChannelMarketlogsLocator)
    
    def AddChannelMarket(self,applyuser,channel,spent_fee):
        market = ChannelMarketlogs()
        market.applyuser = applyuser
        market.channel = channel
        market.spent_fee = spent_fee
        market.date = datetime.now()
        market.type = type
        operation_session.add(market)
        try:
            operation_session.commit()
        except:
            operation_session.rollback()
            raise