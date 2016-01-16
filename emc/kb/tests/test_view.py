from plone.testing.z2 import Browser

import unittest
from zope import event
from emc.kb.testing import INTEGRATION_TESTING
from emc.kb.testing import FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID,login,TEST_USER_NAME, TEST_USER_PASSWORD

from z3c.relationfield import RelationCatalog
from zc.relation.interfaces import ICatalog
from zope import component
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue

from emc.kb.events import FollowedEvent
from emc.kb.events import UnFollowedEvent
from emc.kb.events import FollowedEvent
from emc.kb.events import UnFollowedEvent
from emc.kb.events import FavoriteAnswerEvent
from emc.kb.events import UnFavoriteAnswerEvent
from emc.kb.events import LikeEvent
from emc.kb.events import UnLikeEvent

from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent import ObjectModifiedEvent


from emc.kb.contents.question import Iquestion
from emc.kb.contents.topic import Itopic
from emc.kb.contents.answer import Ianswer
from emc.kb.contents.feed import Ifeed

from emc.kb.interfaces import IFollowing
# from emc.kb.interfaces import IAnswerEvaluate
from emc.kb.interfaces import IFollowing

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles,login,logout

class TestView(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    def setUp(self):
        portal = self.layer['portal']
        self.catalog = getToolByName(portal, 'portal_catalog')  
        setRoles(portal, TEST_USER_ID, ('Manager',))
        intids = getUtility(IIntIds) 
#        portal.invokeFactory('emc.kb.mentionwofolder', 'mentionwofolder')
#        portal.invokeFactory('emc.kb.feedsfolder', 'feedsfolder')
        portal.invokeFactory('emc.kb.questionfolder', 'questionfolder')
        portal.invokeFactory('emc.kb.topicfolder', 'topicfolder',title="topicfolder title")
        portal['topicfolder'].invokeFactory("emc.kb.topic",'topic1',
                                            title=u"topicone",
                                            description=u"descriptionone"
                                            )
        portal['topicfolder'].invokeFactory("emc.kb.topic",'topic2',
                                            title=u"topictwo",
                                            description=u"descriptiontwo"
                                            )        
        self.t1 = portal['topicfolder']['topic1']
        self.t2 = portal['topicfolder']['topic2']
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question1',
                                            title='questionone',
                                            affiliatedtopics=[RelationValue(intids.getId(self.t1))],
                                            )
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question2',
                                            title='questiontwo',
                                            affiliatedtopics=[RelationValue(intids.getId(self.t1))],
                                            )
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question3',
                                            title='questionthree',
                                            affiliatedtopics=[RelationValue(intids.getId(self.t1))],
                                            )
        self.q1 = portal['questionfolder']['question1']
        self.q2 = portal['questionfolder']['question2'] 
        self.q3 = portal['questionfolder']['question3']
        portal['questionfolder']['question1'].invokeFactory('emc.kb.answer', 'answer1',
                                                            content=u"answerone",
                                                            title=u"answerone"
                                                            )
        portal['questionfolder']['question2'].invokeFactory('emc.kb.answer', 'answer2',
                                                            content=u"answertwo",
                                                            title=u"answer2 title"
                                                            )
        portal['questionfolder']['question3'].invokeFactory('emc.kb.answer', 'answer3',
                                                            content=u"answerthree",
                                                            title=u"answer3 title"
                                                            )
        self.answer1 =portal['questionfolder']['question1']['answer1']
        self.answer2 =portal['questionfolder']['question2']['answer2']
        self.answer3 =portal['questionfolder']['question3']['answer3']                
        self.t1.relatedquestion=[RelationValue(intids.getId(self.q1)),RelationValue(intids.getId(self.q2)),RelationValue(intids.getId(self.q3))]
      
        event.notify(ObjectModifiedEvent(self.t1))
        
        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('user1', 'secret', ['Member'], [])
        acl_users.userFolderAddUser('user2', 'secret', ['Member'], [])
        acl_users.userFolderAddUser('user3', 'secret', ['Member'], [])        
        import transaction
        transaction.commit()
        
    def testtopicView(self):

        app = self.layer['app']
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        browser = Browser(app)
        browser.handleErrors = False
        
        
        intids = getUtility(IIntIds)
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question4',
                                            title='newquestion',
                                            affiliatedtopics=[RelationValue(intids.getId(self.t1))],
                                            )
        
#        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
        browser.open(self.t1.absolute_url())
        
        self.assertTrue("topicone" in browser.contents)
        self.assertTrue("descriptionone" in browser.contents)
        
        self.assertTrue("newquestion" in browser.contents)
        
        self.assertTrue("questionone" in browser.contents)
        self.assertTrue("answerone" in browser.contents)
