#-*- coding: UTF-8 -*-
import json
from five import grok
from Acquisition import aq_parent
from datetime import datetime

from emc.kb.contents.answer import Ianswer
from emc.kb.contents.mentionme import Imentionme
from emc.kb.interfaces import IFollowing
from emc.kb.interfaces import ILikeEvent
from emc.kb.contents.mentionmefolder import Imentionmefolder
from emc.kb.interfaces import ICreatedMentionwoFolderEvent

from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer
from zope.lifecycleevent.interfaces import IObjectAddedEvent 

@grok.subscribe(Ianswer, IObjectAddedEvent)
def mentionmeanswer(obj,event):
    """我的提问有新答案"""
    mp = getToolByName(obj,'portal_membership')
    userobject = mp.getAuthenticatedMember()
    
    questionobject = aq_parent(obj)
    votename = questionobject.Creator()
    
    catalog = getToolByName(obj, 'portal_catalog')
    
    brain = catalog({'object_provides':  Imentionmefolder.__identifier__,
             'Creator': votename,
             'sort_on': 'sortable_title'})
    if not brain:
        return
    folder = brain[0].getObject()
    if not folder:
        return
    date = datetime.now()
    id = str(date.year)+str(date.month)+str(date.day)+str(date.hour)+str(date.minute)+str(date.second)
    item = createContentInContainer(folder,"emc.kb.mentionme",checkConstraints=False,id=id)
    item.title = ''
    item.answerid = obj.getId()
    item.answeruser = userobject.getId()
    item.discription = {"我的提问有新答案":1,"我关注的问题有新答案":2,"有人赞同我的答案":3}
    item.state = 1
    item.questionid = questionobject.id
    item.reindexObject()
        
@grok.subscribe(Ianswer, IObjectAddedEvent)
def followquestionanswer(obj,event):
    """我关注的问题有新答案"""
    mp = getToolByName(obj,'portal_membership')
    userobject = mp.getAuthenticatedMember()
    
    catalog = getToolByName(obj, 'portal_catalog')
    
    questionobject = aq_parent(obj)
    """问题作者"""
    votename = questionobject.Creator()
    evlutelist = IFollowing(questionobject).followed
    if len(evlutelist) == 0:
        return 
    for evlute in evlutelist:
        """不想要给问题作者添加该关注记录"""
        if evlute == votename:
            break
        brain = catalog({'object_provides':  Imentionwofolder.__identifier__,
                'Creator': evlute,
             'sort_on': 'sortable_title'})
        if not brain:
            break
        folder = brain[0].getObject()
        if not folder:
            break
        date = datetime.now()
        id = str(date.year)+str(date.month)+str(date.day)+str(date.hour)+str(date.minute)+str(date.second)
        item = createContentInContainer(folder,"emc.kb.mentionme",checkConstraints=False,id=id)
        item.title = ''
        item.answerid = obj.getId()
        item.answeruser = userobject.getId()
        item.discription = {"我的提问有新答案":1,"我关注的问题有新答案":2,"有人赞同我的答案":3}
        item.state = 2
        item.questionid = questionobject.id
        item.reindexObject()
        
@grok.subscribe(Ianswer, ILikeEvent)
def FavoriteAnswer(obj,event):
    """有人赞同我的答案"""
    questionobject = aq_parent(obj)
    mp = getToolByName(obj,'portal_membership')
    userobject1 = mp.getMemberById(obj.Creator())
    username = userobject1.getId()
    """赞同用户"""
    userobject2 = mp.getAuthenticatedMember()
    
    catalog = getToolByName(obj, 'portal_catalog')
    brain = catalog({'object_provides':  Imentionmefolder.__identifier__,
             'Creator': username,
             'sort_on': 'sortable_title'})
    if not brain:
            return
    folder = brain[0].getObject()
    if not folder:
        return
    date = datetime.now()
    id = str(date.year)+str(date.month)+str(date.day)+str(date.hour)+str(date.minute)+str(date.second)
    item = createContentInContainer(folder,"emc.kb.mentionme",checkConstraints=False,id=id)
    item.title = ''
    item.answerid = obj.getId()
    item.answeruser = userobject2.getId()
    item.discription = {"我的提问有新答案":1,"我关注的问题有新答案":2,"有人赞同我的答案":3}
    item.state = 3
    item.questionid = questionobject.id
    item.reindexObject()