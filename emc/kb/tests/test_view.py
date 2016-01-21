from plone.testing.z2 import Browser

import unittest
from zope import event
from emc.kb.testing import INTEGRATION_TESTING
from emc.kb.testing import FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID,TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import setRoles,login,logout

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
from emc.memberArea.events import FavoriteEvent
from emc.memberArea.events import UnFavoriteEvent
from emc.kb.events import LikeEvent
from emc.kb.events import UnLikeEvent
from emc.memberArea.events import MemberAreaCreatedEvent

from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent import ObjectModifiedEvent,ObjectAddedEvent


from emc.kb.contents.question import Iquestion
from emc.kb.contents.topic import Itopic
from emc.kb.contents.answer import Ianswer
from emc.kb.contents.feed import Ifeed

from emc.kb.interfaces import IFollowing
# from emc.kb.interfaces import IAnswerEvaluate
from emc.kb.interfaces import IFollowing



class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    def setUp(self):
        portal = self.layer['portal']
        self.catalog = getToolByName(portal, 'portal_catalog')  
        setRoles(portal, TEST_USER_ID, ('Manager',))
        intids = getUtility(IIntIds)
        portal.invokeFactory('Folder', 'Members')
        portal.invokeFactory('emc.kb.folder', 'folder') 
        portal['folder'].invokeFactory('emc.kb.mentionmefolder', 'mentionmefolder')
        portal['folder'].invokeFactory('emc.kb.feedsfolder', 'feedsfolder')
        portal['folder'].invokeFactory('emc.kb.questionfolder', 'questionfolder')
        portal['folder'].invokeFactory('emc.kb.topicfolder', 'topicfolder',title="topicfolder title")
        portal['folder']['topicfolder'].invokeFactory("emc.kb.topic",'topic1',
                                            title=u"topicone",
                                            description=u"descriptionone"
                                            )
        portal['folder']['topicfolder'].invokeFactory("emc.kb.topic",'topic2',
                                            title=u"topictwo",
                                            description=u"descriptiontwo"
                                            )        
        self.t1 = portal['folder']['topicfolder']['topic1']
        self.t2 = portal['folder']['topicfolder']['topic2']
        portal['folder']['questionfolder'].invokeFactory('emc.kb.question', 'question1',
                                            title='questionone',
                                            affiliatedtopics=[RelationValue(intids.getId(self.t1))],
                                            )
        portal['folder']['questionfolder'].invokeFactory('emc.kb.question', 'question2',
                                            title='questiontwo',
                                            affiliatedtopics=[RelationValue(intids.getId(self.t1))],
                                            )
        portal['folder']['questionfolder'].invokeFactory('emc.kb.question', 'question3',
                                            title='questionthree',
                                            affiliatedtopics=[RelationValue(intids.getId(self.t1))],
                                            )
        self.q1 = portal['folder']['questionfolder']['question1']
        self.q2 = portal['folder']['questionfolder']['question2'] 
        self.q3 = portal['folder']['questionfolder']['question3']
        portal['folder']['questionfolder']['question1'].invokeFactory('emc.kb.answer', 'answer1',
                                                            content=u"answerone",
                                                            title=u"answerone"
                                                            )
        portal['folder']['questionfolder']['question2'].invokeFactory('emc.kb.answer', 'answer2',
                                                            content=u"answertwo",
                                                            title=u"answer2 title"
                                                            )
        portal['folder']['questionfolder']['question3'].invokeFactory('emc.kb.answer', 'answer3',
                                                            content=u"answerthree",
                                                            title=u"answer3 title"
                                                            )
        self.answer1 =portal['folder']['questionfolder']['question1']['answer1']
        self.answer2 =portal['folder']['questionfolder']['question2']['answer2']
        self.answer3 =portal['folder']['questionfolder']['question3']['answer3']                
        self.t1.relatedquestion=[RelationValue(intids.getId(self.q1)),RelationValue(intids.getId(self.q2)),RelationValue(intids.getId(self.q3))]
      
        event.notify(ObjectModifiedEvent(self.t1))
        
#         acl_users = getToolByName(portal, 'acl_users')
        self.membership = getToolByName(portal,'portal_membership')
        self.membership.addMember('member', 'secret', ['Member'], [])
        self.membership.addMember('user1', 'secret', ['Member'], [])
        self.membership.addMember('user2', 'secret', ['Member'], [])
        self.membership.addMember('user3', 'secret', ['Member'], [])
#         acl_users.userFolderAddUser('user1', 'secret', ['Member'], [])
#         acl_users.userFolderAddUser('user2', 'secret', ['Member'], [])
#         acl_users.userFolderAddUser('user3', 'secret', ['Member'], [])        
        self.membership.memberareaCreationFlag = True
        import transaction
        transaction.commit()
        logout()
        login(portal, 'user1')        
        self.membership.loginUser()
        user = self.membership.getAuthenticatedMember()
        event.notify(MemberAreaCreatedEvent(user))
        transaction.commit()
        
        logout()
        login(portal, 'user2')        
        self.membership.loginUser()
        user = self.membership.getAuthenticatedMember()
        event.notify(MemberAreaCreatedEvent(user))
        transaction.commit()
        logout()
        login(portal, 'user3')        
        self.membership.loginUser()
        user = self.membership.getAuthenticatedMember()
        event.notify(MemberAreaCreatedEvent(user))
        user.setProperties(fullname=u"test user3")
        setRoles(portal, 'user3', ('Manager',))    
        transaction.commit()
        self.portal = portal
        
