from plone.testing.z2 import Browser
 
import unittest
from zope import event
from emc.kb.testing import INTEGRATION_TESTING
from emc.kb.testing import FUNCTIONAL_TESTING

from Products.CMFCore.utils import getToolByName

from zope.component import getUtility

from emc.kb.events import FollowedEvent
from emc.kb.events import UnFollowedEvent
from emc.kb.events import FollowedEvent
from emc.kb.events import UnFollowedEvent

from plone.app.testing import TEST_USER_ID,login,TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import setRoles

class TestIfollowed(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.questionfolder', 'questionfolder')
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question1',
                                 title=u"test",
                                 date=u"date"
                                )
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question2',
                                 title=u"testtwo",
                                 date=u"date"
                                )
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question3',
                                 title=u"testthree",
                                 date=u"date"
                                )
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question4',
                                 title=u"testfour",
                                 date=u"date"
                                )
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question5',
                                 title=u"testfive",
                                 date=u"date"
                                )
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question6',
                                 title=u"testsix",
                                 date=u"date"
                                )
        portal['questionfolder']['question1'].invokeFactory('emc.kb.answer', 'answer1',
                                 title=u"testtest",
                                 date=u"date"
                                )
        
        ques1 = portal['questionfolder']['question1']
        ques2 = portal['questionfolder']['question2']
        ques3 = portal['questionfolder']['question3']
        ques4 = portal['questionfolder']['question4']
        ques5 = portal['questionfolder']['question5']
        ques6 = portal['questionfolder']['question6']
        event.notify(FollowedEvent(ques1))
        event.notify(FollowedEvent(ques2))
        event.notify(FollowedEvent(ques3))
        event.notify(FollowedEvent(ques4))
        event.notify(FollowedEvent(ques5))
        event.notify(FollowedEvent(ques6))
        
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.topicfolder', 'topicfolder')
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal['topicfolder'].invokeFactory('emc.kb.topic', 'topic1',
                                 title=u"topicone",
                                 description="testtopic1",
                                 date=u"date"
                                )
        portal['topicfolder'].invokeFactory('emc.kb.topic', 'topic2',
                                 title=u"testtwo",
                                 description="testtopic2",
                                 date=u"date"
                                )
        portal['topicfolder'].invokeFactory('emc.kb.topic', 'topic3',
                                 title=u"topicthree",
                                 description="testtopic3",
                                 date=u"date"
                                )
        portal['topicfolder'].invokeFactory('emc.kb.topic', 'topic4',
                                 title=u"topicfour",
                                 description="testtopic4",
                                 date=u"date"
                                )
        portal['topicfolder'].invokeFactory('emc.kb.topic', 'topic5',
                                 title=u"topicfive",
                                 description="testtopic5",
                                 date=u"date"
                                )
        portal['topicfolder'].invokeFactory('emc.kb.topic', 'topic6',
                                 title=u"topicsix",
                                 description="testtopic6",
                                 date=u"date"
                                 )
        topic1 = portal['topicfolder']['topic1']
        topic2 = portal['topicfolder']['topic2']
        topic3 = portal['topicfolder']['topic3']
        topic4 = portal['topicfolder']['topic4']
        topic5 = portal['topicfolder']['topic5']
        topic6 = portal['topicfolder']['topic6']
        event.notify(FollowedEvent(topic1))
        event.notify(FollowedEvent(topic2))
        event.notify(FollowedEvent(topic3))
        event.notify(FollowedEvent(topic4))
        event.notify(FollowedEvent(topic5))
        event.notify(FollowedEvent(topic6))
        
    
    def testquestionsIfollowed(self):
        app = self.layer['app']        
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
        
        que = portal.absolute_url() + '/@@questionfollowed'
        browser.open(que)
        
        open('/tmp/test.html','w').write(browser.contents)
        
        self.assertTrue("testsix" in browser.contents)
        self.assertTrue("unfollow this question" in browser.contents)
        self.assertTrue("Next" in browser.contents)
        
        top = portal.absolute_url() + '/@@topicfollowed'
        browser.open(top)
        
        open('/tmp/test.html','w').write(browser.contents)
        
        self.assertTrue("topicsix" in browser.contents)
        self.assertTrue("testtopic6" in browser.contents)
#        self.assertTrue("unfollow this topic" in browser.contents)
        self.assertTrue("Next" in browser.contents)