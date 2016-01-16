#-*- coding: UTF-8 -*-
import json
from five import grok
from Acquisition import aq_parent
from datetime import datetime
from DateTime import DateTime

from emc.kb.contents.feed import Ifeed
from emc.kb.contents.answer import Ianswer
from emc.kb.contents.question import Iquestion
from emc.kb.contents.feedsfolder import Ifeedsfolder
from emc.kb.interfaces import IFollowing,IFollowing
from emc.kb.interfaces import ICreatedMentionwoFolderEvent
from emc.memberArea.interfaces import IMemberAreaCreatedEvent

from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer
from Products.PluggableAuthService.interfaces.authservice import IPropertiedUser

from zope import event
from zope import component
from zope.intid import IntIds
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zc.relation.interfaces import ICatalog
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from z3c.relationfield import RelationValue,RelationCatalog

    
@grok.subscribe(Ianswer, IObjectAddedEvent)
def feedquestionanswer(obj,event):
    """关注问题有新答案"""
    catalog = getToolByName(obj, 'portal_catalog')
    questionobject = aq_parent(obj)
    questionlist = IFollowing(questionobject).followed
    if len(questionlist) == 0:
        return
    
    for question in questionlist:
        brain = catalog({'object_provides':  Ifeedsfolder.__identifier__,
             'Creator': question,
             'sort_on': 'sortable_title'})
        if not brain:
            break
        folder = brain[0].getObject()
        if not folder:
            break
       
        id = questionobject.getId()
        feed = catalog({'object_provides':  Ifeed.__identifier__,
                 'id': id,
                 'path': dict(query='/'.join(folder.getPhysicalPath()),
                              depth=1),        
             'sort_on': 'sortable_title'})
        """如果存在当前记录，重置修改时间,否则新建"""
        if len(feed) > 0:
            feed[0].getObject().type = 3
            feed[0].getObject().setModificationDate(DateTime())
        else:
            item = createContentInContainer(folder,"emc.kb.feed",checkConstraints=False,id=id)
            item.type = 3
            
@grok.subscribe(Ianswer, IObjectAddedEvent)
def feedtopicanswer(obj,event):
    """关注话题中问题有答案"""
    questionobject = aq_parent(obj)
    intids = getUtility(IIntIds)  
    intid = intids.getId(questionobject)
    catalog = component.getUtility(ICatalog) 
    qlist = sorted(catalog.findRelations({'from_id': intid}))
    if len(qlist) == 0: return
    for q in qlist:
        topicobject = q.to_object
        topiclist = IFollowing(topicobject).followed
        """计算关联回答的topic分数"""
        topicobject.topicscore = topicobject.topicscore + 0.3
        topicobject.reindexObject()
        
        catalog = getToolByName(obj, 'portal_catalog')
        for topic in topiclist:
            brain = catalog({'object_provides':  Ifeedsfolder.__identifier__,
                 'Creator': topic,
                 'sort_on': 'sortable_title'})
            if not brain:
                break
            folder = brain[0].getObject()
            if not folder:
                break
           
            id = questionobject.getId()
            feed = catalog({'object_provides':  Ifeed.__identifier__,
                     'id': id,
                     'path': dict(query='/'.join(folder.getPhysicalPath()),
                                  depth=1),        
                 'sort_on': 'sortable_title'})
            """如果存在当前记录，重置修改时间,否则新建"""
            if len(feed) > 0:
                feed[0].getObject().type = 2
                feed[0].getObject().setModificationDate(DateTime())
            else:
                item = createContentInContainer(folder,"emc.kb.feed",checkConstraints=False,id=id)
                item.type = 2
        
@grok.subscribe(Iquestion, IObjectAddedEvent)
def feedtopciquestion(obj,event):
    """关注话题有问题"""
    intids = getUtility(IIntIds)
    intid = intids.getId(obj)
    catalog = component.getUtility(ICatalog) 
    qtlist = sorted(catalog.findRelations({'from_id': intid}))
    if len(qtlist) == 0: return 
    
    for q in qtlist:
        topiclist = IFollowing(q.to_object).followed
        catalog = getToolByName(obj, 'portal_catalog')
        for topic in topiclist:
            brain = catalog({'object_provides':  Ifeedsfolder.__identifier__,
                 'Creator': topic,
                 'sort_on': 'sortable_title'})
            if not brain:
                break
            folder = brain[0].getObject()
            if not folder:
                break
           
            id = obj.getId()
            feed = catalog({'object_provides':  Ifeed.__identifier__,
                     'id': id,
                     'path': dict(query='/'.join(folder.getPhysicalPath()),
                                  depth=1),        
                    'sort_on': 'sortable_title'})
            """如果存在当前记录，重置修改时间,否则新建"""
            if len(feed) > 0:
                feed[0].getObject().type = 1
                feed[0].getObject().setModificationDate(DateTime())
            else:
                item = createContentInContainer(folder,"emc.kb.feed",checkConstraints=False,id=id)
                item.type = 1