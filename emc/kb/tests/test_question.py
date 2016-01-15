from plone.testing.z2 import Browser

 
import unittest
from zope import event
from emc.kb.testing import INTEGRATION_TESTING
from emc.kb.testing import FUNCTIONAL_TESTING

from Products.CMFCore.utils import getToolByName

from zope.component import getUtility

from emc.kb.events import FollowedEvent
from emc.kb.events import UnFollowedEvent
from emc.kb.events import LikeEvent
from emc.kb.events import UnLikeEvent

from plone.app.testing import TEST_USER_ID,login,TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import setRoles

class Testquestion(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.questionfolder', 'questionfolder')
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question',
                                 title=u"question",
                                 description=u"question description",
                                 )
        portal['questionfolder']['question'].invokeFactory('emc.kb.answer', 'answer1',
                                 content=u"answerone",
                                )
        portal['questionfolder']['question'].invokeFactory('emc.kb.answer', 'answer2',
                                 content=u"answertwo",
                                )
        portal['questionfolder']['question'].invokeFactory('emc.kb.answer', 'answer3',
                                 content=u"answerthree",
                                )
        ans = portal['questionfolder']['question']['answer2']
        event.notify(LikeEvent(ans))
        
    def testquestion(self):
        app = self.layer['app']        
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
        
        ques = portal['questionfolder']['question'].absolute_url()
        browser.open(ques)
        
        browser.getControl(name='form.submit').click()
        
        open('/tmp/test.html','w').write(browser.contents)
        
        self.assertTrue("question" in browser.contents)
        self.assertTrue("question description" in browser.contents)
        
        self.assertTrue("4" in browser.contents)

        self.assertTrue("test_user_1_" in browser.contents)
        self.assertTrue("defaultUser.png" in browser.contents)
        
        self.assertTrue("answerone" in browser.contents)
        
        self.assertTrue("answertwo" in browser.contents)
        self.assertTrue("answerthree" in browser.contents)
        self.assertTrue("add an answer" in browser.contents)