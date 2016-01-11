#-*- coding: UTF-8 -*-
import sqlalchemy.types
import sqlalchemy.schema

from five import grok

from zope import schema
from zope.interface import Interface,implements

from emc.kb import ORMBase
from emc.kb import MessageFactory as _

class IMarket_number(Interface):
    """编号number 记录表
    """
    id = schema.Int(
            title=_(u"gift_number id"),
        )    
    
    number = schema.Int(
            title=_(u"gift number"),
        )
    
    state = schema.Int(
            title=_(u"gift state"),
        )
class Market_number(ORMBase):
    """Database-backed implementation of IGift_number
    """
    implements(IMarket_number)
    
    __tablename__ = 'market_number'
    
    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            primary_key=True,
            autoincrement=True,
        )
        
    number = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            nullable=False,
        )
    state = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            nullable=False,
        )
    
class IDepartmentMarketlogs(Interface):
    """部门报销记录
    """
    id = schema.Int(                
        title = _(u"IDepartmentMarketlogs id"),
        )
    
    applyuser = schema.TextLine(
        title = _(u"IDepartmentMarketlogs applyuser")
        )        
    departmentid = schema.TextLine(
            title = _(u"IDepartmentMarketlogs departmentid")
            )
    spent_fee = schema.Float(
            title = _(u"IDepartmentMarketlogs spent_fee")
            )
    date = schema.Datetime(
            title = _(u"IDepartmentMarketlogs date")
            )    
    type = schema.Int(
            title=_(u"IDepartmentMarketlogs type"),
        )
class DepartmentMarketlogs(ORMBase):
    """部门报销记录"""
    implements(IDepartmentMarketlogs)
    __tablename__ = 'departmentmarket_logs'
    
    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
                primary_key=True,
                autoincrement=True,
                )
    applyuser = sqlalchemy.schema.Column(sqlalchemy.types.String(128),
        nullable=False,
        )
    departmentid = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            nullable=False,
            )
    spent_fee = sqlalchemy.schema.Column(sqlalchemy.types.Float(),
            nullable=False,
            )
    date = sqlalchemy.schema.Column(sqlalchemy.types.DateTime(),
            nullable=False,
            )
    type = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            nullable=False,
            )
    
class IAreaMarketlogs(Interface):
    """区域申请报销记录
    """
    id = schema.Int(                
        title = _(u"IAreaMarketlogs id"),
        )
    
    applyuser = schema.TextLine(
        title = _(u"IAreaMarketlogs applyuser")
        )        
    
    areaid = schema.TextLine(
            title = _(u"IAreaMarketlogs areaid")
            )
    spent_fee = schema.Float(
            title = _(u"IAreaMarketlogs spent_fee")
            )
    date = schema.Datetime(
            title = _(u"IAreaMarketlogs date")
            )
    state =   schema.Int(
            title = _(u"IAreaMarketlogs state")
            )
    type = schema.Int(
            title=_(u"IAreaMarketlogs type"),
        )
class AreaMarketlogs(ORMBase):
    """区域申请报销记录
    """
    implements(IAreaMarketlogs)
    __tablename__ = 'areamarket_logs'
    
    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
                primary_key=True,
                autoincrement=True,
                )
    applyuser = sqlalchemy.schema.Column(sqlalchemy.types.String(128),
                nullable=False,
                )
    areaid = sqlalchemy.schema.Column(sqlalchemy.types.String(15),
                nullable=False,
                )
    spent_fee = sqlalchemy.schema.Column(sqlalchemy.types.Float(),
                nullable=False,
                )
    date = sqlalchemy.schema.Column(sqlalchemy.types.DateTime(),
                nullable=False,
                )
    state = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
                nullable=False,
                )
    type = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            nullable=False,
            )

class IChannelMarketlogs(Interface):
    """签约代理所记录
    """
    id = schema.Int(                
        title = _(u"IChannellogs id"),
        )
    
    applyuser = schema.TextLine(
        title = _(u"IChannellogs applyuser")
        )        
    chanel = schema.TextLine(
            title = _(u"IChannellogs channel")
            )
    spent_fee = schema.Float(
            title = _(u"IChannellogs spent_fee")
            )
    date = schema.Datetime(
            title = _(u"IChannellogs date")
            )    
    type = schema.Int(
            title=_(u"IChannellogs type"),
        )
class ChannelMarketlogs(ORMBase):
    """部门报销记录"""
    implements(IChannelMarketlogs)
    __tablename__ = 'channelmarket_logs'
    
    id = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
                primary_key=True,
                autoincrement=True,
                )
    applyuser = sqlalchemy.schema.Column(sqlalchemy.types.String(128),
        nullable=False,
        )
    channel = sqlalchemy.schema.Column(sqlalchemy.types.String(128),
            nullable=False,
            )
    spent_fee = sqlalchemy.schema.Column(sqlalchemy.types.Float(),
            nullable=False,
            )
    date = sqlalchemy.schema.Column(sqlalchemy.types.DateTime(),
            nullable=False,
            )
    type = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
            nullable=False,
            )