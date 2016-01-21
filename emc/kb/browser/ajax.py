import json
from five import grok
from zope.interface import Interface
from Acquisition import aq_inner
from AccessControl import Unauthorized
from emc.kb.contents.question import Iquestion
from emc.kb.contents.topic import Itopic
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

from zope import event
from emc.kb.events import FollowedEvent
from emc.kb.events import UnFollowedEvent
from emc.kb.events import LikeEvent,UnLikeEvent
from plone.uuid.interfaces import IUUID

class AjaxModify(grok.View):
    """AJAX action for Modifying title & description.
    """
    
    grok.context(Interface)
    grok.name('ajax_modify')
    grok.require('zope2.View')
        
    def render(self):
        context = aq_inner(self.context)
#         authenticator=getMultiAdapter((context, self.request), name=u"authenticator")
#         if not authenticator.verify():
#             raise Unauthorized        
        data = self.request.form

        if data['type'] == "1":
            # modify title            
            context.setTitle(data['txtvalue'])
        else:
            # modify description
            context.setDescription(data['txtvalue'])
        callback = 1
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(callback)
    

class Like(grok.View):
    """AJAX action: like a object.
    """
    
    grok.context(Interface)
    grok.name('like')
    grok.require('zope2.View')
    
    def render(self):
        
        mp = getToolByName(self.context,'portal_membership')
        userobject= mp.getAuthenticatedMember()
        agreelist = list(userobject.getProperty('mylike'))
        unagreelist = list(userobject.getProperty('myunlike'))
        uuid = IUUID(self.context,None)
        if  uuid in agreelist or uuid in agreelist : return json.dumps(0)       
        
        try:
            event.notify(LikeEvent(self.context))
            data = 1
        except:
            data = 0
        return json.dumps(data)        
    
class UnLike(grok.View):
    """AJAX action: follow a question.
    """
    
    grok.context(Interface)
    grok.name('unlike')
    grok.require('zope2.View')
    
    def render(self):
        mp = getToolByName(self.context,'portal_membership')
        userobject= mp.getAuthenticatedMember()
        agreelist = list(userobject.getProperty('mylike'))
        unagreelist = list(userobject.getProperty('myunlike'))
        uuid = IUUID(self.context,None)
        if  uuid in agreelist or uuid in agreelist : return json.dumps(0)         
        try:
            event.notify(UnLikeEvent(self.context))
            data = 1
        except:
            data = 0
        return json.dumps(data)

class Follow(grok.View):
    """AJAX action: follow a question.
    """
    
    grok.context(Interface)
    grok.name('follow')
    grok.require('zope2.View')
    
    def render(self):
        try:
            event.notify(FollowedEvent(self.context))
            data = 1
        except:
            data = 0
        return json.dumps(data)        
    
class UnFollow(grok.View):
    """AJAX action: follow a question.
    """
    
    grok.context(Interface)
    grok.name('unfollow')
    grok.require('zope2.View')
    
    def render(self):
        try:
            event.notify(UnFollowedEvent(self.context))
            data = 1
        except:
            data = 0
        return json.dumps(data)      


class AjaxFollow(grok.View):
    """AJAX action: follow a question.
    """
    
    grok.context(INavigationRoot)
    grok.name('ajax-follow')
    grok.require('zope2.View')
        
    def render(self):
        data = self.request.form
        questionid = data['questionid'].replace('_','.')
        catalog = getToolByName(self.context, 'portal_catalog')
        questionobject = catalog({'object_provides': Iquestion.__identifier__,
                                  'id': questionid,
                                  'sort_on': 'sortable_title'})
        event.notify(FollowedEvent(questionobject[0].getObject()))

class AjaxUnfollow(grok.View):
    """AJAX action: unfollow a question.
    """
    
    grok.context(INavigationRoot)
    grok.name('ajax-unfollow')
    grok.require('zope2.View')
        
    def render(self):
        data = self.request.form
        questionid = data['questionid'].replace('_','.')
        catalog = getToolByName(self.context, 'portal_catalog')
        questionobject = catalog({'object_provides': Iquestion.__identifier__,
                                  'id': questionid,
                                  'sort_on': 'sortable_title'})
        event.notify(UnFollowedEvent(questionobject[0].getObject()))

class AjaxFollowtopic(grok.View):
    """AJAX action: follow a topic.
    """
    
    grok.context(INavigationRoot)
    grok.name('ajax-followtopic')
    grok.require('zope2.View')
    
    def render(self):
        data = self.request.form
        topicid = data['topicid']
        catalog = getToolByName(self.context, 'portal_catalog')
        topicobject = catalog({'object_provides': Itopic.__identifier__,
                               'id': topicid,
                               'sort_on': 'sortable_title'})
        event.notify(FollowedEvent(topicobject[0].getObject()))

class AjaxUnfollowtopic(grok.View):
    """AJAX action: unfollow a topic.
    """
    
    grok.context(INavigationRoot)
    grok.name('ajax-unfollowtopic')
    grok.require('zope2.View')
    
    def render(self):
        data = self.request.form
        topicid = data['topicid']
        catalog = getToolByName(self.context, 'portal_catalog')
        topicobject = catalog({'object_provides': Itopic.__identifier__,
                               'id': topicid,
                               'sort_on': 'sortable_title'})
        event.notify(UnFollowedEvent(topicobject[0].getObject()))

class AjaxFollowtq(grok.View):
    """AJAX action: follow a question from topic page.
    """
    
    grok.context(Itopic)
    grok.name('ajax-followtq')
    grok.require('zope2.View')
        
    def render(self):
        data = self.request.form
        questionid = data['questionid'].replace('_','.')
        catalog = getToolByName(self.context, 'portal_catalog')
        questionobject = catalog({'object_provides': Iquestion.__identifier__,
                                  'id': questionid,
                                  'sort_on': 'sortable_title'})
        event.notify(FollowedEvent(questionobject[0].getObject()))

class AjaxUnfollowtq(grok.View):
    """AJAX action: unfollow a question from topic page.
    """
    
    grok.context(Itopic)
    grok.name('ajax-unfollowtq')
    grok.require('zope2.View')
        
    def render(self):
        data = self.request.form
        questionid = data['questionid'].replace('_','.')
        catalog = getToolByName(self.context, 'portal_catalog')
        questionobject = catalog({'object_provides': Iquestion.__identifier__,
                                  'id': questionid,
                                  'sort_on': 'sortable_title'})
        event.notify(UnFollowedEvent(questionobject[0].getObject()))