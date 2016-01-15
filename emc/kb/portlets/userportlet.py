from StringIO import StringIO
from time import localtime

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

from emc.kb import _
from plone.app.portlets import cache
from plone.app.portlets.portlets import base

from emc.kb.contents.questionfolder import Iquestionfolder

class IuserportletProvider(IPortletDataProvider):
    """
    """
    
class Assignment(base.Assignment):
    implements(IuserportletProvider) 
    
    @property
    def title(self):
        return _(u"User portlet")

class Renderer(base.Renderer):
    render = ViewPageTemplateFile('userportlet.pt')
    @property
    def membership(self):
        context = aq_inner(self.context)
        return getToolByName(context,'portal_membership')
    
    @property
    def anonymous(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        return portal_state.anonymous() 
    
    @property    
    def available(self):
        return not self.anonymous
    
    def getPortrait(self):
        portrait = self.membership.getPersonalPortrait()
        return portrait
    
    def getUsername(self):
        member = self.membership.getAuthenticatedMember()
        username = member.getProperty('fullname')
        return username
    
    def getPosition(self):
        member = self.membership.getAuthenticatedMember()
        position = member.getProperty('position')
        if len(position):
            return position
        return _(u"not fill position")
    
    def getDepartment(self):
        member = self.membership.getAuthenticatedMember()
        department = member.getProperty('department')
        if len(department):
            return department        
        return _(u"not fill department")
    
    def getSignature(self):
        member = self.membership.getAuthenticatedMember()
        department = member.getProperty('description')

        if len(department):
            return department        
        return _(u"non signature")
        
    def getHomepage(self):
        homepage = self.membership.getHomeUrl()
        return homepage
    
    def getQuestionFolder(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, 'portal_catalog')
        questionfolder = pc({'object_provides': Iquestionfolder.__identifier__})
        if len(questionfolder) > 0:
            path = questionfolder[0].getURL()
        else:
            path = ''
        return path
    
class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
