from plone.testing.z2 import Browser
 
import  unittest
from zope import event
from emc.kb.testing import INTEGRATION_TESTING
from emc.kb.testing import FUNCTIONAL_TESTING

from Products.CMFCore.utils import getToolByName

from zope.component import getUtility

from emc.kb.events import FollowedEvent
from emc.kb.events import UnFollowedEvent

from plone.app.testing import TEST_USER_ID,login,TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import setRoles

class TestMyQA(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING

    def setUp(self):  
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.questionfolder', 'questionfolder')
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question1',
                             title=u"soft kitty",
                             date=u"date"
                             )
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question2',
                             title=u"monst kitty",
                             date=u"date"
                             )
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question3',
                             title=u"monst kitty",
                             date=u"date"
                             )
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question4',
                             title=u"monst kitty",
                             date=u"date"
                             )
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question5',
                             title=u"monst kitty",
                             date=u"date"
                             )
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question6',
                             title=u"monst kitty",
                             date=u"date"
                             )
        portal['questionfolder']['question1'].invokeFactory('emc.kb.answer', 'answer11',
                             content=u"cup boll"
                             )
        portal['questionfolder']['question2'].invokeFactory('emc.kb.answer', 'answer21',
                             content=u"fast ball"
                             )
        portal['questionfolder']['question3'].invokeFactory('emc.kb.answer', 'answer31',
                             content=u"cute girl"
                             )
        portal['questionfolder']['question4'].invokeFactory('emc.kb.answer', 'answer41',
                             content=u"grass"
                             )
        portal['questionfolder']['question5'].invokeFactory('emc.kb.answer', 'answer51',
                             content=u"sunshine",
                             )
        
#        ques1 = portal['questionfolder']['question1']
#        event.notify(UnFollowedEvent(ques))
        import transaction
        transaction.commit()
              
    def test_myquestion(self):
        app = self.layer['app']        
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
#        import pdb
#        pdb.set_trace()
        setRoles(portal, TEST_USER_ID, ('Manager',))
        m9 =portal.absolute_url()+'/@@myquestion'
#        import pdb
#        pdb.set_trace() 
#        browser.open(portal.absolute_url())
#        browser.open("%s/@@dam-report" % portal.absolute_url())
        browser.open( m9)
        
        open('/tmp/test.html','w').write(browser.contents)

        self.assertTrue("1" in browser.contents)
        self.assertTrue("monst" in browser.contents)
        self.assertTrue("Next" in browser.contents)

    def test_myanswer(self):
        app = self.layer['app']        
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
#        import pdb
#        pdb.set_trace()
        setRoles(portal, TEST_USER_ID, ('Manager',))
        m9 =portal.absolute_url()+'/@@myanswer'
#        import pdb
#        pdb.set_trace() 
#        browser.open(portal.absolute_url())
#        browser.open("%s/@@dam-report" % portal.absolute_url())
        browser.open( m9)
        
        open('/tmp/test.html','w').write(browser.contents)

#        self.assertTrue("3" in browser.contents)
        self.assertTrue("monst" in browser.contents)
        self.assertTrue("fast" in browser.contents)
        self.assertTrue("Next" in browser.contents)

class TestRendering(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING