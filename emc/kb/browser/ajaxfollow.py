import json
from five import grok

from Acquisition import aq_inner
from emc.kb.contents.question import Iquestion
from emc.kb.contents.topic import Itopic
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.utils import getToolByName

from zope import event
from emc.kb.events import FollowedEvent
from emc.kb.events import UnFollowedEvent
from emc.kb.events import FollowedEvent
from emc.kb.events import UnFollowedEvent

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