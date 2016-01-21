#-*- coding: UTF-8 -*-
from five import grok
from z3c.form import group, field
from datetime import datetime

from persistent.list import PersistentList
from plone.dexterity.interfaces import IDexterityContent

from zope.annotation.interfaces import IAnnotations
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.component import getUtility
from zope.component import getMultiAdapter
from Acquisition import aq_parent, aq_base, Implicit
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from zope.container.interfaces import INameChooser
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

from zope.i18n import translate
from zope.i18nmessageid import Message
from zope.interface import implements
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from zope.component import adapter
from zope.interface import implementer

from emc.kb.contents.topic import Itopic
from emc.kb.contents.question import Iquestion
from emc.kb.contents.topicfolder import Itopicfolder
from emc.kb.interfaces import IFollowedEvent
from emc.kb.interfaces import IUnFollowedEvent
from emc.kb.interfaces import IFollowing,IFollowable
from emc.kb.interfaces import ICountNumEvent
from emc.kb.interfaces import PROMOTIONS_PORTLET_COLUMN 
from emc.kb.portlets import relatedinformation
from plone.uuid.interfaces import IUUID



from emc.kb import _

FOLLOWED_KEY = 'emc.kb.follow'

@implementer(IFollowing)
@adapter(IDexterityContent)
class Follow(object):
#     grok.provides(IFollowing)
#     grok.context(Itopic)
    
    def __init__(self, context):
        self.context = context
        
        annotations = IAnnotations(context)
        if FOLLOWED_KEY not in annotations.keys():
            annotations[FOLLOWED_KEY] = PersistentList()          
        self.followed = annotations[FOLLOWED_KEY]
    
    #Statistics concern the number of
    @property
    def followerNum(self):
        total = len(self.followed)
        return total
        
    #Determine whether to be concerned about
    def available(self, userToken):
        return not(userToken in self.followed)
#         return self.followed.has_key(userToken) 
    #Editing statistics concern the number of               
    def addFollow(self, userToken):
        if self.available(userToken):
            self.followed.append(userToken)
        else:
            raise KeyError("The %s is concerned about" % userToken)
    #Editing statistics concern the number of               
    def delFollow(self, userToken):
        if not self.available(userToken):
            self.followed.remove(userToken)
        else:
            raise KeyError("The %s is not concerned about" % userToken)

@grok.subscribe(IFollowable,IFollowedEvent)
def SubscriberFollowed(obj,event):
    mp = getToolByName(obj,'portal_membership')
#     import pdb
#     pdb.set_trace()
    userobject = mp.getAuthenticatedMember()
    username = userobject.getId()
    fwqlist = list(userobject.getProperty('myfollowquestion'))
    fwtlist = list(userobject.getProperty('myfollowtopic'))
    fwlist = list(userobject.getProperty('myfollow'))

    
    uuid = IUUID(obj,None)
    if uuid == None:return
    if not (uuid in fwlist):
        fwlist.append(uuid)   
        userobject.setProperties(myfollow=fwlist)
        
    if Iquestion.providedBy(obj) and not(uuid in fwqlist):
        fwqlist.append(uuid)   
        userobject.setProperties(myfollowquestion=fwqlist)        
    if Itopic.providedBy(obj) and not(uuid in fwtlist):
        fwtlist.append(uuid)   
        userobject.setProperties(myfollowtopic=fwtlist)         
        
    evlute = IFollowing(obj)    
    if  evlute.available(username):
        evlute.addFollow(username)
        obj.followernum = evlute.followerNum
        obj.reindexObject() 
                
@grok.subscribe(IFollowable,IUnFollowedEvent)
def SubscriberUnFollowed(obj,event):
    mp = getToolByName(obj,'portal_membership')
    userobject = mp.getAuthenticatedMember()
    username = userobject.getId()
    fwqlist = list(userobject.getProperty('myfollowquestion'))
    fwtlist = list(userobject.getProperty('myfollowtopic'))    
    fwlist = list(userobject.getProperty('myfollow'))

    uuid = IUUID(obj,None)
    if uuid == None:return
    if  (uuid in fwlist):
        fwlist.remove(uuid)
        userobject.setProperties(myfollow=fwlist)
    if Iquestion.providedBy(obj) and (uuid in fwqlist):
        fwqlist.remove(uuid)   
        userobject.setProperties(myfollowquestion=fwqlist)        
    if Itopic.providedBy(obj) and (uuid in fwtlist):
        fwtlist.remove(uuid)   
        userobject.setProperties(myfollowtopic=fwtlist)       
    
    evlute = IFollowing(obj)    
    if not evlute.available(username):
        evlute.delFollow(username)
        obj.followernum = evlute.followerNum
        obj.reindexObject()  

@grok.subscribe(IFollowable, IObjectRemovedEvent)
def delFollow(obj,event):
    followevlute = IFollowing(obj)
    fwlist = followevlute.followed
    if len(fwlist) == 0:
        return
    
    pm = getToolByName(obj, 'portal_membership')
    for userid in fwlist:
        userobject=pm.getMemberById(userid)
        fwqlist = list(userobject.getProperty('myfollowquestion'))
        fwtlist = list(userobject.getProperty('myfollowtopic'))    
        fwlist = list(userobject.getProperty('myfollow'))
#         userfollow = list(userobject.getProperty('myfollow'))
        uuid = IUUID(obj,None)
        if uuid in fwlist:
            fwlist.remove(uuid)
            userobject.setProperties(myfollow=fwlist)
        if uuid in fwtlist:
            fwtlist.remove(uuid)
            userobject.setProperties(myfollowtopic=fwtlist)
        if uuid in fwqlist:
            fwqlist.remove(uuid)                                     
            userobject.setProperties(myfollowquestion=fwqlist)                

@grok.subscribe(Itopic,ICountNumEvent)
def CountNum(obj,event):
    num=obj.visitnum
    visitnum=num+1
    obj.visitnum=visitnum

@grok.subscribe(Itopic,IObjectAddedEvent)
def AddTopicPortlet(obj, event):
    """ this will add the relatedinformation portlet to topic automatically."""
    
    parent = aq_parent(obj)
    if Itopic.providedBy(parent):
        return
    
    # A portlet manager is akin to a column
    column = getUtility(IPortletManager, name=PROMOTIONS_PORTLET_COLUMN)
    
    # We multi-adapt the object and the column to an assignment mapping,
    # which acts like a dict where we can put portlet assignments
    manager = getMultiAdapter((obj, column,), IPortletAssignmentMapping)
    
    # We then create the assignment and put it in the assignment manager,
    # using the default name-chooser to pick a suitable name for us.
    assignment = relatedinformation.Assignment()
    chooser = INameChooser(manager)
    manager[chooser.chooseName(None, assignment)] = assignment
