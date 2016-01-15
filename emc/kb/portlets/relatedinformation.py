from StringIO import StringIO
from time import localtime
from zope import event,schema

from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider

from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from zope.component import getMultiAdapter

from zope.formlib import form
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_inner

from emc.kb.events import CountNumEvent

from emc.kb import  _
from plone.app.portlets import cache
from plone.app.portlets.portlets import base
from plone.behavior.interfaces import IBehaviorAssignable

class IRelatedInformation(IPortletDataProvider):
    """
    """
    
class Assignment(base.Assignment):
    implements(IRelatedInformation) 
    
    @property
    def title(self):
        return _(u"Related Information")
    
class Renderer(base.Renderer):
    render = ViewPageTemplateFile('relatedinformation.pt')

#    @property
#    def available(self):
#        """pass"""
#        import pdb
#        pdb.set_trace()
#        context=self.context        
#        assignable = IBehaviorAssignable(context)
#        for behavior in assignable.enumerateBehaviors():
#            behavior_schema = behavior.interface
#            adapted = behavior_schema(context)
#            re = bool(Ipageview==behavior_schema)
#            if  re : return True
                  
    
    def visitnum(self):
        """pass"""
        event.notify(CountNumEvent(self.context))
        num = self.context.visitnum 
        return num
    
    def followednum(self):
        """"""
        context=self.context
        followednum=context.followernum
        return followednum
        
class AddForm(base.NullAddForm):
    
    def create(self):
        return Assignment()
        
