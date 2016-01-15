#-*- coding: UTF-8 -*-
from zope import interface
from zope.component.interfaces import ObjectEvent

from emc.kb.interfaces import IFollowedEvent
from emc.kb.interfaces import IUnFollowedEvent
from emc.kb.interfaces import ILikeEvent
from emc.kb.interfaces import IUnLikeEvent
from emc.kb.interfaces import IFavoriteAnswerEvent
from emc.kb.interfaces import IUnFavoriteAnswerEvent
from emc.kb.interfaces import IClickEvent
from emc.kb.interfaces import ICountStatistics
from emc.kb.interfaces import ICreatedMentionwoFolderEvent
from emc.kb.interfaces import ICountNumEvent


    
class FollowedEvent(ObjectEvent):
    interface.implements(IFollowedEvent)


class UnFollowedEvent(ObjectEvent):
    interface.implements(IUnFollowedEvent)
    

    
class LikeEvent(ObjectEvent):
    interface.implements(ILikeEvent)
    
class UnLikeEvent(ObjectEvent):
    interface.implements(IUnLikeEvent)
    
class FavoriteAnswerEvent(ObjectEvent):
    """取消收藏事件"""
    interface.implements(IFavoriteAnswerEvent)

class UnFavoriteAnswerEvent(ObjectEvent):
    interface.implements(IUnFavoriteAnswerEvent)   

class CreatedMentionwoFolderEvent(ObjectEvent):
    interface.implements(ICreatedMentionwoFolderEvent)   

class ClickEvent(ObjectEvent):
    interface.implements(IClickEvent)

class CountStatistics(ObjectEvent):
    interface.implements(ICountStatistics)

class CountNumEvent(ObjectEvent):
    interface.implements(ICountNumEvent)  

 
