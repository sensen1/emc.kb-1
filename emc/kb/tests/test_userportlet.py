import unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import logout

from emc.kb.testing import INTEGRATION_TESTING

from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from Products.CMFCore.utils import getToolByName

from emc.kb.portlets import userportlet

class TestPortlet(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='emc.userportlet')
        self.assertEquals(portlet.addview, 'emc.userportlet')

    def testInterfaces(self):
        portlet = userportlet.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portal = self.layer['portal']
        
        portlet = getUtility(IPortletType, name='emc.userportlet')
        mapping = portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview()
        self.assertEquals(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], userportlet.Assignment))

    def testRenderer(self):
        context = self.layer['portal']
        request = self.layer['request']
        
        view = context.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=context)
        assignment = userportlet.Assignment()

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.assertTrue(isinstance(renderer, userportlet.Renderer))

class TestRenderer(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.topicfolder', 'tf')
        portal['tf'].invokeFactory('emc.kb.topic', 'tc')
        self.membership = getToolByName(portal, 'portal_membership')
        
        setRoles(portal, TEST_USER_ID, ('Member',))
    
    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        portal = self.layer['portal']
        
        context = context or portal
        request = request or self.layer['request']
        
        view = view or portal.restrictedTraverse('@@plone')
        
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=portal)
        assignment = assignment or userprotlet.Assignment()

        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
    
    def test_anonymous(self):
        portal = self.layer['portal']
        
        member = self.membership.getAuthenticatedMember()
        logout()
        r = self.renderer(context=portal, assignment=userportlet.Assignment())
        self.assertFalse(r.available)

    def test_single(self):
        portal = self.layer['portal']
        
        member = self.membership.getAuthenticatedMember()
        r = self.renderer(context=portal, assignment=userportlet.Assignment())
        self.assertTrue(r.available)
        homepage = self.membership.getHomeUrl()
        self.assertEqual(homepage,r.getHomepage())
        self.assertEqual(u"non signature",r.getSignature())