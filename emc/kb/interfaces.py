#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope import schema
from zope.component.interfaces import IObjectEvent
from plone.app.textfield import RichText

from emc.kb import _

PROMOTIONS_PORTLET_COLUMN = u"plone.rightcolumn"

class IFollowedEvent(IObjectEvent):
    """pass"""

 
class IUnFollowedEvent(IObjectEvent):
    """ pass"""
  
class ILikeEvent(IObjectEvent):
    """ like event"""

class IUnLikeEvent(IObjectEvent):
    """ unlike event"""
    
class IFavoriteAnswerEvent(IObjectEvent):
    """pass"""
class IUnFavoriteAnswerEvent(IObjectEvent):
    """pass"""
class ICreatedMentionwoFolderEvent(IObjectEvent):
    """pass"""
    
class ICountAware(Interface):
    """ the marke interface of that object  can be countted """
    
class ICountNumEvent(IObjectEvent):
    """pass"""
    
class IClickEvent(IObjectEvent):
    """ Event gets fired when the object was viewed """

class ICountStatistics(IObjectEvent):
    """pass"""
    def updateCount(self):
        """update the count of the site"""
        
    def getCount(self):
        """get the conunt of the site"""
    
    def setCount(self):
        """set the conunt of the site"""

# Adapter question Evaluate
class IFollowing(Interface):
    followerNum = schema.Int(
            title=_(u"A score from 1-100"),
            readonly=True,
            )
    def available(userToken):
        """Evaluation of the legality of testing(existing users)
        """
                       
    def addFollow(userToken):
        """Give a positive (True) or negative (False) vote.
        """
        
    def delFollow(userToken):
        """Give a positive (True) or negative (False) vote.
        """  
# Adapter follow
class IFollowing(Interface):
    followerNum = schema.Int(
            title=_(u"A score from 1-100"),
            readonly=True,
            )
    def available(userToken):
        """Evaluation of the legality of testing(existing users)
        """
                       
    def addfollow(userToken):
        """Give a positive (True) or negative (False) vote.
        """
        
    def delFollow(userToken):
        """Give a positive (True) or negative (False) vote.
        """  
class IFollowable(Interface):
    "mark interface for following behavior"

# vote Adapter behavior interface
class IVoting(Interface):

    def voteavailabledisapproved(userToken):
        """  Evaluation of the legality of testing(existing users) 
         """
    def voteavailabledisapproved(userToken):
        """  Evaluation of the legality of testing(existing users) 
         """
    def favavailable(userToken):
        """Evaluation of the legality of testing(existing users)  
         """
    def voteNum(self):
        """the num of people who vote it"""
    
    def agree(userToken):
        """  agree the answer"""
    
    def disagree(userToken):
        """disagree the answer"""
        
# vote Adapter behavior mark interface
class IVotable(Interface):
    """mark interface"""        
 

class Iaddanswer(Interface):
    id = schema.ASCII(
            title=_(u"answer id"),
        )    

    content = RichText(
            title=_(u"content of the answer"),
            required=True,
        )
    voteNum = schema.Int(
            title=_(u"voteNum"),
            default=0,               
        )
    totalNum = schema.Int(
            title=_(u"totalNum"),
            default=0,
        )
    
# db insterface
class IModelLocator (Interface):
    """medel table add row"""
    
    def addModel(self):
        "add a model data"
        
    def queryModel(self):
        "query model by search condition"    
    