#        self.assertTrue("questiontwo" in browser.contents)
#        self.assertTrue("answertwo" in browser.contents)
#        self.assertTrue("questionthree" in browser.contents)
#        self.assertTrue("answerthree" in browser.contents)
   
    def testquestionView(self):
        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
        
        browser.open(self.q1.absolute_url())
#        self.assertTrue("topicone" in browser.contents)
#        
#        self.assertTrue("topic1" in browser.contents)
        
        self.assertTrue("questionone" in browser.contents)
        
        self.assertTrue("answerone" in browser.contents)
#        self.assertTrue("2011-12-" in browser.contents)
        
        self.assertTrue("test_user_1_" in browser.contents)
        self.assertTrue("defaultUser.png" in browser.contents)
    
    def testanswerView(self):
        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
        browser.open(self.answer1.absolute_url())
        
        self.assertTrue("topic1" in browser.contents)
        
        self.assertTrue("questionone" in browser.contents)
        
        self.assertTrue("test_user_1_" in browser.contents)
        self.assertTrue("defaultUser.png" in browser.contents)
        
        self.assertTrue("answerone" in browser.contents)
        self.assertTrue("2011-12-" in browser.contents)
        
    def testhotanswerView(self):
        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        event.notify(LikeEvent(self.answer2))
        event.notify(LikeEvent(self.answer3))
        logout()
        login(portal, 'user1')
        event.notify(LikeEvent(self.answer3))                        
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
#        import pdb
#        pdb.set_trace()
        hotanswer = portal.absolute_url() + '/@@hotanswer'
        browser.open(hotanswer)

        self.assertTrue(u"test_user_1_" in browser.contents)
        self.assertTrue("defaultUser.png" in browser.contents)
        
        self.assertTrue(u"answerthree" in browser.contents)
        self.assertTrue(u"answertwo" in browser.contents)
        
    def testhottopicView(self):

        app = self.layer['app']        
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
        
        hottopic = portal.absolute_url() + '/@@hottopic'
        browser.open(hottopic)
        
#         self.assertTrue("topicfolder title" in browser.contents)
        self.assertTrue("topicone" in browser.contents)
        self.assertTrue("topictwo" in browser.contents)
        

    def testIfollowedView(self):
        app = self.layer['app']        
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        
        event.notify(FollowedEvent(self.q1))
        event.notify(FollowedEvent(self.q2))
        event.notify(FollowedEvent(self.q3))        
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
        
        questionfollowed = portal.absolute_url() + '/@@followed'
        browser.open(questionfollowed)
        
        self.assertTrue("questionone" in browser.contents)
        self.assertTrue("questiontwo" in browser.contents)
        self.assertTrue("questionthree" in browser.contents)
        self.assertTrue("col-md-2 unfollow" in browser.contents)
        
        event.notify(FollowedEvent(self.t1))
        event.notify(FollowedEvent(self.t2))
 
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
        
        topicfollowed = portal.absolute_url() + '/@@followed'
        browser.open(topicfollowed)
        
        self.assertTrue("topicone" in browser.contents)
#         self.assertTrue("descriptionone" in browser.contents)
        self.assertTrue("topictwo" in browser.contents)
#         self.assertTrue("descriptiontwo" in browser.contents)
           
    def testmyqaView(self):
        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))            
        import transaction
        transaction.commit()
#        import pdb
#        pdb.set_trace()
        myquestion = portal.absolute_url() + '/@@myquestion'
        browser.open(myquestion)
        
        self.assertTrue("questionone" in browser.contents)
        self.assertTrue("questiontwo" in browser.contents)
        self.assertTrue("questionthree" in browser.contents)
        import transaction
        transaction.commit()
        
        myquestion = portal.absolute_url() + '/@@myquestion'
        browser.open(myquestion)
        self.assertTrue("questionone" in browser.contents)
        self.assertTrue("questiontwo" in browser.contents)
        self.assertTrue("questionthree" in browser.contents)
        
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
        
        myanswer = portal.absolute_url() + '/@@myanswer'
        browser.open(myanswer)
        
        self.assertTrue("questionone" in browser.contents)
        self.assertTrue("questiontwo" in browser.contents)
        self.assertTrue("questionthree" in browser.contents)
        self.assertTrue("answerone" in browser.contents)
        self.assertTrue("answertwo" in browser.contents)
        self.assertTrue("answerthree" in browser.contents)
        
    def testmyfavoritefolderView(self):

        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False
        
        event.notify(FavoriteAnswerEvent(self.answer1))
        event.notify(FavoriteAnswerEvent(self.answer2))
        event.notify(FavoriteAnswerEvent(self.answer3))
        
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
        
        myfavoritefolder = portal.absolute_url() + '/@@myfavoritefolder'
        browser.open(myfavoritefolder)
        
        self.assertTrue("questionone" in browser.contents)
        self.assertTrue("questiontwo" in browser.contents)
        self.assertTrue("questionthree" in browser.contents)
        self.assertTrue("answerone" in browser.contents)
        self.assertTrue("answertwo" in browser.contents)
        self.assertTrue("answerthree" in browser.contents)
        
        self.assertTrue("test_user_1_" in browser.contents)
