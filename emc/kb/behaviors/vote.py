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
from emc.kb.interfaces import IVoting,IVotable,ILikeEvent,IUnLikeEvent,IFavoriteAnswerEvent,IUnFavoriteAnswerEvent
from plone.uuid.interfaces import IUUID

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
        '指定的用户是否在赞成队列里,true:已在队列中'
        return (userToken in self.approved )         
#         return self.approved.has_key(userToken)
    
    def voteavailabledisapproved(self,userToken):
        '指定的用户是否在反对队列里'        
        return (userToken in self.disapproved)        
#         return self.disapproved.has_key(userToken)
    
    def agree(self, userToken):
        """投赞成票,如果原来没投个赞成票（不在赞成队列中），直接加到赞成队列；
        并且看原来是否在反对队列中，从反对队列删除该用户"""

        if  not self.voteavailableapproved(userToken):
           self.approved.append(userToken)
           if  self.voteavailabledisapproved(userToken):
               self.disapproved.remove(userToken)
        else:
            raise KeyError("Ratings not available for %s" % userToken)
                  
    def disagree(self,userToken):
        if  not self.voteavailabledisapproved(userToken):
            self.disapproved.append(userToken)
            if  self.voteavailableapproved(userToken):
                self.approved.remove(userToken)
        else:
            raise KeyError("Ratings not available for %s" % userToken)
        

        
@grok.subscribe(IVotable, ILikeEvent)
def approve(obj, event):
    """approve the answer"""

    mp = getToolByName(obj,'portal_membership')
    userobject= mp.getAuthenticatedMember()
    username = userobject.getId()
    agreelist = list(userobject.getProperty('mylike'))

    uuid = IUUID(obj,None)
    if uuid == None:return    
    if not uuid in agreelist:
        agreelist.append(uuid)
        userobject.setProperties(mylike=agreelist)

    evlute = IVoting(obj)
    if not evlute.voteavailableapproved(username):
        evlute.agree(username)
        obj.voteNum = evlute.voteNum
        obj.totalNum = evlute.voteNum - len(evlute.disapproved)
        obj.reindexObject()
        
@grok.subscribe(IVotable, IUnLikeEvent)
def disapprove(obj, event):
    """approve the answer"""
    
    mp = getToolByName(obj,'portal_membership')
    userobject= mp.getAuthenticatedMember()
    username = userobject.getId()
    disagreelist = list(userobject.getProperty('myunlike'))

    uuid = IUUID(obj,None)
    if uuid == None:return       
    if not uuid in disagreelist:
        disagreelist.append(uuid)
        userobject.setProperties(myunlike=disagreelist)
    
    evlute = IVoting(obj)
    if not evlute.voteavailabledisapproved(username):
        evlute.disagree(username)
        obj.voteNum = evlute.voteNum
        obj.totalNum = evlute.voteNum - len(evlute.disapproved)
        obj.reindexObject()      

@grok.subscribe(IVotable, IObjectRemovedEvent)
def delVotableObj(obj,event):
    voteevlute = IVoting(obj)
    alist = voteevlute.approved
    dlist = voteevlute.disapproved
    if len(alist) == 0 and len(dlist) == 0:
        return
    
    pm = getToolByName(obj, 'portal_membership')
    if len(alist) != 0:
        for userid in alist:
            userobject=pm.getMemberById(userid)
            likelist = list(userobject.getProperty('mylike'))
            uuid = IUUID(obj,None)
            if uuid in likelist:
                likelist.remove(uuid)
                userobject.setProperties(mylike=likelist)

    if len(dlist) != 0:
        for userid in dlist:
            userobject=pm.getMemberById(userid)
            unlikelist = list(userobject.getProperty('myunlike'))
            uuid = IUUID(obj,None)
            if uuid in likelist:
                unlikelist.remove(uuid)
                userobject.setProperties(myunlike=unlikelist)

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
        