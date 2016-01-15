from zope import event
import unittest
from plone.testing.z2 import Browser

from emc.kb.testing import INTEGRATION_TESTING
from emc.kb.testing import FUNCTIONAL_TESTING

from Products.CMFCore.utils import getToolByName

from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import setRoles

class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    
    def setUp(self):
        from emc.memberArea.events import FavoriteEvent
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.topicfolder', 'topicfolder')
        portal['topicfolder'].invokeFactory('emc.kb.topic', 'topic1',
                             name=u"topic",
                             description=u"description",
    
                             )
        portal['topicfolder'].invokeFactory('emc.kb.topic', 'topic2',
                             name=u"topic",
                             description=u"description",

                             )
        portal.invokeFactory('emc.kb.questionfolder', 'questionfolder')
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question',
                             description=u"description",
                             additional=u"additional",

                             )
        portal['questionfolder']['question'].invokeFactory('emc.kb.answer', 'answer1',

                             content=u"content of the answer"

                             )
        portal['questionfolder']['question'].invokeFactory('emc.kb.answer', 'answer2',

                             content=u"content of the answer"
                             )
        portal['questionfolder']['question'].invokeFactory('emc.kb.answer', 'answer3',

                             content=u"content of the answer"

                             )
        intids = getUtility(IIntIds)
        q1=portal['questionfolder']['question']
        t1=portal['topicfolder']['topic1']
        t2=portal['topicfolder']['topic2']
        q1.affiliatedtopics = [RelationValue(intids.getId(t1)),RelationValue(intids.getId(t2)),]
        
        file1=portal['questionfolder']['question']['answer1']
        file2=portal['questionfolder']['question']['answer2']
        file3=portal['questionfolder']['question']['answer3']
        
        event.notify(FavoriteEvent(file1))
        event.notify(FavoriteEvent(file2))
        event.notify(FavoriteEvent(file3))
        
        import transaction; transaction.commit()
        
    def test_collection_view(self):
        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        browser.handleErrors = False
        pp_url = portal.absolute_url()
        # Open form.
        browser.open("%s/@@myfavoritefolder" % pp_url)
        
        self.assertTrue(TEST_USER_ID in browser.contents)
        self.assertTrue("question" in browser.contents)
        self.assertTrue("answer1" in browser.contents)
        self.assertTrue("answer2" in browser.contents)
        self.assertTrue("answer3" in browser.contents)
        self.assertTrue("topic1" in browser.contents)
        self.assertTrue("topic2" in browser.contents)
