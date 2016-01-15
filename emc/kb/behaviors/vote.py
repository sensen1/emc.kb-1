#-*- coding: UTF-8 -*-
from five import grok
from persistent.list import PersistentList
from Acquisition import aq_parent
from zExceptions import Forbidden
from zope.component import getMultiAdapter
from zope.lifecycleevent.interfaces import IObjectAddedEvent,IObjectRemovedEvent
from zope.annotation.interfaces import IAnnotations
from Products.CMFCore.utils import getToolByName
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from zope import component
from zope.component import adapter
from zope.interface import implementer

from emc.kb.contents.answer import Ianswer
from emc.kb.contents.question import Iquestion
from plone.dexterity.interfaces import IDexterityContent
from emc.kb.events import LikeEvent,UnLikeEvent,FavoriteAnswerEvent,UnFavoriteAnswerEvent
from emc.kb.interfaces import IVoting,ILikeEvent,IUnLikeEvent,IFavoriteAnswerEvent,IUnFavoriteAnswerEvent


APPROVED_KEY = 'emc.kb.approved'
DISAPPROVED_KEY = 'emc.kb.disapproved'


@implementer(IVoting)
@adapter(IDexterityContent)
class Vote(object):
    """vote behavior adapter"""
    
    def __init__(self, context):
        self.context = context
        
        annotations = IAnnotations(context)
        if APPROVED_KEY not in annotations.keys():
            annotations[APPROVED_KEY] = PersistentList()        
        #投赞成票的用户id 队列
        self.approved = annotations[APPROVED_KEY]
        if DISAPPROVED_KEY not in annotations.keys():
            annotations[DISAPPROVED_KEY] = PersistentList()        
        #投反对票的用户id 队列        
        self.disapproved = annotations[DISAPPROVED_KEY]        
    

    @property
    def voteNum(self):
        '赞成票的总票数'
        VoteNum = len(self.approved)
        return VoteNum
          
    def voteavailableapproved(self,userToken):
        '指定的用户是否在赞成队列里'
        return (userToken in self.approved )         
#         return self.approved.has_key(userToken)
    
    def voteavailabledisapproved(self,userToken):
        '指定的用户是否在反对队列里'        
        return (userToken in self.disapproved)        
#         return self.disapproved.has_key(userToken)
    
    def agree(self, userToken):
        '投赞成票'

        if  not self.voteavailableapproved(userToken):
           self.approved.append(userToken)
        elif  self.voteavailableapproved(userToken):
            self.disapproved.remove(userToken)
        else:
            raise KeyError("Ratings not available for %s" % userToken)
                  
    def disagree(self,userToken):
        if  not self.voteavailabledisapproved(userToken):
            self.disapproved.append(userToken)
#         elif  self.voteavailabledisapproved(userToken):
#             self.disapproved.remove(userToken)
        else:
            raise KeyError("Ratings not available for %s" % userToken)
        
#     def favavailable(self, userToken):
#         return  self.favorite.has_key(userToken)  
#     
#     def addfavorite(self,userToken):
#         if not self.favavailable(userToken):
#             self.favorite.insert(userToken)
#         else:
#             raise KeyError("The %s is concerned about" % userToken)
#     
#     def delfavorite(self,userToken):
#         if self.favavailable(userToken):
#             self.favorite.remove(userToken)
#         else:
#            raise KeyError("The %s is not concerned about" % userToken)
        
@grok.subscribe(Ianswer, ILikeEvent)
def approve(obj, event):
    """approve the answer"""

    mp = getToolByName(obj,'portal_membership')
    userobject= mp.getAuthenticatedMember()
    username = userobject.getId()
    agreelist = list(userobject.getProperty('mylike'))
    
    if not obj.id in agreelist:
        agreelist.append(obj.id)
        userobject.setProperties(mylike=agreelist)

    evlute = IVoting(obj)
    if not evlute.voteavailableapproved(username):
        evlute.agree(username)
        obj.voteNum = evlute.voteNum
        obj.totalNum = evlute.voteNum - len(evlute.disapproved)
        obj.reindexObject()
        
@grok.subscribe(Ianswer, IUnLikeEvent)
def disapprove(obj, event):
    """approve the answer"""
    
    mp = getToolByName(obj,'portal_membership')
    userobject= mp.getAuthenticatedMember()
    username = userobject.getId()
    disagreelist = list(userobject.getProperty('myunlike'))
    
    if not obj.id in disagreelist:
        disagreelist.append(obj.id)
        userobject.setProperties(myunlike=disagreelist)
    
    evlute = IVoting(obj)
    if not evlute.voteavailabledisapproved(username):
        evlute.disagree(username)
        obj.voteNum = evlute.voteNum
        obj.totalNum = evlute.voteNum - len(evlute.disapproved)
        obj.reindexObject() 
        
# @grok.subscribe(Ianswer, IFavoriteAnswerEvent)
# def FavoriteAnswer(obj,event):
#     """add the answer to favorite"""
#     
#     mp = getToolByName(obj,'portal_membership')
#     userobject = mp.getAuthenticatedMember()
#     username = userobject.getId()
#     favoritelist = list(userobject.getProperty('myfavorite'))
#     
#     if not obj.id in favoritelist:
#         favoritelist.append(obj.id)
#         userobject.setProperties(myfavorite=favoritelist)
#         
#     evlute = IVoting(obj)
#     if not evlute.favavailable(username):
#         evlute.addfavorite(username)
# 
# @grok.subscribe(Ianswer, IUnFavoriteAnswerEvent)
# def UnFavoriteAnswer(obj,event):
#     """del the answer from the favorite"""
#     mp = getToolByName(obj,'portal_membership')
#     userobject = mp.getAuthenticatedMember()
#     username = userobject.getId()
#     favoritelist = list(userobject.getProperty('myfavorite'))
#     
#     if  obj.id in favoritelist:
#         favoritelist.remove(obj.id)
#         userobject.setProperties(myfavorite=favoritelist)
#         
#     evlute = IVoting(obj)
#     if evlute.favavailable(username):
#         evlute.delfavorite(username)
        
# @grok.subscribe(Ianswer, IObjectRemovedEvent)
# def delAnswer(obj,event):
#     favoriteevlute = IVoting(obj)
#     """判断当前答案是否被收藏"""
#     answerlist = favoriteevlute.favorite
#     if len(answerlist) == 0:
#         return
#     
#     pm = getToolByName(obj, 'portal_membership')
#     for answer in answerlist:
#         userobject=pm.getMemberById(answer)
#         """删除用户收藏到答案"""
#         favoritelist = list(userobject.getProperty('myfavorite'))
#         favoritelist.remove(obj.getId())

@grok.subscribe(Ianswer, IObjectRemovedEvent)
def delAnswertopicscore(obj,event):
    """计算关联回答的topic分数"""
    questionobject = aq_parent(obj)
    
    intids = getUtility(IIntIds)  
    intid = intids.getId(questionobject)
    catalog = component.getUtility(ICatalog) 
    qlist = sorted(catalog.findRelations({'from_id': intid}))
    """修改问题关联到所有话题"""
    if len(qlist) == 0: return
    for q in qlist:
        topicobject = q.to_object
        topicobject.topicscore = topicobject.topicscore - 0.3
        topicobject.reindexObject()
        