#     def testLoggedInCreatesMemberArea(self):
#         if self.membership.memberareaCreationFlag == 'True':
#             self.assertEqual(self.membership.getHomeFolder(), None)
#             self.portal.logged_in()
#             self.assertNotEqual(self.membership.getHomeFolder(), None)
        
    def testtopicView(self):

        app = self.layer['app']
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        browser = Browser(app)
        browser.handleErrors = False
        
        
        intids = getUtility(IIntIds)
        portal['folder']['questionfolder'].invokeFactory('emc.kb.question', 'question4',
                                            title='newquestion',
                                            affiliatedtopics=[RelationValue(intids.getId(self.t1))],
                                            )
        
#        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        browser.addHeader('Authorization', 'Basic %s:%s' % ('user3', 'secret',))
        import transaction
        transaction.commit()
        browser.open(self.t1.absolute_url())
        
        self.assertTrue("topicone" in browser.contents)
        self.assertTrue("descriptionone" in browser.contents)
        
#         self.assertTrue("newquestion" in browser.contents)
        
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
        self.assertTrue("topicone" in browser.contents)        
        self.assertTrue("topic1" in browser.contents)        
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
        browser.addHeader('Authorization', 'Basic %s:%s' % ('user3', 'secret',))
        intids = getUtility(IIntIds)
        self.q1.affiliatedtopics=[RelationValue(intids.getId(self.t1))]
        event.notify(ObjectModifiedEvent(self.q1))
       
        import transaction
        transaction.commit()
        browser.open(self.answer1.absolute_url())        

        self.assertTrue("topicone" in browser.contents)        
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
        
        event.notify(FavoriteEvent(self.answer1))
        event.notify(FavoriteEvent(self.answer2))
        event.notify(FavoriteEvent(self.answer3))
        
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
    
    def testmentionmeView(self):
        
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False
        event.notify(FollowedEvent(self.q1))
        event.notify(FollowedEvent(self.q2))
        event.notify(FollowedEvent(self.q3))  
        portal['folder']['questionfolder'].invokeFactory('emc.kb.question', 'question10',
                             title=u"question10",
                             description = u"by user3 created"
                             )
        portal['folder']['questionfolder']['question10'].invokeFactory('emc.kb.answer', 'answer10',
                             title=u"answer10",
                             description = u"by user3 created"
                             )
        event.notify(ObjectAddedEvent(portal['folder']['questionfolder']['question10']['answer10']))
        logout()
        login(portal, 'user1')

        setRoles(portal, 'user1', ('Manager',))
        event.notify(LikeEvent(portal['folder']['questionfolder']['question10']['answer10']))
        portal['folder']['questionfolder']['question10'].invokeFactory('emc.kb.answer', 'answer11',
                             title=u"answer11",
                             description = u"by user1 created"
                             )
        event.notify(ObjectAddedEvent(portal['folder']['questionfolder']['question10']['answer11']))        
        portal['folder']['questionfolder']['question1'].invokeFactory('emc.kb.answer', 'answer9',
                             title=u"answer9",
                             description = u"by user1 created"
                             )                                 
        event.notify(ObjectAddedEvent(portal['folder']['questionfolder']['question1']['answer9']))
        browser.addHeader('Authorization', 'Basic %s:%s' % ('user3', 'secret',))
        import transaction
        transaction.commit()
        user = self.membership.getAuthenticatedMember()
        mentionmefolderUrl = self.membership.getHomeUrl(user.getId()) + "/workspace/mentionmefolder"
  
        browser.open(mentionmefolderUrl)
        import pdb
        pdb.set_trace()
        
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
        
        browser.getControl(name='form.SearchableText').value = "question"
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
        portal['folder']['questionfolder']['question3'].invokeFactory('emc.kb.answer', 'answer5',
                                 content=u"answerfour"
                                )
         
        portal['folder']['questionfolder'].invokeFactory('emc.kb.question', 'question4',
                                            title='questionfour',
                                            affiliatedtopics=[RelationValue(intids.getId(self.t1))],
                                            )
        q4 = portal['folder']['questionfolder']['question4']
        event.notify(FollowedEvent(q4))        
        import transaction
        transaction.commit()
        browser.open(portal['folder']['feedsfolder'].absolute_url())        
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
        portal['folder']['questionfolder'].invokeFactory('emc.kb.question', 'question4',
                                            title='questionfour',
                                            affiliatedtopics=[RelationValue(intids.getId(self.t1))],
                                            )
        portal['folder']['questionfolder'].invokeFactory('emc.kb.question', 'question5',
                                            title='questionfive',
                                            affiliatedtopics=[RelationValue(intids.getId(self.t1))],
                                            )
        import transaction
        transaction.commit()
        
        event.notify(FollowedEvent(portal['folder']['questionfolder']['question4']))
        event.notify(FollowedEvent(portal['folder']['questionfolder']['question5']))
        event.notify(FollowedEvent(self.t1))
        event.notify(FollowedEvent(self.t2))
        
        import transaction
        transaction.commit()
        
        homepage = portal['folder'].absolute_url() + '/@@view'
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
        
        browser.open(portal['folder']['topicfolder'].absolute_url())
        
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

    def testquesionfollowView(self):
        app = self.layer['app']
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        
        import transaction
        transaction.commit()
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
        
        browser.open(portal.absolute_url() + "/@@questionfollowed")
        
#        open('/tmp/test.html','w').write(browser.contents)
        

        self.assertTrue("topicone" in browser.contents)
#         self.assertTrue("topictwo" in browser.contents)
        self.assertTrue("questionone" in browser.contents)
        self.assertTrue("questiontwo" in browser.contents)        


    def testtopicfollowView(self):
        app = self.layer['app']
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        
        import transaction
        transaction.commit()
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
        browser.open(portal.absolute_url() + "/@@topicfollowed")

        
        self.assertTrue("topicone" in browser.contents)
        self.assertTrue("topictwo" in browser.contents)
       