#        self.assertTrue("defaultUser.png" in browser.contents)
    
    def testmentionwoView(self):
        
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False
        
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
  
        browser.open(portal['mentionwofolder'].absolute_url())
        
        self.assertTrue("questionone" in browser.contents)
        self.assertTrue("questiontwo" in browser.contents)
        self.assertTrue("questionthree" in browser.contents)
        self.assertTrue("answerone" in browser.contents)
        self.assertTrue("answertwo" in browser.contents)
        self.assertTrue("answerthree" in browser.contents)
    
    def testsearchView(self):
        
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False
        
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
        
        search = portal.absolute_url() + '/@@search'
        browser.open(search)
        
#        self.assertFalse("questionone" in browser.contents)
#        self.assertFalse("questiontwo" in browser.contents)
#        self.assertFalse("questionthree" in browser.contents)
        
        browser.getControl(name='form.textbox').value = "question"
        browser.getControl(name='form.search').click()
        
        self.assertTrue("questionone" in browser.contents)
        self.assertTrue("questiontwo" in browser.contents)
        self.assertTrue("questionthree" in browser.contents)
    
    def testpersonalhomepageView(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False
        
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
        
        event.notify(FollowedEvent(self.t1))
        event.notify(FollowedEvent(self.t2))
        event.notify(FollowedEvent(self.q3))
        intids = getUtility(IIntIds)
        portal['questionfolder']['question3'].invokeFactory('emc.kb.answer', 'answer5',
                                 content=u"answerfour"
                                )



         
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question4',
                                            title='questionfour',
                                            affiliatedtopics=[RelationValue(intids.getId(self.t1))],
                                            )
        q4 = portal['questionfolder']['question4']
        event.notify(FollowedEvent(q4))        
        import transaction
        transaction.commit()
        browser.open(portal['feedsfolder'].absolute_url())        
        self.assertTrue("questionthree" in browser.contents)        
        self.assertTrue("questionfour" in browser.contents)
#        self.assertTrue(u"test_user_1_" in browser.contents)
#        self.assertTrue("defaultUser.png" in browser.contents)
#        self.assertFalse("answerfour" in browser.contents)

    def testhomepageView(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False
        
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
        
        intids = getUtility(IIntIds)
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question4',
                                            title='questionfour',
                                            affiliatedtopics=[RelationValue(intids.getId(self.t1))],
                                            )
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question5',
                                            title='questionfive',
                                            affiliatedtopics=[RelationValue(intids.getId(self.t1))],
                                            )
        import transaction
        transaction.commit()
        
        event.notify(FollowedEvent(portal['questionfolder']['question4']))
        event.notify(FollowedEvent(portal['questionfolder']['question5']))
        event.notify(FollowedEvent(self.t1))
        event.notify(FollowedEvent(self.t2))
        
        import transaction
        transaction.commit()
        
        homepage = portal.absolute_url() + '/@@homepage'
        browser.open(homepage)
        
#        open('/tmp/test.html','w').write(browser.contents)

        import transaction
        transaction.commit()
        self.assertTrue("questionfour" in browser.contents)
        self.assertTrue("questionfive" in browser.contents)
        self.assertTrue("topicone" in browser.contents)
        self.assertTrue("topictwo" in browser.contents)
        
        self.assertTrue("questionone" in browser.contents)
        self.assertTrue("questiontwo" in browser.contents)
        self.assertTrue("questionthree" in browser.contents)
        self.assertTrue("answerone" in browser.contents)
        self.assertTrue("answertwo" in browser.contents)
        self.assertTrue("answerthree" in browser.contents)
        
    def testtopicfolderView(self):
        app = self.layer['app']
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        
        import transaction
        transaction.commit()
        
        browser.open(portal['topicfolder'].absolute_url())
        
#        open('/tmp/test.html','w').write(browser.contents)
        
        self.assertTrue("topicone" in browser.contents)
        self.assertTrue("topictwo" in browser.contents)        
#        self.assertTrue("descriptionone" in browser.contents)
        
#        self.assertTrue("questionone" in browser.contents)
#        self.assertTrue("questiontwo" in browser.contents)
#        self.assertTrue("questionthree" in browser.contents)
#        
#        self.assertTrue("answerone" in browser.contents)
#        self.assertTrue("answertwo" in browser.contents)
#        self.assertTrue("answerthree" in browser.contents)

