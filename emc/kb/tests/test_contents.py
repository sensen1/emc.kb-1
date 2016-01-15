import unittest as unittest

from emc.kb.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
#from plone.namedfile.file import NamedImage

class Allcontents(unittest.TestCase):
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.feedsfolder', 'feedsfolder')
        portal['feedsfolder'].invokeFactory('emc.kb.feed', 'feed',
                             name=u"feed1",
                             description=u"feed1 description",
                             )         
        portal.invokeFactory('emc.kb.topicfolder', 'topicfolder')
        portal['topicfolder'].invokeFactory('emc.kb.topic', 'topic',
                             name=u"topic",
                             description=u"description",
                             )

                
        portal.invokeFactory('emc.kb.questionfolder', 'questionfolder')             
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

        self.portal = portal
    
    def test_item_types(self):
        self.assertEqual(self.portal['feedsfolder']['feed'].name,u'feed1')
        self.assertEqual(self.portal['feedsfolder']['feed'].description,u'feed1 description')        
        self.assertEqual(self.portal['topicfolder']['topic'].name,u'topic')
        self.assertEqual(self.portal['topicfolder']['topic'].description,u'description')
        self.assertTrue(self.portal['topicfolder']['topic'].id)        
        self.assertEqual(self.portal['questionfolder'].id,'questionfolder')
        self.assertEqual(self.portal['topicfolder'].id,'topicfolder')        
        self.assertEqual(self.portal['topicfolder']['topic'].id,'topic')    
        self.assertEqual(self.portal['questionfolder']['question'].id,'question')              
        self.assertEqual(self.portal['questionfolder']['question']['answer1'].id,'answer1') 

                                     
                  
       
        