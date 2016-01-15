import unittest
from zope import event
from emc.kb.testing import INTEGRATION_TESTING
from emc.kb.testing import FUNCTIONAL_TESTING
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

class TestSetup(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    
    def test_AnswerLikeEvent_event(self):
        from emc.kb.events import LikeEvent
        from emc.kb.events import UnLikeEvent
        from emc.kb.contents.answer import Ianswer
        from emc.kb.interfaces import IVoting
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.questionfolder', 'questionfolder')
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question',
                             discription=u"discription",
                             additional=u"additional",
                             isfollowed=True,
                             affiliatedtopics=u"affiliatedtopics",
                             relatedquestion=u"relatedquestion",
                             followernum=u"followernum",
                             pageview=u"pageview",
                             date=u"date"
                             )
        portal['questionfolder']['question'].invokeFactory('emc.kb.answer', 'answer',
                             answerer=u"answerer",
                             voteNum=u"voteNum",
                             voters=u"voters",
                             content=u"content of the answer",
                             date=u"date of the answer",
                             )
        file=portal['questionfolder']['question']['answer']
            
        event.notify(LikeEvent(file))
        mp = getToolByName(portal,'portal_membership')
        userobject= mp.getAuthenticatedMember()
        username = userobject.getId()
        agreelist = list(userobject.getProperty('mylike'))
        evlute = IVoting(file)
        
        self.assertTrue(file.id in agreelist)
        self.assertTrue(evlute.voteavailableapproved(username))
        self.assertEqual(1,evlute.voteNum) 


        event.notify(UnLikeEvent(file))
        mp = getToolByName(portal,'portal_membership')
        userobject= mp.getAuthenticatedMember()
        username = userobject.getId()
        disagreelist = list(userobject.getProperty('myunlike'))
        evlute = IVoting(file)
        
        self.assertTrue(file.id in disagreelist)
        self.assertTrue(evlute.voteavailabledisapproved(username))
        
#     def test_AddFavorite_event(self):
#         from emc.kb.events import FavoriteAnswerEvent
#         from emc.kb.events import UnFavoriteAnswerEvent
#         from emc.kb.contents.answer import Ianswer
#         from emc.kb.interfaces import IVoting
#         portal = self.layer['portal']
#         setRoles(portal, TEST_USER_ID, ('Manager',))
#         portal.invokeFactory('emc.kb.questionfolder', 'questionfolder')
#         portal['questionfolder'].invokeFactory('emc.kb.question', 'question',
#                              discription=u"discription",
#                              additional=u"additional",
#                              isfollowed=True,
#                              affiliatedtopics=u"affiliatedtopics",
#                              relatedquestion=u"relatedquestion",
#                              followernum=u"followernum",
#                              pageview=u"pageview",
#                              date=u"date"
#                              )
#         portal['questionfolder']['question'].invokeFactory('emc.kb.answer', 'answer',
#                              answerer=u"answerer",
#                              voteNum=u"voteNum",
#                              voters=u"voters",
#                              content=u"content of the answer",
#                              date=u"date of the answer",
#                              )
#         file=portal['questionfolder']['question']['answer']  
#         event.notify(FavoriteAnswerEvent(file))
#         mp = getToolByName(portal,'portal_membership')
#         userobject = mp.getAuthenticatedMember()
#         username = userobject.getId()
#         favoritelist = list(userobject.getProperty('myfavorite'))
#         evlute = IVoting(file)
#         
#         self.assertTrue(file.id in favoritelist)
#         self.assertTrue(evlute.favavailable(username)) 
# 
#         event.notify(UnFavoriteAnswerEvent(file))
#         mp = getToolByName(portal,'portal_membership')
#         userobject= mp.getAuthenticatedMember()
#         username = userobject.getId()
#         favoritelist = list(userobject.getProperty('myfavorite'))
#         evlute = IVoting(file) 
#         
#         self.assertFalse(file.id in favoritelist)
#         self.assertFalse(evlute.favavailable(username))                    

