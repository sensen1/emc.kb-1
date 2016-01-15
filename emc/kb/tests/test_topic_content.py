import unittest
from zope import event
from emc.kb.testing import INTEGRATION_TESTING
from emc.kb.testing import FUNCTIONAL_TESTING

from Products.CMFCore.utils import getToolByName

from zope.component import getUtility

from emc.kb.events import FollowedEvent
from emc.kb.events import UnFollowedEvent


from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

class TestContent(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    
    def test_topicfolder(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.topicfolder', 'topicfolder')
        self.assertTrue(portal['topicfolder'].id)
        
    def test_topic(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.topicfolder', 'topicfolder')
        portal['topicfolder'].invokeFactory('emc.kb.topic', 'topic',
                             name=u"topic",
                             discription=u"discription",

                             )
        self.assertEqual(portal['topicfolder']['topic'].name,u'topic')
        self.assertEqual(portal['topicfolder']['topic'].discription,u'discription')

        self.assertTrue(portal['topicfolder']['topic'].id)

    def test_questionfolder(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.questionfolder', 'questionfolder')
        self.assertTrue(portal['questionfolder'].id)
        
    def test_question(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.questionfolder', 'questionfolder')
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question',
                             discription=u"discription",
                             additional=u"additional",

                             )
        self.assertEqual(portal['questionfolder']['question'].discription,u'discription')
        self.assertEqual(portal['questionfolder']['question'].additional,u'additional')

        self.assertTrue(portal['questionfolder']['question'].id)
        
    def test_answer(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.questionfolder', 'questionfolder')
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question',
                             discription=u"discription",
                             additional=u"additional"

                             )
        portal['questionfolder']['question'].invokeFactory('emc.kb.answer', 'answer',
                             content=u"content of the answer"
                             )

        self.assertEqual(portal['questionfolder']['question']['answer'].content,u"content of the answer")

        self.assertTrue(portal['questionfolder']['question']['answer'].id)