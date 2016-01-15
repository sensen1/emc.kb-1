"""Test the plone.app.discussion catalog indexes
"""
import unittest
import transaction
from zope import event

from datetime import datetime

from zope.component import createObject
from zope.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from emc.kb.testing import INTEGRATION_TESTING


from emc.kb.events import FollowedEvent
from emc.kb.events import UnFollowedEvent
from emc.kb.events import LikeEvent
from emc.kb.events import UnLikeEvent
from emc.kb.contents.answer import Ianswer

from emc.kb.contents import answer as catalog
from plone.indexer.delegate import DelegatingIndexerFactory

class CatalogSetupTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.portal.invokeFactory(id='topicfolder',
                  title='topic folder1',
                  type_name='emc.kb.topicfolder')

        self.portal['topicfolder'].invokeFactory('emc.kb.topic', 'topic',
                             name=u"topic",
                             discription=u"discription",

                             )
        self.portal.invokeFactory('emc.kb.questionfolder', 'questionfolder')
        self.portal['questionfolder'].invokeFactory('emc.kb.question', 'question',
                             discription=u"discription",
                             additional=u"additional",

                             )
                # Create a conversation.
        self.portal['questionfolder']['question'].invokeFactory('emc.kb.answer', 'answer1',
                             content=u"content of the answer"
                             )
        self.portal['questionfolder']['question'].invokeFactory('emc.kb.answer', 'answer2',
                             content=u"content of the answer2"
                             )        
    
    def test_catalog_installed(self):
        self.assertTrue('voteNum' in
                        self.portal.portal_catalog.indexes())
        self.assertTrue('name' in
                        self.portal.portal_catalog.indexes())
        self.assertTrue('content' in
                        self.portal.portal_catalog.schema())
    def test_conversation_total_comments(self):
        self.assertTrue(isinstance(catalog.voteNum,
                                DelegatingIndexerFactory))
        answer1 = self.portal['questionfolder']['question']['answer1']
        self.assertEqual(catalog.voteNum(answer1)(), 0)
        event.notify(LikeEvent(answer1))
        self.assertEqual(catalog.voteNum(answer1)(), 1)
        
    def test_catalogsearch(self):   
        catalog2 = getToolByName(self.portal, 'portal_catalog')     

        results2 = list(catalog2({'voteNum': 0}))
        self.assertEqual(len(results2), 2)
        answer1 = self.portal['questionfolder']['question']['answer1']        
        event.notify(LikeEvent(answer1))        
        results2 = list(catalog2({'object_provides': Ianswer.__identifier__,
                                  'sort_on': 'voteNum',
                                  'sort_order': 'reverse'}))        
        self.assertEqual(len(results2), 2)
#        import pdb
#        pdb.set_trace()
        self.assertEqual(results2[0].id,'answer1')
        results2 = list(catalog2({'object_provides': Ianswer.__identifier__,
                                  'sort_on': 'voteNum',
                                  'sort_order': 'forward'}))
#        import pdb
#        pdb.set_trace()
        self.assertEqual(results2[0].id,'answer2')


                   
def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
